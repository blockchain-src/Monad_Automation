# 🚀 **Monad 测试网自动化脚本教程**

---

## ⚙️ **安装**

### 🔆 **环境要求**
  📌 **Python** 版本 **3.11.6** 或更高  

### 🛠 **安装/运行**
```bash
git clone https://github.com/blockchain-src/Monad_Automation.git && cd Monad_Automation
chmod +x run.sh && ./run.sh
```
![image](https://github.com/user-attachments/assets/0d887865-049b-4804-9e11-ffc80ae21ce3)

---
## 🎗️ **配置钱包和代理**
> **在终端完成对 `private_keys.txt` 和 `proxies.txt` 的配置。**
- 🗝️ ** `private_keys.txt` ** — 钱包的私钥，每行一个私钥。
- 🛡️ ** `proxies.txt` ** — 代理，每行一个代理。
  - 如果代理数量少于账户数量，则会重复使用代理以满足所有账户的需求。这可能会被识别为**`女巫`**行为。
  - **代理格式**： `用户名:密码@IP地址:端口` 。仅支持 HTTP 代理。
  - **示例**：
    
    如果你的代理服务器信息如下：

    `代理服务器 IP：192.168.1.100 | 端口：8080 | 用户名：user1 | 密码：proxypass`

    那么，你应该配置如下：
    ```bash
    user1:proxypass@192.168.1.100:8080
    ```
  - **如何获得代理 IP & 端口？**

    - 购买代理（如 BrightData、SmartProxy）
    - 在 VPS 上搭建一个 SOCKS5 代理（可以使用 danted 服务器）
    - VPN 提供的代理（部分 VPN 提供 SOCKS5 代理）
    - Tor 网络代理（默认监听 127.0.0.1:9050）
---

## 📁 **数据文件夹**
> **可手动配置以下文件（可选）：**
- 📜 **`discord_tokens.txt`** — Discord 账户的 Token（仅在使用官方水龙头功能时需要）。  
- 📧 **`emails.txt`** — 电子邮件地址（仅支持 `firstmail.tld` 或 `gmx`，用于 ThirdWeb 水龙头）。  

---

## 📝 **配置文件（config.yaml）**
> 本节将详细介绍 `config.yaml` 文件中的各项配置。

### 🔧 **SETTINGS（设置部分）**
- `THREADS` — **同时执行的账户数量**。  
- `ACCOUNTS_RANGE` — **设定要操作的账户范围**：
  - 默认情况下，机器人会使用文件中的所有账户。
  - **示例**：仅操作第 `5` 到 `10` 个账户：
    ```yaml
    ACCOUNTS_RANGE: [5, 10]
    ```
  - 默认值为 `[0, 0]`（即使用所有账户）。  
- `EXACT_ACCOUNTS_TO_USE` — **指定要操作的账户**：
  - **示例**：仅操作账户 `1, 3, 5`：
    ```yaml
    EXACT_ACCOUNTS_TO_USE: [1, 3, 5]
    ```
  - **⚠️ 仅当 `ACCOUNTS_RANGE: [0, 0]` 时有效。**  
- `PAUSE_BETWEEN_ATTEMPTS` — **错误重试间隔**。  
- `PAUSE_BETWEEN_SWAPS` — **交易间隔（如 Ambient、Bean 等）**。  
- `RANDOM_PAUSE_BETWEEN_ACCOUNTS` — **账户之间的随机间隔**。  
- `RANDOM_PAUSE_BETWEEN_ACTIONS` — **操作之间的随机间隔**（类似于 `PAUSE_BETWEEN_ATTEMPTS`）。  
- `RANDOM_INITIALIZATION_PAUSE` — **启动账户前的延迟**，避免所有账户同时开始操作。  
- `BROWSER_PAUSE_MULTIPLIER` — **浏览器操作的暂停时间倍数**（如 `2、3、4`，可增大以减少错误）。  

---

### 🔄 **FLOW（流程部分）**
> `TASKS` 是最重要的字段，用于配置所有功能。  
> **可用功能列表将在 `TASKS` 字段上方更新。**

- **示例 1：执行 `Magma 质押 MON`、`Owlto 部署合约` 和 `Bima 借贷`**
    ```yaml
    TASKS: ["magma", "owlto", "bima"]
    ```
- **示例 2：执行 `logs`，然后在 `swaps`、`ambient` 和 `bean` 之间随机选一个，最后执行 `connect_discord`**
    ```yaml
    TASKS: ["logs", ["swaps", "ambient", "bean"], "connect_discord"]
    ```
  - **✅ 可自由组合随机功能的数量及顺序。**  

🔹 `NUMBER_OF_SWAPS` — **交易次数**（适用于所有交易所）。  
🔹 `PERCENT_OF_BALANCE_TO_SWAP` — **交易时用于交换的余额百分比**。  

---

### 💧 **FAUCET（水龙头功能）**
- `THIRDWEB: true/false` — **是否使用 ThirdWeb 水龙头**（需 **电子邮件** + **打开浏览器**）。  
- `MONAD_XYZ: true/false` — **是否使用 MonadXYZ 官方水龙头**（需 API 及代理）。  
  - `CAPSOLVER_API_KEY` — **`capsolver.com` API 密钥**（用于验证码解决）。  
  - `PROXY_FOR_CAPTCHA` — **用于验证码解决的代理**（格式：`user:pass@ip:port`）。  

---

### ⛽ **GASZIP（Gas 充值功能）**
- `NETWORKS_TO_REFUEL_FROM` — **选择用于充值的网络**：
  - 可选：`Arbitrum`、`Base`、`Optimism`  
- `AMOUNT_TO_REFUEL` — **充值所用 ETH 数量**。  
- `MINIMUM_BALANCE_TO_REFUEL` — **当余额低于设定值时，自动充值**。  

---

## 💁‍♂️ **支持**
📢 **Telegram 技术支持群** 👉 [点击加入](https://t.me/StarLabsTech)  
💬 **Telegram 交流群** 👉 [点击加入](https://t.me/StarLabsChat)