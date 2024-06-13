# Copyright © 2024 Takenoko
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import glob
import os
import piexif
import piexif.helper
import json
from PIL import Image, PngImagePlugin, ImageDraw, ImageFont
from datetime import datetime
from pywintypes import Time

# Windowsの場合
on_windows = os.name == 'nt'
if on_windows:
    import win32file
    import win32con

# ========= 変更不可 (Unchangeable) ==========
# Configuration changes can be made from config.txt / 設定変更はconfig.txtより行えます
# デフォルト値
DEFAULT_QUALITY = 80
INPUT_DIR = 'inputs/'
OUTPUT_DIR = 'outputs/'
DEFAULT_INCLUDE_SUBDIRS = False
DEFAULT_IMG_OUTPUT_FILENAME_EXT = 'jpg'
VALID_IMG_OUTPUT_FILENAME_EXTS = ['jpg', 'jpeg', 'JPG', 'JPEG']
DEFAULT_BOOL = True
DEFAULT_SKIP_EXISTING_FILES = False
# ========= 変更不可 (Unchangeable) ==========

# 設定ファイルを読み込む関数
def load_config(config_file):
    config = {}
    with open(config_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split(" = ")
                if value in ["True", "False"]:
                    config[key] = value == "True"
                elif value.isdigit():
                    config[key] = int(value)
                else:
                    # 両端がシングルクォート、ダブルクォート、またはバッククォートの場合、取り除く
                    if ((value.startswith("'") and value.endswith("'")) or
                        (value.startswith('"') and value.endswith('"')) or
                        (value.startswith("`") and value.endswith("`"))):
                        value = value[1:-1]
                    config[key] = value
    return config

# 設定ファイルを読み込む
config = load_config('config.txt')
# 設定を変数に割り当てる、入力値が不正な場合はデフォルト値を使用する
INPUT_DIR = config.get('INPUT_DIR', INPUT_DIR )
OUTPUT_DIR = config.get('OUTPUT_DIR', OUTPUT_DIR)

# QUALITYの検証
QUALITY = config.get('QUALITY', DEFAULT_QUALITY)
if not (0 <= QUALITY <= 100):
    QUALITY = DEFAULT_QUALITY

# IMG_OUTPUT_FILENAME_EXTの検証
IMG_OUTPUT_FILENAME_EXT = config.get('IMG_OUTPUT_FILENAME_EXT', DEFAULT_IMG_OUTPUT_FILENAME_EXT)
if IMG_OUTPUT_FILENAME_EXT not in VALID_IMG_OUTPUT_FILENAME_EXTS:
    IMG_OUTPUT_FILENAME_EXT = DEFAULT_IMG_OUTPUT_FILENAME_EXT

# Bool値の検証
A1111_METADATA_PNG = config.get('A1111_METADATA_PNG', DEFAULT_BOOL)
if not isinstance(A1111_METADATA_PNG, bool):
    A1111_METADATA_PNG = DEFAULT_BOOL

NOVELAI_METADATA_PNG = config.get('NOVELAI_METADATA_PNG', DEFAULT_BOOL)
if not isinstance(NOVELAI_METADATA_PNG, bool):
    NOVELAI_METADATA_PNG = DEFAULT_BOOL

COMFYUI_WORKFLOW_JSON = config.get('COMFYUI_WORKFLOW_JSON', DEFAULT_BOOL)
if not isinstance(COMFYUI_WORKFLOW_JSON, bool):
    COMFYUI_WORKFLOW_JSON = DEFAULT_BOOL

# サブディレクトリを含めるかどうかの設定
INCLUDE_SUBDIRS = config.get('INCLUDE_SUBDIRS', DEFAULT_INCLUDE_SUBDIRS)
if not isinstance(INCLUDE_SUBDIRS, bool):
    INCLUDE_SUBDIRS = DEFAULT_INCLUDE_SUBDIRS

# 出力ファイルが既に存在する場合にスキップするかどうかの設定
SKIP_EXISTING_FILES = config.get('SKIP_EXISTING_FILES', DEFAULT_SKIP_EXISTING_FILES)
if not isinstance(SKIP_EXISTING_FILES, bool):
    SKIP_EXISTING_FILES = DEFAULT_SKIP_EXISTING_FILES

# ========= 変更不可 (Unchangeable) ==========
# 画像形式
IMG_INPUT_FORMAT = 'PNG'
IMG_OUTPUT_FORMAT = 'JPEG'
# 画像拡張子
IMG_INPUT_FILENAME_EXT = 'png'
# ========= 変更不可 (Unchangeable) ==========

# 日付情報の設定関数
def set_file_times(file_path, creation_time, access_time, modify_time):
    # Windowsの場合、元画像の作成日時、アクセス日時、更新日時を設定
    if on_windows:
        handle = win32file.CreateFile(
            file_path,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            0,
            None
        )
        win32file.SetFileTime(handle, Time(creation_time), Time(access_time), Time(modify_time))
        handle.Close()
    # 他のプラットフォームの場合、元画像のアクセス日時と更新日時を設定
    os.utime(file_path, (access_time, modify_time))

# 画像を配列に格納
if INCLUDE_SUBDIRS:
    files = glob.glob(os.path.join(INPUT_DIR, '**', '*.' + IMG_INPUT_FILENAME_EXT), recursive=True)
else:
    files = glob.glob(os.path.join(INPUT_DIR, '*.' + IMG_INPUT_FILENAME_EXT))

# 対象画像の変換・保存
for file in files:
    # 入力ファイルの相対パスを取得
    relative_path = os.path.relpath(file, INPUT_DIR)
    file_name = os.path.splitext(os.path.basename(file))[0]

    # 出力ディレクトリの構造を作成
    output_subdir = os.path.dirname(relative_path)
    output_dir = os.path.join(OUTPUT_DIR, output_subdir)
    os.makedirs(output_dir, exist_ok=True)

    output_file_name = file_name + '.' + IMG_OUTPUT_FILENAME_EXT
    output_file_path = os.path.join(output_dir, output_file_name)
    output_file_abspath = os.path.abspath(output_file_path)
    json_output_file_name = file_name + '.json'
    json_output_file_path = os.path.join(output_dir, json_output_file_name)
    dammy_image_path = os.path.join(output_dir, file_name + '.png')
    output_json = False
    json_data = ""
    output_metadata_image = False
    generated_software_name = ""

    def get_png_info(file):
        try:
            img = Image.open(file)
            png_info = img.info
            img.close()
            return png_info
        except Exception as e:
            print(f"Could not open image / 画像を開けませんでした : {e}")
            return None

    # PNGファイルからpnginfoを取得
    png_info = get_png_info(file)

    # 画像を開く
    image = Image.open(file)

    # 日時情報を取得
    access_time = os.path.getatime(file)
    modify_time = os.path.getmtime(file)
    if on_windows:
        creation_time = os.path.getctime(file)

    # 画像変換
    # 出力ファイルが既に存在する場合にスキップする処理
    skip_image = SKIP_EXISTING_FILES and os.path.exists(output_file_path)
    if skip_image:
        print(f"Skipped image: {output_file_path}")
    else:
        # JPEGに変換して保存
        image = image.convert('RGB')
        image.save(output_file_path, format=IMG_OUTPUT_FORMAT, quality=QUALITY)
        print(f"Saved image: {output_file_path}")

    # JPEGファイルにExifデータ（PNG Info）を保存する
    if png_info is not None:
        # pnginfoの各項目を改行区切りで連結
        png_info_data = ""
        for key, value in png_info.items():
            # ComfyUI形式データの場合
            if key == 'workflow':
                if COMFYUI_WORKFLOW_JSON:
                    json_data += f"{value}"
                    json_data = json_data.rstrip()
                    output_json = True

            # NovelAI形式データの場合
            if key == 'Software' and value == 'NovelAI':
                if NOVELAI_METADATA_PNG:
                    generated_software_name = "NovelAI"
                    output_metadata_image = True

            # Automatic1111形式データの場合
            if key == 'parameters':
                png_info_data += f"{value}\n"
                if A1111_METADATA_PNG:
                    generated_software_name = "other AI"
                    output_metadata_image = True
            else:
                png_info_data += f"{key}: {value}\n"

        png_info_data = png_info_data.rstrip()

        if not skip_image:
            # Exifデータを作成
            exif_dict = {"Exif": {piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(png_info_data or '', encoding='unicode')}}
            # Exifデータをバイトに変換
            exif_bytes = piexif.dump(exif_dict)
            # Exifデータを挿入して画像を保存
            piexif.insert(exif_bytes, output_file_path)
    else:
        print("Could not retrieve PNG Info / PNG Infoを取得できませんでした")

    # 出力画像に元画像の日付情報を設定
    set_file_times(output_file_path, creation_time, access_time, modify_time)

    # 画像を閉じる
    image.close()


    # 設定条件による追加処理

    # jsonを出力
    # 出力ファイルが既に存在する場合にスキップする
    skip_json = SKIP_EXISTING_FILES and os.path.exists(json_output_file_path)
    if skip_json:
        print(f"Skipped json : {json_output_file_path}")
    else:
        if output_json:
            if json_data:
                with open(json_output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json.loads(json_data), json_file, ensure_ascii=False, indent=4)
                    print(f"Saved json: {json_output_file_path}")

                # 日付情報を設定
                set_file_times(json_output_file_path, creation_time, access_time, modify_time)
            else:
                print("Could not retrieve workflow / ワークフローを取得できませんでした")

    # 生成AI入力用ダミーpngを生成する
    # 出力ファイルが既に存在する場合にスキップする
    skip_dammy_image = SKIP_EXISTING_FILES and os.path.exists(dammy_image_path)
    if skip_dammy_image:
        print(f"Skipped dammy : {dammy_image_path}")
    else:
        if output_metadata_image:
            width, height = 176, 176
            gray_color = (48, 48, 48, 255)
            text_color = gray_color

            # 画像を作成
            dammy_image = Image.new('RGBA', (width, height), (200, 200, 200, 255))
            draw = ImageDraw.Draw(dammy_image)

            # フォントを設定
            try:
                font = ImageFont.truetype("arial.ttf", 19)
            except IOError:
                font = ImageFont.load_default()

            # 文字を描画
            text = "For " + generated_software_name + " input"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = (width - text_width) / 2
            text_y = (height - text_height) / 2
            draw.text((text_x, text_y), text, fill=text_color, font=font)

            # pnginfoを設定
            pnginfo = PngImagePlugin.PngInfo()
            for key, value in png_info.items():
                pnginfo.add_text(key, str(value))

            # 画像のパスを設定
            dammy_image.save(dammy_image_path, format='PNG', pnginfo=pnginfo)
            print(f"Saved dammy: {dammy_image_path}")
            dammy_image.close()

            # 日時情報を設定
            set_file_times(dammy_image_path, creation_time, access_time, modify_time)

