import os
from rich.console import Console
from rich.text import Text
from tabulate import tabulate
from rich.table import Table
from rich import box
from typing import List
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, Window, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
import questionary
from questionary import Style as QuestionaryStyle
import asyncio
import sys


def show_logo():
    """显示 STARLABS 的标志"""
    # 清除屏幕
    os.system("cls" if os.name == "nt" else "clear")

    console = Console()

    # 创建带有星空效果的样式化标志
    logo_text = """
✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆ ˚   ✦  . ⋆ ˚   ✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆   ˚ ✦  ˚  ✦  . ⋆ ✦ ˚ 
. ⋆ ˚ ✧  . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆  ˚ ✦ .✦ ˚ . 
·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ·˚ ★ ·˚
✧ ⋆｡˚✦ ⋆｡  ███████╗████████╗ █████╗ ██████╗ ██╗      █████╗ ██████╗ ███████╗  ⋆｡ ✦˚⋆｡ 
★ ·˚ ⋆｡˚   ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝  ✦˚⋆｡ ˚· 
⋆｡✧ ⋆ ★    ███████╗   ██║   ███████║██████╔╝██║     ███████║██████╔╝███████╗   ˚· ★ ⋆
˚· ★ ⋆｡    ╚════██║   ██║   ██╔══██║██╔══██╗██║     ██╔══██║██╔══██╗╚════██║   ⋆ ✧｡⋆ 
✧ ⋆｡ ˚·    ███████║   ██║   ██║  ██║██║  ██║███████╗██║  ██║██████╔╝███████║   ★ ·˚ ｡
★ ·˚ ✧     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝   ｡⋆ ✧ 
·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚ ⋆｡⋆｡. ★ ·˚ ⋆｡⋆｡. ★ ·˚ ★ ·˚·˚ ⋆｡⋆｡.
. ⋆ ˚ ✧  . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆ ˚  ✦ ˚ . ⋆  ˚ ✦ . ⋆  ˚ ✦ .. ⋆  ˚ 
✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆ ˚   ✦  . ⋆ ˚   ✦ ˚ . ⋆   ˚ ✦  ˚  ✦  . ⋆   ˚ ✦  ˚  ✦  . ⋆  ✦"""

    # 创建渐变文本
    gradient_logo = Text(logo_text)
    gradient_logo.stylize("bold bright_cyan")

    # 输出带有缩进的文本
    console.print(gradient_logo)
    print()


def show_dev_info():
    """显示开发者信息和版本信息"""
    console = Console()

    # 创建美观的表格
    table = Table(
        show_header=False,
        box=box.DOUBLE,
        border_style="bright_cyan",
        pad_edge=False,
        width=49,
        highlight=True,
    )

    # 添加列
    table.add_column("内容", style="bright_cyan", justify="center")

    # 添加行，包含联系方式
    table.add_row("✨ StarLabs Monad Bot 1.8 ✨")
    table.add_row("─" * 43)
    table.add_row("")
    table.add_row("⚡ GitHub: [link]https://github.com/0xStarLabs[/link]")
    table.add_row("👤 开发者: [link]https://t.me/StarLabsTech[/link]")
    table.add_row("💬 交流群: [link]https://t.me/StarLabsChat[/link]")
    table.add_row("")

    # 输出表格，并添加缩进
    print("   ", end="")
    print()
    console.print(table)
    print()


async def show_menu(title: str, options: List[str]) -> str:
    """
    显示交互式菜单，并返回用户选择的选项。
    """
    try:
        # 添加空行以调整间距
        print("\n")

        # 创建自定义样式，使文本更大
        custom_style = QuestionaryStyle(
            [
                ("question", "fg:#B8860B bold"),  # 标题颜色 - 暗金色
                ("answer", "fg:#ffffff bold"),  # 选中选项颜色 - 白色
                ("pointer", "fg:#B8860B bold"),  # 指针颜色 - 暗金色
                ("highlighted", "fg:#B8860B bold"),  # 高亮选项颜色 - 暗金色
                ("instruction", "fg:#666666"),  # 说明文本颜色 - 灰色
            ]
        )

        print()

        # 显示菜单并应用自定义样式
        result = await questionary.select(
            title,
            choices=options,  # 直接使用 options，因为其中已经包含了表情符号
            style=custom_style,
            qmark="🎯",  # 自定义指示符
            instruction="(使用方向键和回车选择)",
        ).ask_async()

        return result

    except KeyboardInterrupt:
        print("\n\n退出程序... 再见！👋")
        sys.exit(0)