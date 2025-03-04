### Monad 测试网自动化脚本概述

该脚本用于自动化与 Monad 测试网的交互，包括各种 DeFi 操作和代币交互。

---

## 所有功能均可在配置文件中启用：

### **水龙头（FAUCETS）**
- `"faucet"` - 从水龙头获取代币  
- `"farm_faucet"` - 从水龙头获取代币（针对农场账户 `data/keys_for_faucet.txt`）  
- `"disperse_farm_accounts"` - 将农场账户的代币分发到主账户 | `keys_for_faucet.txt -> private_keys.txt`  
- `"disperse_from_one_wallet"` - 从单个钱包向所有其他钱包分发代币 | `keys_for_faucet.txt`（第一个钱包） -> `private_keys.txt`  

### **代币交换（SWAPS）**
- `"collect_all_to_monad"` - 将所有代币兑换为 Monad 原生代币（MON）  
- `"swaps"` - 在 [testnet.monad.xyz](https://testnet.monad.xyz) 页面进行代币交换  
- `"bean"` - 在 **Bean DEX** 进行代币交换  
- `"ambient"` - 在 **Ambient DEX** 进行代币交换  
- `"izumi"` - 在 **Izumi DEX** 进行代币交换  

### **质押（STAKES）**
- `"apriori"` - 质押 MON 代币  
- `"magma"` - 在 **Magma** 质押 MON 代币  
- `"shmonad"` - 在 **shmonad.xyz** 购买并质押 shmon 代币 | **查看下方设置**  
- `"kintsu"` - 在 **kintsu.xyz** 质押 MON 代币  

### **铸造 NFT（MINT）**
- `"magiceden"` - 在 **magiceden.io** 铸造 NFT  
- `"accountable"` - 铸造 **accountable NFT**  
- `"owlto"` - 在 **Owlto** 部署合约  
- `"lilchogstars"` - 在 **testnet.lilchogstars.com** 铸造 NFT  
- `"demask"` - 在 **app.demask.finance/launchpad** 铸造 NFT  
- `"monadking"` - 在 **nerzo.xyz/monadking** 铸造 NFT  
- `"monadking_unlocked"` - 在 **www.nerzo.xyz/unlocked** 铸造 NFT  

### **Gas 费用补充（REFUEL）**
- `"gaszip"` - 通过 **Arbitrum、Optimism、Base** 补充 Monad Gas  
- `"orbiter"` - 通过 **Orbiter** 桥接 **Sepolia** 的 ETH 至 Monad  
- `"memebridge"` - 通过 **Arbitrum、Optimism、Base** 补充 Monad Gas  

### **其他（OTHER）**
- `"logs"` - 显示日志信息：MON 余额 | 交易数量 | 平均余额 | 平均交易数量  
- `"nad_domains"` - 在 **nad.domains** 注册随机域名  
- `"aircraft"` - 在 **aircraft.fun** 铸造 NFT  

---

## **环境要求**
- 需要 **Python 3.11** 或更高版本  

## **安装并运行**

```bash
git clone https://github.com/blockchain-src/Monad_Automation.git && cd Monad_Automation
chmod +x run.sh && ./run.sh
```
![image](https://github.com/user-attachments/assets/0d887865-049b-4804-9e11-ffc80ae21ce3)

---

## **支持**
- **Telegram 技术支持群**: [点击加入](https://t.me/StarLabsTech)  
- **Telegram 交流群**: [点击加入](https://t.me/StarLabsChat)