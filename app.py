import streamlit as st
from PIL import Image,ExifTags

def process_image(base_img, img1, img2, img3, img4):
    base_img = base_img.copy()
    
    img1 = img1.resize((300, 250))
    img2 = img2.resize((250, 200))
    img3 = img3.resize((200, 150))
    img4 = img4.resize((65, 65))
    
    base_img.paste(img1, (68, 250))
    base_img.paste(img2, (400, 250))
    base_img.paste(img3, (68, 630))
    base_img.paste(img4, (68, 880))
    
    return base_img

def center_crop(img, desired_size):
    w, h = img.size

    # 横長の場合、通常のリサイズを行う
    if w > h:
        img = img.resize(desired_size, Image.ANTIALIAS)
        return img

    # 縦長の場合、中心を基準にクロップ
    th, tw = desired_size
    left = (w - tw) / 2
    top = (h - th) / 2
    right = left + tw
    bottom = top + th
    img = img.crop((left, top, right, bottom))
    img = img.resize(desired_size)
    return img

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
        # 画像にEXIF情報がない場合、何もしない
        pass
    return img

st.title("ポンチしんぶん せいさくアプリ")

base_image = Image.open("ponchi.png")

uploaded_img1 = st.file_uploader("メインしゃしん をアップロードしてください (1.jpg)", type="jpg")
uploaded_img2 = st.file_uploader("サブしゃしん１ をアップロードしてください (2.jpg)", type="jpg")
uploaded_img3 = st.file_uploader("サブしゃしん２ をアップロードしてください (3.jpg)", type="jpg")
uploaded_img4 = st.file_uploader("きみのしゃしん をアップロードしてください (4.jpg)", type="jpg")

if uploaded_img1 and uploaded_img2 and uploaded_img3 and uploaded_img4:
    img1 = orient_image(Image.open(uploaded_img1))
    img2 = orient_image(Image.open(uploaded_img2))
    img3 = orient_image(Image.open(uploaded_img3))
    img4 = orient_image(Image.open(uploaded_img4))

    result = process_image(base_image, img1, img2, img3, img4)
    st.image(result, caption="完成した画像", use_column_width=True)
