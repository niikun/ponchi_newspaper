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


def process_image(base_img, img1, name):
    base_img = base_img.copy()
    img1 = resize_and_pad(img1, (220, 220))
    base_img.paste(img1, (80, 280))
    
    # 名前を描画するためのフォントとサイズを設定
    font = ImageFont.truetype("sans serif", 40)  # 'arial.ttf'はシステムにインストールされたフォントに置き換えてください
    draw = ImageDraw.Draw(base_img)
    
    # 名前を画像上に配置する位置を設定（x, y座標）
    text_position = (400, 380)  # ここはカードのデザインに合わせて調整してください
    
    # 黒色でテキストを描画
    draw.text(text_position, name, font=font, fill="black")

    return base_img


def resize_and_pad(img, desired_size):
    w, h = img.size
    desired_w, desired_h = desired_size

    # アスペクト比を維持してリサイズ
    ratio = min(desired_w / w, desired_h / h)
    new_w = int(w * ratio)
    new_h = int(h * ratio)
    img = img.resize((new_w, new_h))

    # 新しい画像を生成して白で塗りつぶす
    new_img = Image.new("RGB", desired_size, color="white")
    
    # 元の画像を左上に配置
    new_img.paste(img, (0, 0))

    return new_img

    return new_img

def get_image_download_link(img, filename="output.png", text="いんさつしてね！"):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a target="_blank" href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'


st.title("ポンチしんぶん しゃいんしょ いんさつしょ")

# 名前入力フィールドを追加
name = st.text_input("あなたのなまえをにゅうりょくしてください", "")

uploaded_img1 = st.file_uploader("あなたの しゃしん をアップロードしてください (1.jpg)", type="jpg")

if all([uploaded_img1, name]):
    img1 = orient_image(Image.open(uploaded_img1))

    # 名前も画像処理関数に渡す
    result = process_image(Image.open("ponchi_company_card.png"), img1, name)
    st.image(result, caption="できた！", use_column_width=True)
    
    st.markdown(get_image_download_link(result), unsafe_allow_html=True)
else:
    st.image("ponchi_company_card.png", caption="いんさつまえ", use_column_width=True)