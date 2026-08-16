#!/usr/bin/env python3
"""
图片优化脚本
使用 Pillow 库优化 PNG 和 JPG 图片
"""

from PIL import Image
import os
import sys

def optimize_png(input_path, output_path=None, quality=85):
    """优化 PNG 图片"""
    if output_path is None:
        output_path = input_path

    img = Image.open(input_path)

    # 转换为 RGB 模式（如果是 RGBA，保留 alpha 通道）
    if img.mode in ('RGBA', 'LA'):
        # 保留透明通道
        img.save(output_path, 'PNG', optimize=True, compress_level=9)
    else:
        # 转换为 RGB
        rgb_img = img.convert('RGB')
        rgb_img.save(output_path, 'PNG', optimize=True, compress_level=9)

    # 获取文件大小
    original_size = os.path.getsize(input_path)
    optimized_size = os.path.getsize(output_path)
    saved = original_size - optimized_size
    saved_percent = (saved / original_size) * 100 if original_size > 0 else 0

    print(f"✓ {os.path.basename(input_path)}")
    print(f"  原始: {original_size/1024:.1f}KB → 优化后: {optimized_size/1024:.1f}KB")
    print(f"  节省: {saved/1024:.1f}KB ({saved_percent:.1f}%)")

def optimize_jpg(input_path, output_path=None, quality=85):
    """优化 JPG 图片"""
    if output_path is None:
        output_path = input_path

    img = Image.open(input_path)

    # 转换为 RGB 模式
    rgb_img = img.convert('RGB')
    rgb_img.save(output_path, 'JPEG', quality=quality, optimize=True)

    # 获取文件大小
    original_size = os.path.getsize(input_path)
    optimized_size = os.path.getsize(output_path)
    saved = original_size - optimized_size
    saved_percent = (saved / original_size) * 100 if original_size > 0 else 0

    print(f"✓ {os.path.basename(input_path)}")
    print(f"  原始: {original_size/1024:.1f}KB → 优化后: {optimized_size/1024:.1f}KB")
    print(f"  节省: {saved/1024:.1f}KB ({saved_percent:.1f}%)")

def main():
    assets_dir = 'assets'

    if not os.path.exists(assets_dir):
        print(f"❌ 找不到 {assets_dir} 目录")
        sys.exit(1)

    print("🖼️  开始优化图片...\n")

    # 优化 PNG 文件
    png_files = ['portrait.png', 'nachoneko-sticker.png']
    for png_file in png_files:
        png_path = os.path.join(assets_dir, png_file)
        if os.path.exists(png_path):
            try:
                optimize_png(png_path)
                print()
            except Exception as e:
                print(f"❌ 优化 {png_file} 失败: {e}\n")

    # 优化 JPG 文件
    jpg_files = ['banner.jpg']
    for jpg_file in jpg_files:
        jpg_path = os.path.join(assets_dir, jpg_file)
        if os.path.exists(jpg_path):
            try:
                optimize_jpg(jpg_path, quality=90)
                print()
            except Exception as e:
                print(f"❌ 优化 {jpg_file} 失败: {e}\n")

    print("✅ 图片优化完成！")

if __name__ == '__main__':
    try:
        from PIL import Image
    except ImportError:
        print("❌ 请先安装 Pillow 库:")
        print("   pip install Pillow")
        sys.exit(1)

    main()
