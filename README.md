# png2jpg-ai-image-metadata

[日本語](#日本語) | [English](#english)

# 日本語

# 説明

## 1. Automatic1111 生成画像の変換について

- Automatic1111 に入力可能なメタデータを維持したまま PNG を JPEG に変換します。
- 元画像のメタデータ（PNG Info）は JPEG 画像の Exif に格納されます。
- JPEG 画像は元画像同様に Automatic1111 の PNG Info に読み込ませることが可能です。
- 他生成 AI 入力用のダミー png(数 kB 程度)を追加で出力することができます。JPEG に変換すると他の生成 AI（ComfyUI 等）に入力できなくなりますが、ダミー png を出力することで対応できます。初期設定はオンになっています（変更可）。

## 2. NovelAI 生成画像の変換について

- 元画像のメタデータ（PNG Info）は JPEG 画像の Exif に格納されます。
- NovelAI（及び Automatic1111）入力用のダミー png(数 kB 程度)を追加で出力することができます。JPEG に変換すると他の生成 NovelAI（及び Automatic1111）に入力できなくなりますが、ダミー png を出力することで対応できます。初期設定はオンになっています（変更可）。

## 3. CompyUI 生成画像の変換について

- 元画像のメタデータ（PNG Info）は JPEG 画像の Exif に格納されます。
- Workflow 入力用の json を追加で出力することができます。JPEG に変換すると ComfyUI に入力できなくなりますが、json を出力することで対応できます。初期設定はオンになっています（変更可）。

## 4. 日付情報について

元画像の日付情報を変換後の画像に引き継ぎます。

- Windows: 更新日時, 作成日時
- Mac, Linux: 更新日時
  <br><br>

# オプションの変更

png2jpg.py 内の Config より変更可能です。

```
# ========= Config start / 設定ここから =========
# ディレクトリ / Directories
INPUT_DIR = 'inputs/'
OUTPUT_DIR = 'outputs/'

# JPEG品質 (0-100) / JPEG quality (0-100)
QUALITY = 80

# 出力画像拡張子（'jpg', 'jpeg', 'JPG', 'JPEG'）/ Output image file extension ('jpg', 'jpeg', 'JPG', 'JPEG')
IMG_OUTPUT_FILENAME_EXT = 'jpg'

# A1111画像の追加設定 / Additional settings for A1111 images
# 他生成AI用のダミーpngを出力 / Output a dummy PNG file for other generation AIs
# True / False
A1111_METADATA_PNG = True

# NovelAI画像の追加設定 / Additional settings for NovelAI images
# NovelAI（及びA1111）入力用のダミーpngを出力 / Output a dummy PNG file for NovelAI (and A1111) input
# True / False
NOVELAI_METADATA_PNG = True

# CompyUI画像の追加設定 / Additional settings for CompyUI images
# ワークフロー入力用のjsonを出力 / Output a JSON file for Workflow input
# True / False
COMPYUI_WORKFLOW_JSON = True
# ========= Config end / 設定ここまで ==========
```

# 前提

Python3 環境
<br><br>

# 準備

以下のライブラリを使用するため、入っていない場合はインストールします。

- PIL

```
pip install pillow
```

- piexif

```
pip install piexif
```

Windows のみ

- pywin32

```
pip install pywin32
```

<br>

# 使い方

1. inputs フォルダに変換したい PNG 画像を入れます。
2. Windows の場合は png2jpg.bat をダブルクリックします。Mac, Linux 等の場合はターミナルから png2jpg.py を実行します。
3. outputs フォルダに JPEG 画像が保存されます。
   <br><br>

# 設定変更等

- Windows の bat ファイル起動でエラーの確認や変換状況を確認するために、処理完了後にコマンドラインを閉じないようにしたい場合は png2jpg.bat 内の@REM pause のコメントアウトを外してください。
  <br><br>

# 変更履歴

## [1.0.0] - 2024-06-12

### 追加

- 初回リリース
  <br><br>

# ライセンス

Copyright © 2024 Takenoko  
Released under the [MIT License](https://opensource.org/licenses/mit-license.php).
<br><br><br>

# English

Here is the English translation of the content, with markdown formatting preserved:

# Description

## 1. About Converting Automatic1111 Generated Images

- Converts PNG to JPEG while preserving the metadata that can be entered into Automatic1111.
- The metadata (PNG Info) of the original image is stored in the Exif of the JPEG image.
- The JPEG image can be loaded into Automatic1111's PNG Info, just like the original image.
- You can additionally output a dummy png (a few kB) for input into other generative AIs. If you convert to JPEG, you won't be able to input it into other generative AIs (such as ComfyUI), but outputting a dummy png can address this issue. The default setting is on (changeable).

## 2. About Converting NovelAI Generated Images

- The metadata (PNG Info) of the original image is stored in the Exif of the JPEG image.
- You can additionally output a dummy png (a few kB) for input into NovelAI (and Automatic1111). If you convert to JPEG, you won't be able to input it into NovelAI (and Automatic1111), but outputting a dummy png can address this issue. The default setting is on (changeable).

## 3. About Converting CompyUI Generated Images

- The metadata (PNG Info) of the original image is stored in the Exif of the JPEG image.
- You can additionally output a json file for Workflow input. If you convert to JPEG, you won't be able to input it into ComfyUI, but outputting a json file can address this issue. The default setting is on (changeable).

## 4. About Date Information

The date information of the original image is carried over to the converted image.

- Windows: Last Modified Date, Creation Date
- Mac, Linux: Last Modified Date
  <br><br>

# Changing Options

You can change the options in the Config section of png2jpg.py.

```
# ========= Config start / 設定ここから =========
# ディレクトリ / Directories
INPUT_DIR = 'inputs/'
OUTPUT_DIR = 'outputs/'

# JPEG品質 (0-100) / JPEG quality (0-100)
QUALITY = 80

# 出力画像拡張子（'jpg', 'jpeg', 'JPG', 'JPEG'）/ Output image file extension ('jpg', 'jpeg', 'JPG', 'JPEG')
IMG_OUTPUT_FILENAME_EXT = 'jpg'

# A1111画像の追加設定 / Additional settings for A1111 images
# 他生成AI用のダミーpngを出力 / Output a dummy PNG file for other generation AIs
# True / False
A1111_METADATA_PNG = True

# NovelAI画像の追加設定 / Additional settings for NovelAI images
# NovelAI（及びA1111）入力用のダミーpngを出力 / Output a dummy PNG file for NovelAI (and A1111) input
# True / False
NOVELAI_METADATA_PNG = True

# CompyUI画像の追加設定 / Additional settings for CompyUI images
# ワークフロー入力用のjsonを出力 / Output a JSON file for Workflow input
# True / False
COMPYUI_WORKFLOW_JSON = True
# ========= Config end / 設定ここまで ==========
```

# Prerequisites

Python3 environment
<br><br>

# Preparation

Install the following libraries if they are not already installed:

- PIL

```
pip install pillow
```

- piexif

```
pip install piexif
```

Windows only

- pywin32

```
pip install pywin32
```

<br>

# Usage

1. Place the PNG images you want to convert in the inputs folder.
2. For Windows, double-click png2jpg.bat. For Mac, Linux, etc., run png2jpg.py from the terminal.
3. The JPEG images will be saved in the outputs folder.
   <br><br>

# Changing Settings, etc.

- If you're running the Windows bat file and want to keep the command line open after processing is complete so you can check for errors or conversion status, uncomment the @REM pause line in png2jpg.bat.
  <br><br>

# Changelog

## [1.0.0] - 2024-06-12

### Added

- Initial release
  <br><br>

# License

Copyright © 2024 Takenoko  
Released under the [MIT License](https://opensource.org/licenses/mit-license.php).
<br><br><br>
