#!/usr/bin/env python3
"""
将桌面端 SVG 打字动画转换为 GIF
需要安装: pip install selenium pillow
需要浏览器驱动: Chrome/Firefox
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io

def create_typing_gif():
    """录制 SVG 动画并转换为 GIF"""

    print("🎬 开始录制打字动画...")

    # 设置 Chrome 无头模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=760,64')
    chrome_options.add_argument('--disable-gpu')

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        print("❌ 找不到 Chrome，尝试使用 Firefox...")
        driver = webdriver.Firefox()
        driver.set_window_size(760, 64)

    # 创建临时 HTML 文件
    html_path = os.path.abspath('temp_animation.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 0; background: transparent; }
        img { display: block; width: 760px; height: 64px; }
    </style>
</head>
<body>
    <img src="assets/typing-banner.svg" alt="typing">
</body>
</html>
        ''')

    driver.get(f'file://{html_path}')
    time.sleep(1)  # 等待加载

    frames = []
    frame_duration = 100  # 每帧 100ms
    total_duration = 8000  # 录制前 8 秒（两个句子）
    num_frames = total_duration // frame_duration

    print(f"📸 录制 {num_frames} 帧...")

    for i in range(num_frames):
        # 截图
        screenshot = driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(screenshot))

        # 裁剪到正确尺寸
        img = img.crop((0, 0, 760, 64))
        frames.append(img)

        if (i + 1) % 10 == 0:
            print(f"  已录制 {i + 1}/{num_frames} 帧")

        time.sleep(frame_duration / 1000.0)

    driver.quit()
    os.remove(html_path)

    print("💾 保存为 GIF...")

    # 保存为 GIF
    output_path = 'assets/typing-banner-mobile.gif'
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,
        optimize=True
    )

    file_size = os.path.getsize(output_path) / 1024
    print(f"✅ 完成! 文件大小: {file_size:.1f} KB")
    print(f"📁 保存位置: {output_path}")

    return output_path

if __name__ == '__main__':
    try:
        create_typing_gif()
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n请确保已安装:")
        print("  pip install selenium pillow")
        print("  并且安装了 Chrome 或 Firefox 浏览器")
