import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

st.title("✨ AI Image Dashboard")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🧰 Tools")

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Image", type=["png", "jpg", "jpeg"]
)

tool = st.sidebar.radio(
    "Select Tool",
    ["🎨 Background Change", "✨ Enhance Image"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Advanced Tool")
st.sidebar.markdown("👉 Use Erase Tool below")

# 👉 Link to HTML tool
st.sidebar.markdown(
    "[🚀 Open Erase Tool](https://skyhostpro32-dev.github.io/erase-tool/)"
)

# =========================
# MAIN
# =========================
col1, col2 = st.columns(2)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))

    with col1:
        st.subheader("📸 Original Image")
        st.image(image, use_column_width=True)

    # =========================
    # 🎨 BACKGROUND CHANGE
    # =========================
    if tool == "🎨 Background Change":
        st.sidebar.subheader("🎨 Settings")

        color_hex = st.sidebar.color_picker("Pick Background Color", "#00ffaa")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

        if st.sidebar.button("🚀 Apply Background"):
            with st.spinner("Processing..."):
                img_array = np.array(image)

                gray = np.mean(img_array, axis=2)
                mask = gray > 200

                img_array[mask] = color

                result = Image.fromarray(img_array)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button("📥 Download", buf.getvalue(), "background.png")

    # =========================
    # ✨ ENHANCE IMAGE
    # =========================
    elif tool == "✨ Enhance Image":
        st.sidebar.subheader("✨ Settings")

        strength = st.sidebar.slider("Sharpness", 1, 5, 2)

        if st.sidebar.button("🚀 Enhance"):
            with st.spinner("Enhancing image..."):
                result = image

                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button("📥 Download", buf.getvalue(), "enhanced.png")

else:
    st.info("👈 Upload an image from the sidebar to begin")

st.markdown("---")
st.caption("🚀 Built with Streamlit")
