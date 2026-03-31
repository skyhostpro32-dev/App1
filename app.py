import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas

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
    ["🎨 Background Change", "✨ Enhance Image", "🎯 Erase Spot"]
)

# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns(2)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
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

                gray = np.mean(img_array[:, :, :3], axis=2)
                mask = gray > 200

                img_array[mask] = (*color, 255)

                result = Image.fromarray(img_array)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                "📥 Download Image",
                buf.getvalue(),
                "background.png"
            )

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

            st.download_button(
                "📥 Download Image",
                buf.getvalue(),
                "enhanced.png"
            )

    # =========================
    # 🎯 ERASE SPOT (FIXED)
    # =========================
    elif tool == "🎯 Erase Spot":
        st.sidebar.subheader("🎯 Erase Settings")

        brush_size = st.sidebar.slider("Brush Size", 10, 50, 30)

        st.write("👉 Draw on image to erase spots")

        # 🔥 FIX: Convert to RGB for canvas
        canvas_image = image.convert("RGB")

        canvas = st_canvas(
            fill_color="rgba(255,0,0,0.4)",
            stroke_width=brush_size,
            stroke_color="white",
            background_image=canvas_image,
            update_streamlit=True,
            height=canvas_image.height,
            width=canvas_image.width,
            drawing_mode="freedraw",
            key="canvas",
        )

        if canvas.image_data is not None:
            img_array = np.array(image)

            mask = canvas.image_data[:, :, 3] > 0

            # Erase (transparent)
            img_array[mask] = [0, 0, 0, 0]

            result = Image.fromarray(img_array)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                "📥 Download Image",
                buf.getvalue(),
                "erased.png"
            )

else:
    st.info("👈 Upload an image from the sidebar to begin")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Built with Streamlit")
