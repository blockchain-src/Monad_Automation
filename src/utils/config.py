from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
import yaml
from pathlib import Path
import asyncio


@dataclass
class SettingsConfig:
    THREADS: int
    ATTEMPTS: int
    ACCOUNTS_RANGE: Tuple[int, int]
    EXACT_ACCOUNTS_TO_USE: List[int]
    PAUSE_BETWEEN_ATTEMPTS: Tuple[int, int]
    PAUSE_BETWEEN_SWAPS: Tuple[int, int]
    RANDOM_PAUSE_BETWEEN_ACCOUNTS: Tuple[int, int]
    RANDOM_PAUSE_BETWEEN_ACTIONS: Tuple[int, int]
    BROWSER_PAUSE_MULTIPLIER: float
    RANDOM_INITIALIZATION_PAUSE: Tuple[int, int]
    TELEGRAM_USERS_IDS: List[int]
    TELEGRAM_BOT_TOKEN: str

@dataclass
class FaucetConfig:
    CAPSOLVER_API_KEY: str


@dataclass
class FlowConfig:
    TASKS: List
    NUMBER_OF_SWAPS: Tuple[int, int]
    PERCENT_OF_BALANCE_TO_SWAP: Tuple[int, int]


@dataclass
class AprioriConfig:
    AMOUNT_TO_STAKE: Tuple[float, float]


@dataclass
class MagmaConfig:
    AMOUNT_TO_STAKE: Tuple[float, float]


@dataclass
class KintsuConfig:
    AMOUNT_TO_STAKE: Tuple[float, float]


@dataclass
class BimaConfig:
    LEND: bool
    PERCENT_OF_BALANCE_TO_LEND: Tuple[int, int]


@dataclass
class WalletInfo:
    account_index: int
    private_key: str
    address: str
    balance: float
    transactions: int


@dataclass
class WalletsConfig:
    wallets: List[WalletInfo] = field(default_factory=list)


@dataclass
class GaszipConfig:
    NETWORKS_TO_REFUEL_FROM: List[str]
    AMOUNT_TO_REFUEL: Tuple[float, float]
    MINIMUM_BALANCE_TO_REFUEL: float
    WAIT_FOR_FUNDS_TO_ARRIVE: bool
    MAX_WAIT_TIME: int
    BRIDGE_ALL: bool
    BRIDGE_ALL_MAX_AMOUNT: float


@dataclass
class MemebridgeConfig:
    NETWORKS_TO_REFUEL_FROM: List[str]
    AMOUNT_TO_REFUEL: Tuple[float, float]
    MINIMUM_BALANCE_TO_REFUEL: float
    WAIT_FOR_FUNDS_TO_ARRIVE: bool
    MAX_WAIT_TIME: int
    BRIDGE_ALL: bool
    BRIDGE_ALL_MAX_AMOUNT: float


@dataclass
class TestnetBridgeConfig:
    NETWORKS_TO_REFUEL_FROM: List[str]
    AMOUNT_TO_REFUEL: Tuple[float, float]
    MINIMUM_BALANCE_TO_REFUEL: float
    WAIT_FOR_FUNDS_TO_ARRIVE: bool
    MAX_WAIT_TIME: int


@dataclass
class ShmonadConfig:
    PERCENT_OF_BALANCE_TO_SWAP: Tuple[int, int]
    BUY_AND_STAKE_SHMON: bool
    UNSTAKE_AND_SELL_SHMON: bool


@dataclass
class AccountableConfig:
    NFT_PER_ACCOUNT_LIMIT: int


@dataclass
class OrbiterConfig:
    AMOUNT_TO_BRIDGE: Tuple[float, float]
    BRIDGE_ALL: bool
    WAIT_FOR_FUNDS_TO_ARRIVE: bool
    MAX_WAIT_TIME: int


@dataclass
class DisperseConfig:
    MIN_BALANCE_FOR_DISPERSE: Tuple[float, float]


