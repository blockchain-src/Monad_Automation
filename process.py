import asyncio
import random

from loguru import logger

from src.model.disperse_from_one.instance import DisperseFromOneWallet
from src.model.disperse_one_one.instance import DisperseOneOne
import src.utils
from src.utils.logs import report_error, report_success
from src.utils.output import show_dev_info, show_logo
import src.model
from src.utils.statistics import print_wallets_stats


async def start():
    async def launch_wrapper(index, proxy, private_key, discord_token, email):
        async with semaphore:
            await account_flow(
                index,
                proxy,
                private_key,
                discord_token,
                email,
                config,
                lock,
            )

    show_logo()
    show_dev_info()

    print("\nAvailable options:\n")
    print("[1] 😈 Start farm")
    print("[2] 🔧 Edit config")
    print("[3] 👋 Exit")
    print()

    try:
        choice = input("Enter option (1-3): ").strip()
    except Exception as e:
        logger.error(f"Input error: {e}")
        return

    if choice == "3" or not choice:
        return
    elif choice == "2":
        config_ui = src.utils.ConfigUI()
        config_ui.run()
        return
    elif choice == "1":
        pass
    else:
        logger.error(f"Invalid choice: {choice}")
        return

    config = src.utils.get_config()

    # 读取所有文件
    proxies = src.utils.read_txt_file("proxies", "data/proxies.txt")
    if len(proxies) == 0:
        logger.error("No proxies found in data/proxies.txt")
        return

    if "disperse_farm_accounts" in config.FLOW.TASKS:
        main_keys = src.utils.read_txt_file("private keys", "data/private_keys.txt")
        farm_keys = src.utils.read_txt_file("private keys", "data/keys_for_faucet.txt")
        disperse_one_one = DisperseOneOne(main_keys, farm_keys, proxies, config)
        await disperse_one_one.disperse()
        return
    elif "disperse_from_one_wallet" in config.FLOW.TASKS:
        main_keys = src.utils.read_txt_file("private keys", "data/private_keys.txt")
        farm_keys = src.utils.read_txt_file("private keys", "data/keys_for_faucet.txt")
        disperse_one_wallet = DisperseFromOneWallet(
            farm_keys[0], main_keys, proxies, config
        )
        await disperse_one_wallet.disperse()
        return

    if "farm_faucet" in config.FLOW.TASKS:
        private_keys = src.utils.read_txt_file(
            "private keys", "data/keys_for_faucet.txt"
        )
    else:
        private_keys = src.utils.read_txt_file("private keys", "data/private_keys.txt")

    # 确定账户范围
    start_index = config.SETTINGS.ACCOUNTS_RANGE[0]
    end_index = config.SETTINGS.ACCOUNTS_RANGE[1]

    # 如果两者都为 0，则检查 EXACT_ACCOUNTS_TO_USE
    if start_index == 0 and end_index == 0:
        if config.SETTINGS.EXACT_ACCOUNTS_TO_USE:
            # 将账户编号转换为索引（编号 - 1）
            selected_indices = [i - 1 for i in config.SETTINGS.EXACT_ACCOUNTS_TO_USE]
            accounts_to_process = [private_keys[i] for i in selected_indices]
            logger.info(
                f"Using specific accounts: {config.SETTINGS.EXACT_ACCOUNTS_TO_USE}"
            )

            # 兼容其他代码
            start_index = min(config.SETTINGS.EXACT_ACCOUNTS_TO_USE)
            end_index = max(config.SETTINGS.EXACT_ACCOUNTS_TO_USE)
        else:
            # 如果列表为空，则像以前一样使用所有账户
            accounts_to_process = private_keys
            start_index = 1
            end_index = len(private_keys)
    else:
        # Python 切片不包含最后一个元素，因此 +1
        accounts_to_process = private_keys[start_index - 1 : end_index]

    discord_tokens = [""] * len(accounts_to_process)
    emails = [""] * len(accounts_to_process)

    threads = config.SETTINGS.THREADS

    # 为选定的账户准备代理
    cycled_proxies = [
        proxies[i % len(proxies)] for i in range(len(accounts_to_process))
    ]

    # 创建索引列表并对其进行随机排列
    shuffled_indices = list(range(len(accounts_to_process)))
    random.shuffle(shuffled_indices)

    # 创建账户顺序的字符串
    account_order = " ".join(str(start_index + idx) for idx in shuffled_indices)
    logger.info(
        f"Starting with accounts {start_index} to {end_index} in random order..."
    )
    logger.info(f"Accounts order: {account_order}")

    lock = asyncio.Lock()
    semaphore = asyncio.Semaphore(value=threads)
    tasks = []

    # 使用随机化索引创建任务
    for shuffled_idx in shuffled_indices:
        tasks.append(
            asyncio.create_task(
                launch_wrapper(
                    start_index + shuffled_idx,
                    cycled_proxies[shuffled_idx],
                    accounts_to_process[shuffled_idx],
                    discord_tokens[shuffled_idx],
                    emails[shuffled_idx],
                )
            )
        )

    await asyncio.gather(*tasks)

    logger.success("Saved accounts and private keys to a file.")

    print_wallets_stats(config)


def task_exists_in_config(task_name: str, tasks_list: list) -> bool:
    """递归检查任务是否存在于任务列表中，包括嵌套列表"""
    for task in tasks_list:
        if isinstance(task, list):
            if task_exists_in_config(task_name, task):
                return True
        elif task == task_name:
            return True
    return False
