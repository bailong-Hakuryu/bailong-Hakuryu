# 创建移动端 GIF 动画 - 手动步骤

## 方法 1：在线工具（最简单）

### 步骤 1：录制屏幕
1. 打开你的 GitHub 主页（桌面端）
2. 使用屏幕录制工具录制打字动画区域（约 10 秒）
   - Windows: Win + G（Xbox Game Bar）
   - Mac: Cmd + Shift + 5
   - 或使用 OBS Studio

### 步骤 2：转换为 GIF
访问以下任一网站：
- https://ezgif.com/video-to-gif （推荐）
- https://cloudconvert.com/mp4-to-gif
- https://www.iloveimg.com/video-to-gif

设置：
- 宽度：420px（移动端尺寸）
- 帧率：10 FPS
- 优化：启用
- 循环：无限循环

### 步骤 3：放置文件
1. 保存为 `assets/typing-banner-mobile.gif`
2. 提交到 Git

---

## 方法 2：使用自动化脚本

### 前提条件
```bash
pip install selenium pillow
```

### 运行脚本
```bash
python create_mobile_gif.py
```

脚本会自动：
- 在浏览器中打开 SVG
- 录制 8 秒动画
- 转换为优化的 GIF
- 保存到 `assets/typing-banner-mobile.gif`

---

## 方法 3：使用 FFmpeg（高质量）

### 安装 FFmpeg
- Windows: `choco install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `apt install ffmpeg`

### 步骤
1. 先录制视频（使用屏幕录制）
2. 转换为 GIF：

```bash
ffmpeg -i input.mp4 \
  -vf "fps=10,scale=420:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -loop 0 \
  assets/typing-banner-mobile.gif
```

---

## 方法 4：使用 Playwright（推荐给开发者）

创建 `record-animation.js`：

```javascript
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 420, height: 88 }
  });

  await page.goto('file://' + __dirname + '/test-animation.html');
  
  // 创建临时 HTML
  const html = `
    <!DOCTYPE html>
    <html>
    <body style="margin:0;background:#0d1117;">
      <img src="assets/typing-banner.svg" width="420">
    </body>
    </html>
  `;
  
  fs.writeFileSync('test-animation.html', html);
  await page.goto('file://' + __dirname + '/test-animation.html');
  
  const frames = [];
  for (let i = 0; i < 80; i++) {
    const screenshot = await page.screenshot();
    frames.push(screenshot);
    await page.waitForTimeout(100);
  }
  
  await browser.close();
  
  // 使用 gifencoder 将帧转换为 GIF
  console.log('已录制 80 帧，请使用 gifencoder 或其他工具合成');
})();
```

---

## 完成后

### 更新 README.md
```html
<picture>
  <source media="(max-width: 600px)" srcset="./assets/typing-banner-mobile.gif"/>
  <img src="./assets/typing-banner.svg" alt="白龙的动态打字介绍" width="760" loading="lazy"/>
</picture>
```

### 提交
```bash
git add assets/typing-banner-mobile.gif README.md
git commit -m "Add GIF animation for mobile devices"
git push
```

---

## 预期文件大小

- 未优化：800KB - 2MB
- 优化后：200KB - 500KB
- 使用 WebP（推荐）：100KB - 200KB

## WebP 替代方案（更小）

如果 GIF 太大，可以使用 WebP 格式：

```html
<picture>
  <source media="(max-width: 600px)" type="image/webp" srcset="./assets/typing-banner-mobile.webp"/>
  <source media="(max-width: 600px)" srcset="./assets/typing-banner-mobile.gif"/>
  <img src="./assets/typing-banner.svg" alt="白龙的动态打字介绍" width="760" loading="lazy"/>
</picture>
```

转换命令：
```bash
ffmpeg -i typing-banner-mobile.gif -c:v libwebp -quality 85 typing-banner-mobile.webp
```

---

## 需要帮助？

如果遇到问题，可以：
1. 发送你录制的视频给我
2. 我帮你转换为 GIF
3. 或者我们一起调试脚本
