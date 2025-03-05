# 🚀 **Monad 测试网自动化脚本教程**  

## ⚙️ **安装**  

### 🔆 **环境要求**  
- **Python** 版本 **3.11.6** 或更高  

### 🛠 **安装 & 运行** 
- **⚫ 首次安装并运行**
```bash
git clone https://github.com/blockchain-src/Monad_Automation.git && cd Monad_Automation
chmod +x run.sh && ./run.sh
```

- **⚫ 非首次运行**  

进入项目目录，执行以下命令
```bash
source venv/bin/activate && python3 main.py
```
![image](https://github.com/user-attachments/assets/0d887865-049b-4804-9e11-ffc80ae21ce3)  
---

## 🎗️ **配置钱包 & 代理**  
📌 **在终端配置 `private_keys.txt` 和 `proxies.txt`**  

### 🔑 **输入私钥（配置`private_keys.txt`）**  
- **每行一个私钥**，示例如下：
  ```bash
  0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
  0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
  ```
- **如何获取私钥？**  
  - 通过 **MetaMask** 或 **OKX_web3钱包** 导出  
  - 使用 **助记词转换工具**（如 `ethers.js`）获取私钥  

### 🛡️ **输入代理（配置`proxies.txt`）**  
- **格式**：`用户名:密码@IP:端口`（仅支持 HTTP 代理）  
- **每行一个代理**，示例如下：
  ```bash
  user1:proxypass@192.168.1.100:8080
  user2:proxypass@192.168.1.101:8080
  user3:proxypass@192.168.1.102:8080
  ```
- **代理配置数量最好与私钥相同，如果代理不足会重复使用，可能会导致“女巫”行为**  

- **代理来源推荐**：  
  - **购买代理**（如 BrightData、SmartProxy）  
  - **自建代理**（在 VPS 上搭建 SOCKS5，如 `danted`）  
  - **VPN 提供的 SOCKS5 代理**  
  - **Tor 网络代理**（默认监听 `127.0.0.1:9050`）  

---

## 📁 **数据文件（可选）**  
📌 **手动配置以下文件（如有需求）：**  
- 📜 **`discord_tokens.txt`** — **Discord 账户 Token**（用于官方水龙头）  
- 📧 **`emails.txt`** — **电子邮件**（支持 `firstmail.tld` 或 `gmx`，用于 ThirdWeb 水龙头）  

---

## 📝 **配置文件 `config.yaml`**  
📌 **核心参数说明**  

### 🔧 **SETTINGS（基础设置）**  
- `THREADS` — **同时执行的账户数**  
- `ACCOUNTS_RANGE` — **操作账户范围**（默认 `[0, 0]` 代表全部）  
  ```yaml
  ACCOUNTS_RANGE: [5, 10]  # 仅操作第 5 到 10 个账户
  ```
- `EXACT_ACCOUNTS_TO_USE` — **指定具体账户**（需 `ACCOUNTS_RANGE: [0, 0]`）  
  ```yaml
  EXACT_ACCOUNTS_TO_USE: [1, 3, 5]  # 仅操作账户 1, 3, 5
  ```
- `PAUSE_BETWEEN_ATTEMPTS` — **错误重试间隔**  
- `PAUSE_BETWEEN_SWAPS` — **交易间隔**（适用于 Ambient、Bean 等）  
- `RANDOM_PAUSE_BETWEEN_ACCOUNTS` — **账户之间的随机间隔**  
- `RANDOM_PAUSE_BETWEEN_ACTIONS` — **操作间隔（类似 `PAUSE_BETWEEN_ATTEMPTS`）**  
- `RANDOM_INITIALIZATION_PAUSE` — **启动账户的随机延迟**（避免所有账户同时操作）  
- `BROWSER_PAUSE_MULTIPLIER` — **浏览器暂停时间倍数**（如 `2、3、4`）  

---

### 🔄 **FLOW（功能流程）**  
📌 **核心字段：`TASKS`**  
- **示例 1**：执行 `Magma 质押 MON`、`Owlto 部署合约` 和 `Bima 借贷`  
  ```yaml
  TASKS: ["magma", "owlto", "bima"]
  ```
- **示例 2**：执行 `logs`，然后随机选 `swaps`、`ambient` 或 `bean`，最后执行 `connect_discord`  
  ```yaml
  TASKS: ["logs", ["swaps", "ambient", "bean"], "connect_discord"]
  ```
✅ **任务支持自由组合 & 随机执行**  

📌 **交易相关参数**  
- `NUMBER_OF_SWAPS` — **交易次数**  
- `PERCENT_OF_BALANCE_TO_SWAP` — **交易金额占比**  

---

### 💧 **FAUCET（水龙头功能）**  
- `THIRDWEB: true/false` — **是否使用 ThirdWeb 水龙头**（需邮箱 & 浏览器）  
- `MONAD_XYZ: true/false` — **是否使用 MonadXYZ 官方水龙头**（需 API & 代理）  
  - `CAPSOLVER_API_KEY` — **验证码 API 密钥（capsolver.com）**  
  - `PROXY_FOR_CAPTCHA` — **验证码解决代理（格式：`user:pass@ip:port`）**  

---

### ⛽ **GASZIP（Gas 充值）**  
📌 **低余额时自动充值**  
- `NETWORKS_TO_REFUEL_FROM` — **充值网络**（`Arbitrum`、`Base`、`Optimism`）  
- `AMOUNT_TO_REFUEL` — **充值 ETH 数量**  
- `MINIMUM_BALANCE_TO_REFUEL` — **低于此值自动充值**  

---

## 💁‍♂️ **支持**  
📢 **技术支持群** 👉 [点击加入](https://t.me/StarLabsTech)  
💬 **用户交流群** 👉 [点击加入](https://t.me/StarLabsChat)  
