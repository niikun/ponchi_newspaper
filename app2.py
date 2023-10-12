import streamlit as st
from PIL import Image, ExifTags
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

def center_crop(img, desired_size):
    w, h = img.size
    if w > h:  # 横長の場合
        img = img.resize(desired_size)
    else:  # 縦長の場合
        th, tw = desired_size
        left = (w - tw) / 2
        top = (h - th) / 2
        right = left + tw
        bottom = top + th
        img = img.crop((left, top, right, bottom))
        img = img.resize(desired_size)
    return img

def process_image(base_img, img1, img2, img3, img4):
    base_img = base_img.copy()

    img1 = center_crop(img1, (300, 250))
    img2 = center_crop(img2, (250, 200))
    img3 = center_crop(img3, (200, 150))
    img4 = center_crop(img4, (65, 65))

    base_img.paste(img1, (68, 250))
    base_img.paste(img2, (400, 250))
    base_img.paste(img3, (68, 630))
    base_img.paste(img4, (68, 880))

    a4_size = (2100, 2970)  # A4サイズ
    base_img = base_img.resize(a4_size)
    return base_img

def get_image_download_link(img, filename="output.png", text="Download result image"):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a target="_blank" href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'

st.title("ポンチしんぶん いんさつしょ")

uploaded_img1 = st.file_uploader("メインのえ をアップロードしてください (1.jpg)", type="jpg")
uploaded_img2 = st.file_uploader("サブのえ をアップロードしてください (2.jpg)", type="jpg")
uploaded_img3 = st.file_uploader("サブのえ をアップロードしてください (3.jpg)", type="jpg")
uploaded_img4 = st.file_uploader("あなたのしゃしん をアップロードしてください (4.jpg)", type="jpg")

if all([uploaded_img1, uploaded_img2, uploaded_img3, uploaded_img4]):
    img1 = orient_image(Image.open(uploaded_img1))
    img2 = orient_image(Image.open(uploaded_img2))
    img3 = orient_image(Image.open(uploaded_img3))
    img4 = orient_image(Image.open(uploaded_img4))

    result = process_image(Image.open("ponchi.png"), img1, img2, img3, img4)
    st.image(result, caption="できた！", use_column_width=True)
    
    st.markdown(get_image_download_link(result), unsafe_allow_html=True)
else:
    st.image("ponchi.png", caption="いんさつまえ", use_column_width=True)