@dataclass
class LilchogstarsConfig:
    MAX_AMOUNT_FOR_EACH_ACCOUNT: Tuple[int, int]


@dataclass
class DemaskConfig:
    MAX_AMOUNT_FOR_EACH_ACCOUNT: Tuple[int, int]


@dataclass
class MonadkingConfig:
    MAX_AMOUNT_FOR_EACH_ACCOUNT: Tuple[int, int]


@dataclass
class MagicEdenConfig:
    NFT_CONTRACTS: List[str]


@dataclass
class WithdrawalConfig:
    currency: str
    networks: List[str]
    min_amount: float
    max_amount: float
    wait_for_funds: bool
    max_wait_time: int
    retries: int
    max_balance: float  # 允许提现的最大钱包余额


@dataclass
class ExchangesConfig:
    name: str  # 交易所名称 (OKX, BINANCE, BYBIT)
    apiKey: str
    secretKey: str
    passphrase: str  # 仅适用于 OKX
    withdrawals: List[WithdrawalConfig]


@dataclass
class Config:
    SETTINGS: SettingsConfig
    EXCHANGES: ExchangesConfig
    FAUCET: FaucetConfig
    FLOW: FlowConfig
    APRIORI: AprioriConfig
    MAGMA: MagmaConfig
    KINTSU: KintsuConfig
    BIMA: BimaConfig
    GASZIP: GaszipConfig
    SHMONAD: ShmonadConfig
    ACCOUNTABLE: AccountableConfig
    ORBITER: OrbiterConfig
    DISPERSE: DisperseConfig
    LILCHOGSTARS: LilchogstarsConfig
    DEMASK: DemaskConfig
    MONADKING: MonadkingConfig
    MAGICEDEN: MagicEdenConfig
    MEMEBRIDGE: MemebridgeConfig
    TESTNET_BRIDGE: TestnetBridgeConfig
    WALLETS: WalletsConfig = field(default_factory=WalletsConfig)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    @classmethod
    def load(cls, path: str = "config.yaml") -> "Config":
        """Load configuration from yaml file"""
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # 从tasks.py加载任务
        try:
            # 尝试使用常规导入从tasks.py导入任务
            import tasks

            if hasattr(tasks, "TASKS"):
                # TASKS 现在包含预设名称
                preset_names = [preset_name.upper() for preset_name in tasks.TASKS]

                # 合并所有指定预设中的任务
                combined_tasks = []
                for preset_name in preset_names:
                    if hasattr(tasks, preset_name):
                        preset_tasks = getattr(tasks, preset_name)
                        combined_tasks.extend(preset_tasks)
                    else:
                        print(f"Warning: Preset {preset_name} not found in tasks.py")

                if combined_tasks:
                    tasks_list = combined_tasks
                else:
                    error_msg = "No valid presets found in tasks.py"
                    print(f"Error: {error_msg}")
                    raise ValueError(error_msg)
            else:
                error_msg = "No TASKS list found in tasks.py"
                print(f"Error: {error_msg}")
                raise ValueError(error_msg)
        except ImportError as e:
            error_msg = f"Could not import tasks.py: {e}"
            print(f"Error: {error_msg}")
            raise ImportError(error_msg) from e

        return cls(
            SETTINGS=SettingsConfig(
                THREADS=data["SETTINGS"]["THREADS"],
                ATTEMPTS=data["SETTINGS"]["ATTEMPTS"],
                ACCOUNTS_RANGE=tuple(data["SETTINGS"]["ACCOUNTS_RANGE"]),
                EXACT_ACCOUNTS_TO_USE=data["SETTINGS"]["EXACT_ACCOUNTS_TO_USE"],
                PAUSE_BETWEEN_ATTEMPTS=tuple(
                    data["SETTINGS"]["PAUSE_BETWEEN_ATTEMPTS"]
                ),
                PAUSE_BETWEEN_SWAPS=tuple(data["SETTINGS"]["PAUSE_BETWEEN_SWAPS"]),
                RANDOM_PAUSE_BETWEEN_ACCOUNTS=tuple(
                    data["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACCOUNTS"]
                ),
                RANDOM_PAUSE_BETWEEN_ACTIONS=tuple(
                    data["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACTIONS"]
                ),
                RANDOM_INITIALIZATION_PAUSE=tuple(
                    data["SETTINGS"]["RANDOM_INITIALIZATION_PAUSE"]
                ),
                BROWSER_PAUSE_MULTIPLIER=data["SETTINGS"]["BROWSER_PAUSE_MULTIPLIER"],
                TELEGRAM_USERS_IDS=data["SETTINGS"]["TELEGRAM_USERS_IDS"],
                TELEGRAM_BOT_TOKEN=data["SETTINGS"]["TELEGRAM_BOT_TOKEN"],
            ),
            EXCHANGES=ExchangesConfig(
                name=data["EXCHANGES"]["name"],
                apiKey=data["EXCHANGES"]["apiKey"],
                secretKey=data["EXCHANGES"]["secretKey"],
                passphrase=data["EXCHANGES"]["passphrase"],
                withdrawals=[
                    WithdrawalConfig(
                        currency=w["currency"],
                        networks=w["networks"],
                        min_amount=w["min_amount"],
                        max_amount=w["max_amount"],
                        wait_for_funds=w["wait_for_funds"],
                        max_wait_time=w["max_wait_time"],
                        retries=w["retries"],
                        max_balance=w["max_balance"]
                    ) for w in data["EXCHANGES"]["withdrawals"]
                ]
            ),
            FAUCET=FaucetConfig(
                CAPSOLVER_API_KEY=data["FAUCET"]["CAPSOLVER_API_KEY"],
            ),
            FLOW=FlowConfig(
                TASKS=tasks_list,
                NUMBER_OF_SWAPS=tuple(data["FLOW"]["NUMBER_OF_SWAPS"]),
                PERCENT_OF_BALANCE_TO_SWAP=tuple(
                    data["FLOW"]["PERCENT_OF_BALANCE_TO_SWAP"]
                ),
            ),
            APRIORI=AprioriConfig(
                AMOUNT_TO_STAKE=tuple(data["APRIORI"]["AMOUNT_TO_STAKE"]),
            ),
            MAGMA=MagmaConfig(
                AMOUNT_TO_STAKE=tuple(data["MAGMA"]["AMOUNT_TO_STAKE"]),
            ),
            KINTSU=KintsuConfig(
                AMOUNT_TO_STAKE=tuple(data["KINTSU"]["AMOUNT_TO_STAKE"]),
            ),
            BIMA=BimaConfig(
                LEND=data["BIMA"]["LEND"],
                PERCENT_OF_BALANCE_TO_LEND=tuple(
                    data["BIMA"]["PERCENT_OF_BALANCE_TO_LEND"]
                ),
            ),
            GASZIP=GaszipConfig(
                NETWORKS_TO_REFUEL_FROM=data["GASZIP"]["NETWORKS_TO_REFUEL_FROM"],
                AMOUNT_TO_REFUEL=tuple(data["GASZIP"]["AMOUNT_TO_REFUEL"]),
                MINIMUM_BALANCE_TO_REFUEL=data["GASZIP"]["MINIMUM_BALANCE_TO_REFUEL"],
                WAIT_FOR_FUNDS_TO_ARRIVE=data["GASZIP"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
                MAX_WAIT_TIME=data["GASZIP"]["MAX_WAIT_TIME"],
                BRIDGE_ALL=data["GASZIP"]["BRIDGE_ALL"],
                BRIDGE_ALL_MAX_AMOUNT=data["GASZIP"]["BRIDGE_ALL_MAX_AMOUNT"],
            ),
            MEMEBRIDGE=MemebridgeConfig(
                NETWORKS_TO_REFUEL_FROM=data["MEMEBRIDGE"]["NETWORKS_TO_REFUEL_FROM"],
                AMOUNT_TO_REFUEL=tuple(data["MEMEBRIDGE"]["AMOUNT_TO_REFUEL"]),
                MINIMUM_BALANCE_TO_REFUEL=data["MEMEBRIDGE"][
                    "MINIMUM_BALANCE_TO_REFUEL"
                ],
                WAIT_FOR_FUNDS_TO_ARRIVE=data["MEMEBRIDGE"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
                MAX_WAIT_TIME=data["MEMEBRIDGE"]["MAX_WAIT_TIME"],
                BRIDGE_ALL=data["MEMEBRIDGE"]["BRIDGE_ALL"],
                BRIDGE_ALL_MAX_AMOUNT=data["MEMEBRIDGE"]["BRIDGE_ALL_MAX_AMOUNT"],
            ),
            TESTNET_BRIDGE=TestnetBridgeConfig(
                NETWORKS_TO_REFUEL_FROM=data["TESTNET_BRIDGE"][
                    "NETWORKS_TO_REFUEL_FROM"
                ],
                AMOUNT_TO_REFUEL=tuple(data["TESTNET_BRIDGE"]["AMOUNT_TO_REFUEL"]),
                MINIMUM_BALANCE_TO_REFUEL=data["TESTNET_BRIDGE"][
                    "MINIMUM_BALANCE_TO_REFUEL"
                ],
                WAIT_FOR_FUNDS_TO_ARRIVE=data["TESTNET_BRIDGE"][
                    "WAIT_FOR_FUNDS_TO_ARRIVE"
                ],
                MAX_WAIT_TIME=data["TESTNET_BRIDGE"]["MAX_WAIT_TIME"],
            ),
            SHMONAD=ShmonadConfig(
                PERCENT_OF_BALANCE_TO_SWAP=tuple(
                    data["SHMONAD"]["PERCENT_OF_BALANCE_TO_SWAP"]
                ),
                BUY_AND_STAKE_SHMON=data["SHMONAD"]["BUY_AND_STAKE_SHMON"],
                UNSTAKE_AND_SELL_SHMON=data["SHMONAD"]["UNSTAKE_AND_SELL_SHMON"],
            ),
            ACCOUNTABLE=AccountableConfig(
                NFT_PER_ACCOUNT_LIMIT=data["ACCOUNTABLE"]["NFT_PER_ACCOUNT_LIMIT"],
            ),
            ORBITER=OrbiterConfig(
                AMOUNT_TO_BRIDGE=tuple(data["ORBITER"]["AMOUNT_TO_BRIDGE"]),
                BRIDGE_ALL=data["ORBITER"]["BRIDGE_ALL"],
                WAIT_FOR_FUNDS_TO_ARRIVE=data["ORBITER"]["WAIT_FOR_FUNDS_TO_ARRIVE"],
                MAX_WAIT_TIME=data["ORBITER"]["MAX_WAIT_TIME"],
            ),
            DISPERSE=DisperseConfig(
                MIN_BALANCE_FOR_DISPERSE=tuple(
                    data["DISPERSE"]["MIN_BALANCE_FOR_DISPERSE"]
                ),
            ),
            LILCHOGSTARS=LilchogstarsConfig(
                MAX_AMOUNT_FOR_EACH_ACCOUNT=tuple(
                    data["LILCHOGSTARS"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"]
                ),
            ),
            DEMASK=DemaskConfig(
                MAX_AMOUNT_FOR_EACH_ACCOUNT=tuple(
                    data["DEMASK"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"]
                ),
            ),
            MONADKING=MonadkingConfig(
                MAX_AMOUNT_FOR_EACH_ACCOUNT=tuple(
                    data["MONADKING"]["MAX_AMOUNT_FOR_EACH_ACCOUNT"]
                ),
            ),
            MAGICEDEN=MagicEdenConfig(
                NFT_CONTRACTS=data["MAGICEDEN"]["NFT_CONTRACTS"],
            ),
        )


# 单例模式获取配置
def get_config() -> Config:
    """Get configuration singleton"""
    if not hasattr(get_config, "_config"):
        get_config._config = Config.load()
    return get_config._config
