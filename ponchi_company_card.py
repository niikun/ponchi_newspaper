import streamlit as st
from PIL import Image, ExifTags
import io
import base64

def orient_image(img):
    """EXIF情報を元に画像を正しいオリエンテーションに調整します。"""
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    try:
        exif = img._getexif()
        if exif is not None and orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(-90, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError, TypeError):
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

def process_image(base_img, img1):
    base_img = base_img.copy()
    img1 = center_crop_to_square(img1, 220)
    base_img.paste(img1, (80, 280))
    return base_img

def get_image_download_link(img, filename="output.png", text="ダウンロード"):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

st.title("ポンチしんぶん\nしゃいんしょ いんさつしょ")

uploaded_img1 = st.file_uploader("あなたの しゃしんを アップロードして!", type=["jpg", "jpeg"])

if uploaded_img1:
    img1 = Image.open(uploaded_img1)
    img1 = orient_image(img1)
    result = process_image(Image.open("ponchi_company_card.png"), img1)
    st.image(result, caption="できた！", use_column_width=True)
    st.markdown(get_image_download_link(result), unsafe_allow_html=True)
else:
    st.image("ponchi_company_card.png", caption="いんさつまえ", use_column_width=True)
