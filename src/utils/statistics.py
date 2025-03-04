from tabulate import tabulate
from typing import List, Optional
from loguru import logger

from src.utils.config import Config, WalletInfo

def print_wallets_stats(config: Config):
    """
    以表格形式输出所有钱包的统计信息
    """
    try:
        # 按索引对钱包进行排序
        sorted_wallets = sorted(config.WALLETS.wallets, key=lambda x: x.account_index)

        # 准备表格数据
        table_data = []
        total_balance = 0
        total_transactions = 0

        for wallet in sorted_wallets:
            # 隐藏私钥（仅显示最后 5 个字符）
            masked_key = "•" * 3 + wallet.private_key[-5:]

            total_balance += wallet.balance
            total_transactions += wallet.transactions

            row = [
                str(wallet.account_index),  # 纯数字索引，无前导零
                wallet.address,  # 完整钱包地址
                masked_key,
                f"{wallet.balance:.4f} MON",  # 余额格式化为 4 位小数
                f"{wallet.transactions:,}",  # 交易次数，带千位分隔符
            ]
            table_data.append(row)

        # 如果有数据，则输出表格和统计信息
        if table_data:
            # 创建表格标题
            headers = [
                "№ Account",
                "Wallet Address",
                "Private Key",
                "Balance (MON)",
                "Total Txs",
            ]

            # 生成表格，使用更美观的格式
            table = tabulate(
                table_data,
                headers=headers,
                tablefmt="double_grid",  # 更美观的边框
                stralign="center",  # 文本居中对齐
                numalign="center",  # 数字居中对齐
            )

            # 计算平均值
            wallets_count = len(sorted_wallets)
            avg_balance = total_balance / wallets_count
            avg_transactions = total_transactions / wallets_count

            # 输出表格和统计数据
            logger.info(
                f"\n{'='*50}\n"
                f"         钱包统计信息 ({wallets_count} 个钱包)\n"
                f"{'='*50}\n"
                f"{table}\n"
                f"{'='*50}\n"
                f"{'='*50}"
            )

            logger.info(f"平均余额: {avg_balance:.4f} MON")
            logger.info(f"平均交易次数: {avg_transactions:.1f}")
            logger.info(f"总余额: {total_balance:.4f} MON")
            logger.info(f"总交易次数: {total_transactions:,}")
        else:
            logger.info("\n暂无钱包统计数据")

    except Exception as e:
        logger.error(f"打印统计信息时出错: {e}")
