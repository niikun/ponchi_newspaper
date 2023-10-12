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

# def center_crop(img, desired_size):
#     w, h = img.size
#     desired_w, desired_h = desired_size

#     # アスペクト比を計算
#     img_ratio = w / h
#     desired_ratio = desired_w / desired_h

#     # リサイズするサイズを計算
#     if img_ratio > desired_ratio:
#         # 元の画像が横長の場合
#         resize_w = int(h * desired_ratio)
#         resize_h = h
#     else:
#         # 元の画像が縦長、または同じアスペクト比の場合
#         resize_w = w
#         resize_h = int(w / desired_ratio)

#     img = img.resize((resize_w, resize_h))

    # 画像の中央を目的のサイズにクロップ
    # left = (resize_w - desired_w) / 2
    # top = (resize_h - desired_h) / 2
    # right = left + desired_w
    # bottom = top + desired_h
    # img = img.crop((left, top, right, bottom))

    # return img



def process_image(base_img, img1, img2, img3, img4):
    base_img = base_img.copy()

    # img1 = center_crop(img1, (300, 250))
    # img2 = center_crop(img2, (250, 200))
    # img3 = center_crop(img3, (200, 150))
    # img4 = center_crop(img4, (65, 65))

    img1 = resize_and_pad(img1, (300, 250))
    img2 = resize_and_pad(img2, (250, 200))
    img3 = resize_and_pad(img3, (200, 150))
    img4 = resize_and_pad(img4, (65, 65))

    base_img.paste(img1, (68, 250))
    base_img.paste(img2, (400, 250))
    base_img.paste(img3, (68, 630))
    base_img.paste(img4, (68, 880))

    a4_size = (2100, 2970)  # A4サイズ
    base_img = base_img.resize(a4_size)
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
    
    # 元の画像を中央に配置
    x_offset = (desired_w - new_w) // 2
    y_offset = (desired_h - new_h) // 2
    new_img.paste(img, (x_offset, y_offset))

    return new_img

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