import streamlit as st
from PIL import Image, ExifTags, ImageDraw, ImageFont
import io
import base64

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

def process_image(base_img, img1, name1,name2):
    base_img = base_img.copy()
    img1 = center_crop_to_square(img1, 190)
    base_img.paste(img1, (50, 165))
    
    # 名前を描画するためのフォントとサイズを設定
    font1 = ImageFont.truetype("NotoSansJP-Regular.ttf", 35) 
    font2 = ImageFont.truetype("NotoSansJP-Regular.ttf", 25) 
    draw = ImageDraw.Draw(base_img)
    
    # 名前を画像上に配置する位置を設定（x, y座標）
    text_position1 = (265, 195)
    text_position2 = (265, 160)  # ここはカードのデザインに合わせて調整してください
    
    # 黒色でテキストを描画
    draw.text(text_position2, name2, font=font2, fill="Orange")
    draw.text(text_position1, name1, font=font1, fill="Orange")
    return base_img

def get_image_download_link(img, filename="output.png", text="ダウンロード"):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a target="_blank" href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'


st.title("KOBE元気サロン女子会\n 名札 製作所")

# 名前入力フィールドを追加
name1 = st.text_input("あなたの名前を入力してください", "")
name2 = st.text_input("名前のふりがなを 入力してください", "")

uploaded_img1 = st.file_uploader("あなたの 写真 をアップロードしてください (1.jpg)", type="jpg")

if all([uploaded_img1, name1,name2]):
    img1 = orient_image(Image.open(uploaded_img1))

    # 名前も画像処理関数に渡す
    result = process_image(Image.open("kgs_plate.png"), img1, name1,name2)
    st.image(result, caption="できた！", use_column_width=True)
    
    st.markdown(get_image_download_link(result), unsafe_allow_html=True)
else:
    st.image("kgs_plate.png", caption="制作前", use_column_width=True)