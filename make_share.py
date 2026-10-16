#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键打包「分享版」：
  生成 分享版/汐汐小桌宠/ （只含运行必需文件 + 通用启动器 + 使用说明）
  并压缩为 汐汐小桌宠-分享版.zip

用法：python make_share.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE_ROOT = os.path.join(HERE, "分享版")
SHARE = os.path.join(SHARE_ROOT, "汐汐小桌宠")
ZIP_BASE = os.path.join(HERE, "汐汐小桌宠-分享版")

# 通用启动器（GBK 编码，中文 Windows 的 cmd 下正常显示）
BAT = r'''@echo off
cd /d %~dp0
title 汐汐小桌宠
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo   [需要先安装 Python]
    echo   请打开 https://www.python.org/downloads/ 下载安装 Python 3.8 以上版本，
    echo   安装时务必勾选 "Add Python to PATH"，装好后重新双击本文件。
    echo.
    pause
    exit /b 1
)
python -c "import PyQt5, numpy, pygame" >nul 2>nul
if errorlevel 1 (
    echo.
    echo   首次运行，正在自动安装依赖（需要联网，约 1-2 分钟）...
    echo.
    python -m pip install PyQt5 numpy pygame
    if errorlevel 1 (
        echo.
        echo   依赖安装失败，请检查网络后重试。
        pause
        exit /b 1
    )
)
python pet_qt.py
if errorlevel 1 pause
'''

README = '''汐汐小桌宠 · 使用说明
==============================

【第一次使用】
1. 电脑需要安装 Python 3.8 以上版本
   下载：https://www.python.org/downloads/
   安装时务必勾选 "Add Python to PATH"
2. 双击「启动桌宠.bat」
   首次运行会自动安装依赖（需联网，约 1-2 分钟）
3. 之后汐汐会出现在屏幕右下角

【玩法】
- 按住脑袋 rua 头 / 按住身体拖动 / 滚轮放大缩小
- 底部按钮：摸摸头、投喂、聊聊、🔊 音效、中/日 语音切换
- 右键汐汐：弹出语音菜单，点哪条她念哪条
- 聊天里带"对吗"，她会回答"对的对的 / 不对不对"
- 点右侧小叉让她休息，再点"唤回汐汐"叫她回来

【发给别人 / 换电脑】
把整个「汐汐小桌宠」文件夹打包发过去，
对方装好 Python 后双击「启动桌宠.bat」即可，无需其他配置。

【文件说明】
pet_qt.py        主程序
xixi.png         人物图（透明背景）
xixi_sad.png     难过状态的去饱和图
voice/           汐汐语音（中/日 各 13 段）
启动桌宠.bat     双击启动
使用说明.txt     本文件

【版权】
人物与语音版权归《卡拉彼丘》(Strinova) 原作所有，
仅供个人学习娱乐使用，请勿商用。
'''


def main():
    if os.path.exists(SHARE_ROOT):
        shutil.rmtree(SHARE_ROOT)
    os.makedirs(SHARE)

    # 必需文件
    for name in ("pet_qt.py", "xixi.png", "xixi_sad.png"):
        shutil.copy(os.path.join(HERE, name), os.path.join(SHARE, name))

    # 语音
    os.makedirs(os.path.join(SHARE, "voice", "wav", "cn"))
    os.makedirs(os.path.join(SHARE, "voice", "wav", "jp"))
    for lang in ("cn", "jp"):
        src = os.path.join(HERE, "voice", "wav", lang)
        dst = os.path.join(SHARE, "voice", "wav", lang)
        for f in os.listdir(src):
            shutil.copy(os.path.join(src, f), os.path.join(dst, f))
    shutil.copy(os.path.join(HERE, "voice", "manifest.json"),
                os.path.join(SHARE, "voice", "manifest.json"))

    # 启动器与说明
    with open(os.path.join(SHARE, "启动桌宠.bat"), "w", encoding="gbk", errors="replace") as f:
        f.write(BAT)
    with open(os.path.join(SHARE, "使用说明.txt"), "w", encoding="utf-8-sig") as f:
        f.write(README)

    # 压缩
    zip_path = shutil.make_archive(ZIP_BASE, "zip", SHARE_ROOT, "汐汐小桌宠")
    size = os.path.getsize(zip_path) / 1048576
    print("分享包已生成：%s （%.1f MB）" % (zip_path, size))


if __name__ == "__main__":
    main()
