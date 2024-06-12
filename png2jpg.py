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
files = glob.glob(INPUT_DIR + '*.' + IMG_INPUT_FILENAME_EXT)

# 対象画像の変換・保存
for file in files:
    file_name = os.path.splitext(os.path.basename(file))[0]
    output_file_name = file_name + '.' + IMG_OUTPUT_FILENAME_EXT
    output_file_path = OUTPUT_DIR + output_file_name
    output_file_abspath = os.path.abspath(OUTPUT_DIR + output_file_name)
    json_output_file_name = file_name + '.json'
    json_output_file_path = OUTPUT_DIR + json_output_file_name
    output_json = False
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

    # JPEGに変換
    image = image.convert('RGB')
    image.save(output_file_path, format=IMG_OUTPUT_FORMAT, quality=QUALITY)

    # 画像を閉じる
    image.close()

    # JPEGファイルにExifデータ（PNG Info）を保存する
    if png_info is not None:
        # pnginfoの各項目を改行区切りで連結
        png_info_data = ""
        json_data = ""
        for key, value in png_info.items():
            # CompyUI形式データの場合
            if key == 'workflow':
                if COMPYUI_WORKFLOW_JSON:
                    json_data += f"{value}"

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

        # Exifデータを作成
        exif_dict = {"Exif": {piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(png_info_data or '', encoding='unicode')}}

        # Exifデータをバイトに変換
        exif_bytes = piexif.dump(exif_dict)

        # Exifデータを挿入して新しい画像を保存
        piexif.insert(exif_bytes, output_file_path)

        # JSONデータに値がある場合、jsonを保存する
        if json_data:
            json_data = json_data.rstrip()
            with open(json_output_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json.loads(json_data), json_file, ensure_ascii=False, indent=4)
                output_json = True

    else:
        print("Could not retrieve PNG Info / PNG Infoを取得できませんでした")

    # 出力画像に元画像の日付情報を設定
    set_file_times(output_file_path, creation_time, access_time, modify_time)

    # 設定条件による追加処理
    # jsonを出力
    if output_json:
        set_file_times(json_output_file_path, creation_time, access_time, modify_time)

    # 生成AI入力用png画像を生成する
    if output_metadata_image:
        width, height = 176, 176
        gray_color = (48, 48, 48, 255)
        text_color = gray_color

        # 新しい画像を作成
        text_image = Image.new('RGBA', (width, height), (200, 200, 200, 255))
        draw = ImageDraw.Draw(text_image)

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

        # 新しい画像のパスを設定
        text_image_path = OUTPUT_DIR + file_name + '.png'
        text_image.save(text_image_path, format='PNG', pnginfo=pnginfo)
        text_image.close()

        # 日時情報を設定
        set_file_times(text_image_path, creation_time, access_time, modify_time)
