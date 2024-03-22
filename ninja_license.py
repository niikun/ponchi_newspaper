import streamlit as st
from PIL import Image, ExifTags, ImageDraw, ImageFont
import io
import base64
import datetime

def orient_image(img):
    """EXIF情報を元に画像を正しいオリエンテーションに調整します"""
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    try:
        exif = img._getexif()
        if exif is not None and orientation in exif:
            if exif[orientation] == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 3:
                img = img.rotate(180)
            elif exif[orientation] == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 6:
                img = img.rotate(-90, expand=True)
            elif exif[orientation] == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img


def center_crop_to_square(img, size):
    w, h = img.size
    min_side = min(w, h)
    left = (w - min_side) / 2
    top = (h - min_side) / 2
    right = (w + min_side) / 2
    bottom = (h + min_side) / 2
    img = img.crop((left, top, right, bottom)).resize((size, size), Image.Resampling.LANCZOS)
    return img

def process_image(base_img, img1, name, today_date):
    base_img = base_img.copy()
    img1 = center_crop_to_square(img1, 450)
    base_img.paste(img1, (640, 200))
    
    # 名前を描画するためのフォントとサイズを設定
    font = ImageFont.truetype("NotoSansJP-Regular.ttf", 60) 
    draw = ImageDraw.Draw(base_img)
    
    # 名前を画像上に配置する位置を設定（x, y座標）
    text_position = (480, 26)  # ここはカードのデザインに合わせて調整してください
    
    # 黒色でテキストを描画
    draw.text(text_position, name, font=font, fill="black")

    # 今日の日付を描画
    font_date = ImageFont.truetype("NotoSansJP-Regular.ttf", 30) 
    date_position = (250, 420)
    draw.text(date_position, today_date, font=font_date, fill="black")

    return base_img

def get_image_download_link(img, filename="output.png", text="いんさつしてね！"):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a target="_blank" href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'

st.title("忍者免許発行所")

# 今日の日付を取得
today_date = datetime.date.today().strftime("%Y年%m月%d日")

# 名前入力フィールドを追加
name = st.text_input("なまえをにゅうりょくしてください", "")

uploaded_img1 = st.file_uploader("しゃしん をアップロードしてください (1.jpg)", type="jpg")

if all([uploaded_img1, name]):
    img1 = orient_image(Image.open(uploaded_img1))

    # 名前と今日の日付を画像処理関数に渡す
    result = process_image(Image.open("ninja_license.png"), img1, name, today_date)
    st.image(result, caption="できた！", use_column_width=True)
    
    st.markdown(get_image_download_link(result), unsafe_allow_html=True)
else:
    st.image("ninja_license.png", caption="いんさつまえ", use_column_width=True)
