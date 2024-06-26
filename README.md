# png2jpg-ai-image-metadata

[日本語](#日本語) | [English](#english)

# 日本語

# 概要

- AI 生成画像のメタデータを保持して PNG を JPEG に変換します。
- サブディレクトリを含めて一括変換が可能です。
- PNG のメタデータを取得して JPEG の Exif に移植する機能を持つため、AI 生成画像以外のでもメタデータの保持目的で使用可能です。
  <br><br>

# 特長

- Automatic1111, ComfyUI, NovelAI の生成画像に対応しています。
- 元の PNG 画像が持つメタデータを JPEG 画像の Exif に格納します。
- 元の PNG 画像からメタデータを移植したダミー PNG(数 kB 程度)を同時に出力することが可能です。画像を変換すると生成 AI への取り込み機能が一部失われる場合がありますが、これにより機能を保持することが可能です。
- 出力ディレクトリに同名のファイルがある場合、デフォルトでは上書き処理を行いますが、処理をスキップすることも可能です。出力ディレクトリに変換済みの画像が置いてある状態でも、追加分だけ変換が可能なため処理を軽減できます。
  <br><br>

# 説明

## 1. Automatic1111 生成画像の変換について

- JPEG 画像は元画像同様に Automatic1111 の PNG Info に読み込ませて利用することが可能です。
- JPEG に変換すると他の生成 AI（ComfyUI 等）に読み込ませて利用することができなくなりますが、ダミー PNG を追加で出力することで入力機能を保持できます。

## 2. NovelAI 生成画像の変換について

- JPEG に変換すると NovelAI 及び Automatic1111 に読み込ませて利用することができなくなりますが、入力用のダミー PNG(数 kB 程度)を追加で出力することで入力機能を保持できます。
- ダミー PNG は NovelAI 及び Automatic1111 に読み込ませて利用することが可能です。

## 3. ComfyUI 生成画像の変換について

- JPEG に変換すると ComfyUI に入力できなくなりますが、ワークフロー入力用の json を追加で出力することで入力機能を保持できます。

## 4. 日付情報について

元画像の日付情報を変換後の画像に引き継ぎます。

- Windows: 更新日時, 作成日時
- Mac, Linux: 更新日時
  <br><br>

# 使い方

1. inputs フォルダに変換したい PNG 画像を入れます。
2. Windows の場合は png2jpg.bat をダブルクリックします。Mac, Linux 等の場合はターミナルから png2jpg.py を実行します。
3. outputs フォルダに JPEG 画像が保存されます。
   <br><br>

# オプションの変更

- config.txt より変更可能です。
- 入力値が未入力や不正な場合はデフォルト値が適用されます。
- Config.txt は gitignore に登録してあるため git pull で更新しても影響を受けません。

## オプション項目

- QUALITY: JPEG 品質 (0-100)
- INPUT_DIR: 入力ディレクトリ (相対参照または絶対参照で指定)
- OUTPUT_DIR: 出力ディレクトリ (相対参照または絶対参照で指定)
- INCLUDE_SUBDIRS: サブディレクトリを含めるかどうかの設定 (出力画像は入力側と同じディレクトリ構造で保存されます)
- IMG_OUTPUT_FILENAME_EXT: 出力画像拡張子（'jpg', 'jpeg', 'JPG', 'JPEG'）
- A1111_METADATA_PNG: A1111 画像用のダミー PNG を出力するかどうかの設定
- NOVELAI_METADATA_PNG: NovelAI 画像用のダミー PNG を出力するかどうかの設定
- COMFYUI_WORKFLOW_JSON: ComfyUI 画像用の json を出力するかどうかの設定
- SKIP_EXISTING_FILES: 同名の出力ファイルが既に存在する場合にスキップするかどうかの設定
  <br>

## config.txt

```
# ========= Config start =========
QUALITY = 80
INPUT_DIR = 'inputs/'
OUTPUT_DIR = 'outputs/'
INCLUDE_SUBDIRS = False
IMG_OUTPUT_FILENAME_EXT = 'jpg'
A1111_METADATA_PNG = True
NOVELAI_METADATA_PNG = True
COMFYUI_WORKFLOW_JSON = True
SKIP_EXISTING_FILES = False
# ========== Config end ==========
```

<br>

# その他の設定変更等

- Windows の bat ファイル起動でエラーの確認や変換状況を確認するために、処理完了後にコマンドラインを閉じないようにしたい場合は png2jpg.bat 内の@REM pause のコメントアウトを外してください。
  <br><br>

# 必要要件

Python3
<br><br>

# 必要ライブラリ

以下の Python ライブラリを使用するため、入っていない場合はインストールします。

- Pillow：画像の処理を行うためのライブラリ

```
pip install pillow
```

- piexif：Exif データの操作を行うためのライブラリ

```
pip install piexif
```

以下は Windows のみ

- pywin32：Windows プラットフォームでファイルのタイムスタンプを設定するためのライブラリ

```
pip install pywin32
```

<br>

# 変更履歴

## [1.1.0] - 2024-06-13

### 追加

- config.txt によるオプション変更
- サブディレクトリを含めた変換機能
- 同名ファイルの上書きスキップ機能

## [1.0.1] - 2024-06-12

### 修正

- 文言修正

## [1.0.0] - 2024-06-12

### 追加

- 初回リリース
  <br><br>

# ライセンス

Copyright © 2024 Takenoko  
Released under the [MIT License](https://opensource.org/licenses/mit-license.php).
<br><br><br>

# English

# Overview

- Retains metadata of AI-generated images and converts PNG to JPEG.
- Allows batch conversion, including subdirectories.
- Can be used for purposes other than AI-generated images, as it transfers PNG metadata to JPEG Exif.

<br><br>

# Features

- Supports images generated by Automatic1111, ComfyUI, and NovelAI.
- Stores metadata from the original PNG image into the JPEG image's Exif.
- Can simultaneously output dummy PNGs (a few kB) with metadata transferred from the original PNG. This maintains functionality for AI input even after conversion.
- If a file with the same name exists in the output directory, it will overwrite by default, but can be set to skip. This allows additional conversions without reprocessing existing files.

<br><br>

# Description

## 1. Conversion of Automatic1111 Generated Images

- JPEG images can be read and used by Automatic1111's PNG Info similar to the original images.
- Although JPEGs can't be used by other AIs like ComfyUI, outputting a dummy PNG retains input functionality.

## 2. Conversion of NovelAI Generated Images

- JPEGs can't be read by NovelAI or Automatic1111, but outputting a dummy PNG (a few kB) retains input functionality.
- The dummy PNG can be used by both NovelAI and Automatic1111.

## 3. Conversion of ComfyUI Generated Images

- JPEGs can't be input into ComfyUI, but outputting a workflow input JSON retains input functionality.

## 4. Date Information

Transfers the date information from the original image to the converted image.

- Windows: Modification date, Creation date
- Mac, Linux: Modification date

<br><br>

# Usage

1. Place the PNG images you want to convert in the `inputs` folder.
2. For Windows, double-click `png2jpg.bat`. For Mac, Linux, etc., run `png2jpg.py` from the terminal.
3. The JPEG images are saved in the `outputs` folder.

<br><br>

# Changing Options

- Options can be changed from `config.txt`.
- If input values are missing or invalid, default values are applied.
- `config.txt` is registered in `.gitignore`, so updates with `git pull` do not affect it.

## Option Items

- QUALITY: JPEG quality (0-100)
- INPUT_DIR: Input directory (specify with relative or absolute path)
- OUTPUT_DIR: Output directory (specify with relative or absolute path)
- INCLUDE_SUBDIRS: Whether to include subdirectories (output images are saved in the same directory structure as the input)
- IMG_OUTPUT_FILENAME_EXT: Output image extension ('jpg', 'jpeg', 'JPG', 'JPEG')
- A1111_METADATA_PNG: Whether to output a dummy PNG for Automatic1111 images
- NOVELAI_METADATA_PNG: Whether to output a dummy PNG for NovelAI images
- COMFYUI_WORKFLOW_JSON: Whether to output a JSON for ComfyUI images
- SKIP_EXISTING_FILES: Whether to skip processing if a file with the same name already exists

<br><br>

## config.txt

```
# ========= Config start =========
QUALITY = 80
INPUT_DIR = 'inputs/'
OUTPUT_DIR = 'outputs/'
INCLUDE_SUBDIRS = False
IMG_OUTPUT_FILENAME_EXT = 'jpg'
A1111_METADATA_PNG = True
NOVELAI_METADATA_PNG = True
COMFYUI_WORKFLOW_JSON = True
SKIP_EXISTING_FILES = False
# ========== Config end ==========
```

<br>

# Other Settings

- To prevent the command line from closing after execution to check for errors or conversion status, uncomment `@REM pause` in `png2jpg.bat`.

<br><br>

# Requirements

Python3

<br><br>

# Required Libraries

The following Python libraries are used, install them if not already installed.

- Pillow: For image processing

```
pip install pillow
```

- piexif: For manipulating Exif data

```
pip install piexif
```

Windows only:

- pywin32: For setting file timestamps on Windows platforms

```
pip install pywin32
```

<br>

# Changelog

## [1.1.0] - 2024-06-13

### Added

- Option changes via `config.txt`
- Conversion with subdirectories
- Option to skip overwriting files with the same name

## [1.0.1] - 2024-06-12

### Fixed

- Text corrections

## [1.0.0] - 2024-06-12

### Added

- Initial release

<br><br>

# License

Copyright © 2024 Takenoko  
Released under the [MIT License](https://opensource.org/licenses/mit-license.php).

<br><br><br>
