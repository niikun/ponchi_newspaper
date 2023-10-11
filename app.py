import streamlit as st
from PIL import Image

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

st.title("ポンチしんぶん せいさくアプリ")

base_image = Image.open("ponchi.png")

uploaded_img1 = st.file_uploader("メインしゃしん をアップロードしてください (1.jpg)", type="jpg")
uploaded_img2 = st.file_uploader("サブしゃしん１ をアップロードしてください (2.jpg)", type="jpg")
uploaded_img3 = st.file_uploader("サブしゃしん２ をアップロードしてください (3.jpg)", type="jpg")
uploaded_img4 = st.file_uploader("きみのしゃしん をアップロードしてください (4.jpg)", type="jpg")

if uploaded_img1 and uploaded_img2 and uploaded_img3 and uploaded_img4:
    img1 = Image.open(uploaded_img1)
    img2 = Image.open(uploaded_img2)
    img3 = Image.open(uploaded_img3)
    img4 = Image.open(uploaded_img4)

    result = process_image(base_image, img1, img2, img3, img4)
    st.image(result, caption="完成した画像", use_column_width=True)
