# **Monad 测试网自动化脚本教程**

---
## ⚙️ 安装

### **要求：**

- Python 版本 3.11.6 或更高

### **安装并运行**

```bash
git clone https://github.com/blockchain-src/Monad_Automation.git && cd Monad_Automation
chmod +x run.sh && ./run.sh
```
![image](https://github.com/user-attachments/assets/0d887865-049b-4804-9e11-ffc80ae21ce3)

---

## 📁 数据文件夹

可手动配置以下文件（可选）。

- `discord_tokens.txt` - Discord 账户的 Token（可选，仅在使用官方水龙头功能时需要）。
- `emails.txt` - 电子邮件地址，仅支持 `firstmail.tld` 或 `gmx`，仅在使用 ThirdWeb 水龙头时需要。

## 📝 配置文件（config.yaml）

本节将详细介绍 `config.yaml` 文件中的每个功能。

### **SETTINGS（设置部分）：**

- `THREADS` - 同时执行的账户数量。
- `ACCOUNTS_RANGE` - 设定要操作的账户范围。
    - 默认情况下，机器人会使用文件中的所有账户。
    - 例如，如果只需要操作第 5 到第 10 个账户，则设置为 `ACCOUNTS_RANGE: [5, 10]`。
    - 默认值 `[0, 0]`（使用所有账户）。
- `EXACT_ACCOUNTS_TO_USE` - 指定要操作的账户。
    - 例如，如果只需要操作账户 `1, 3, 5`，则设置为 `EXACT_ACCOUNTS_TO_USE: [1, 3, 5]`。
    - **仅当 `ACCOUNTS_RANGE: [0, 0]` 时，此功能才有效。**
- `PAUSE_BETWEEN_ATTEMPTS` - 发生错误时的重试间隔。
- `PAUSE_BETWEEN_SWAPS` - 交易（如 Ambient、Bean 等）之间的间隔。
- `RANDOM_PAUSE_BETWEEN_ACCOUNTS` - 账户之间的随机间隔。
- `RANDOM_PAUSE_BETWEEN_ACTIONS` - 操作之间的随机间隔（与 `PAUSE_BETWEEN_ATTEMPTS` 类似）。
- `RANDOM_INITIALIZATION_PAUSE` - 启动账户前的延迟，以防止所有账户同时开始操作。
- `BROWSER_PAUSE_MULTIPLIER` - 使用浏览器时的暂停时间倍数。
    - 如果遇到错误，可以增加此值（如 2、3、4 等）。

### **FLOW（流程部分）：**

- `TASKS` - **此字段用于配置所有功能**，是最重要的字段。
    - 所有可用功能的列表会在 `TASKS` 字段上方进行更新。
    - 例如：
    
    该示例将执行 **Magma 质押 MON 代币、Owlto 部署合约、Bima 借贷和水龙头** 三项任务。
    
    ```yaml
    TASKS: ["magma", "owlto", "bima"]
    ```
    
    - 如果希望某些功能随机执行，可以将它们放入方括号中，例如：
    
    上述示例会执行 **logs 功能**，然后从 `swaps`、`ambient` 和 `bean` 中随机执行一个，最后执行 **连接 Discord** 功能。
    
    ```yaml
    TASKS: ["logs", ["swaps", "ambient", "bean"], "connect_discord"]
    ```
    
    - **可以随意设置随机功能的数量及其顺序。**
- `NUMBER_OF_SWAPS` - 交易（Swaps）功能的交易次数，适用于所有交易所。
- `PERCENT_OF_BALANCE_TO_SWAP` - 交易时用于交换的余额百分比。

### **FAUCET（水龙头功能）：**

- `THIRDWEB: true/false` - 是否使用 ThirdWeb 网站水龙头（需要电子邮件并打开浏览器）。
- `MONAD_XYZ: true/false` - 是否使用 MonadXYZ 官方水龙头。
    - 使用官方水龙头时，需要填写以下字段：
    - `CAPSOLVER_API_KEY` - `capsolver.com` 的 API 密钥，仅用于水龙头。
    - `PROXY_FOR_CAPTCHA` - 用于验证码解决的代理，格式：`user:pass@ip:port`。

### **GASZIP（Gas 充值功能）：**

- `NETWORKS_TO_REFUEL_FROM` - 选择用于充值的网络。
    - 可选网络：`Arbitrum`、`Base`、`Optimism`。
- `AMOUNT_TO_REFUEL` - 用多少 ETH 购买代币。
- `MINIMUM_BALANCE_TO_REFUEL` - 如果测试网络的余额低于设定值，则执行充值。

## 💁‍♀️ **支持**
- **Telegram 技术支持群**: [点击加入](https://t.me/StarLabsTech)  
- **Telegram 交流群**: [点击加入](https://t.me/StarLabsChat)