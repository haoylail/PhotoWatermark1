# 图片水印命令行工具

## 项目简介
图片水印命令行工具是一款基于 Python 的实用工具，能够为图片添加基于 EXIF 信息的水印。用户可以通过命令行指定图片路径、字体大小、颜色以及水印位置，程序会自动处理图片并将带有水印的图片保存到新目录中。

### 功能特点
- 支持单张图片和批量图片处理。
- 自动提取图片 EXIF 信息中的拍摄日期作为水印内容。
- 用户可自定义水印的字体大小、颜色和位置。
- 处理后的图片保存在原目录的子目录中，确保原图片不被覆盖。
- 当图片缺少 EXIF 信息时，使用当前日期作为水印内容。

---

## 使用方法

### 环境准备
1. 确保已安装 Python 3.6 或更高版本。
2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```

### 命令行参数
运行程序时，可通过以下参数进行配置：
- `path` (必填): 图片文件路径或包含图片的目录路径。
- `--font-size` (可选): 水印字体大小，默认值为 20。
- `--font-color` (可选): 水印字体颜色，默认值为黑色。
- `--position` (可选): 水印位置，可选值为 `top-left`、`center`、`bottom-right`，默认值为 `bottom-right`。

### 示例

#### 单张图片处理
运行以下命令为单张图片添加水印：
```bash
python src/main.py tests/test.jpg --font-size 30 --font-color red --position center
```

#### 批量图片处理
运行以下命令为目录中的所有图片添加水印：
```bash
python src/main.py tests/ --font-size 25 --font-color blue --position top-left
```

### 输出
- 处理后的图片将保存在输入目录的子目录中，命名为 `<原目录名>_watermark`。
- 示例：如果输入路径为 `tests/test.jpg`，处理后的图片将保存在 `tests/test.jpg_watermark/` 中。

---

## 注意事项
- 确保输入的图片包含有效的 EXIF 数据以提取拍摄日期；否则，程序将使用当前日期作为水印内容。
- 字体文件 `arial.ttf` 必须存在于系统中，或根据需要修改代码以指定其他字体文件。

---

## 许可证
本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。