import streamlit as st
from sprite_converter import SpriteConverter
from pathlib import Path
import tempfile
import os
import base64
import random


# Initialize session state for uploader reset
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = str(random.randint(1000, 9999))

# Configuration de la page
st.set_page_config(
    page_title="Sprite2GIF Converter",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Dark mode CSS avec design moderne
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem 1rem;
    }

    /* Hide ONLY the uploaded file list, keep the dropzone */
    [data-testid='stFileUploader'] ul {
        display: none;
    }
    [data-testid='stFileUploader'] div[role="listbox"] {
        display: none;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .app-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        color: #a0a0a0;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    .settings-title {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .preview-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 239, 125, 0.6);
    }
    
    .stSuccess {
        background: rgba(56, 239, 125, 0.1);
        border-left: 4px solid #38ef7d;
        border-radius: 8px;
    }
    
    .stError {
        background: rgba(239, 56, 56, 0.1);
        border-left: 4px solid #ef3856;
        border-radius: 8px;
    }
    
    label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🎨 Sprite2GIF</div>
        <div class="app-subtitle">Transform your sprite sheets into animated GIFs</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Create 2-column layout from the start
col_left, col_right = st.columns([1, 1.2], gap="large")

# ========== LEFT COLUMN - UPLOAD & RESULT ==========
with col_left:
    st.markdown(
        '<div class="settings-title">Step 1: Upload</div>', unsafe_allow_html=True
    )

    # Upload section
    uploaded_file = st.file_uploader(
        "Drop your sprite sheet here",
        type=["png"],
        help="Upload a PNG sprite sheet",
        label_visibility="collapsed",
        key=st.session_state.uploader_key,
    )

    if uploaded_file is not None:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            sprite_path = tmp_file.name

        # Custom Thumbnail Preview (Compact)
        st.markdown("<br>", unsafe_allow_html=True)
        c_prev, c_info = st.columns([0.3, 0.7])
        with c_prev:
            st.image(uploaded_file, width=80)
        with c_info:
            # Layout: Filename | X Button
            c_name, c_btn = st.columns([0.7, 0.3])
            c_name.caption(f"**{uploaded_file.name}**")
            if c_btn.button("❌", key="rm_btn", help="Remove file"):
                st.session_state.uploader_key = str(random.randint(1000, 9999))
                st.rerun()

        # Placeholder for GIF result
        st.markdown("<br>", unsafe_allow_html=True)
        gif_container = st.container()

# ========== RIGHT COLUMN - PREVIEW & SETTINGS ==========
if uploaded_file is not None:
    with col_right:
        st.markdown(
            '<div class="settings-title">Step 2: Configure</div>',
            unsafe_allow_html=True,
        )

        # Row 1: Dimensions
        c1, c2 = st.columns(2)
        with c1:
            frame_width = st.slider(
                "🔲 Frame Width (px)", min_value=16, max_value=512, value=256, step=16
            )
        with c2:
            frame_height = st.slider(
                "📏 Frame Height (px)", min_value=16, max_value=512, value=256, step=16
            )

        # Row 2: Grid
        c3, c4 = st.columns(2)
        with c3:
            frames_per_row = st.slider(
                "➡️ Frames per Row", min_value=1, max_value=20, value=4
            )
        with c4:
            number_of_rows = st.slider(
                "⬇️ Number of Rows", min_value=1, max_value=20, value=1
            )

        # Row 3: Animation
        c5, c6 = st.columns(2)
        with c5:
            duration = st.slider(
                "⏱️ Duration (ms)", min_value=10, max_value=1000, value=100, step=10
            )
        with c6:
            loop_count = st.slider(
                "🔄 Loop Count", min_value=0, max_value=10, value=0, help="0 = infinite"
            )

        # Advanced settings
        with st.expander("🔧 Advanced Settings", expanded=False):
            c_opt, c_trans, c_select = st.columns([1.5, 2, 3])
            with c_opt:
                st.markdown(
                    "<div style='padding-top: 15px;'></div>", unsafe_allow_html=True
                )
                optimize = st.checkbox("Optimize", value=True, help="Reduce file size")
            with c_trans:
                st.markdown(
                    "<div style='padding-top: 15px;'></div>", unsafe_allow_html=True
                )
                transparency = st.checkbox(
                    "Transparency", value=True, help="Keep transparent areas"
                )
            with c_select:
                selected_rows = st.multiselect(
                    "📑 Select Rows",
                    options=list(range(1, number_of_rows + 1)),
                    default=list(range(1, number_of_rows + 1)),
                    help="Choose which rows to include",
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Convert button
        if st.button("🚀 Convert to GIF", use_container_width=True):
            if not selected_rows:
                st.error("⚠️ Please select at least one row!")
            else:
                with st.spinner("✨ Converting..."):
                    # Create output file
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".gif"
                    ) as output_file:
                        output_path = output_file.name

                    # Convert
                    converter = SpriteConverter(sprite_path)
                    success = converter.convert_to_gif(
                        output_path=output_path,
                        frame_width=frame_width,
                        frame_height=frame_height,
                        num_cols=frames_per_row,
                        num_rows=number_of_rows,
                        duration=duration,
                        loop=loop_count,
                        optimize=optimize,
                        selected_rows=selected_rows,
                    )

                    if success:
                        st.toast("🎉 GIF created successfully!", icon="✅")

                        # Read GIF data immediately
                        with open(output_path, "rb") as f:
                            gif_bytes = f.read()
                        b64_gif = base64.b64encode(gif_bytes).decode()

                        # Display GIF in left column
                        with gif_container:
                            try:
                                st.markdown(
                                    f'<div style="display: flex; justify-content: center;">'
                                    f'<img src="data:image/gif;base64,{b64_gif}" alt="Generated GIF" style="max-width: 100%; border-radius: 10px;">'
                                    f"</div>",
                                    unsafe_allow_html=True,
                                )
                            except Exception as e:
                                st.error(f"❌ Error: {e}")

                        # Download button (Right Column, below Convert)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.download_button(
                            label="💾 Download GIF",
                            data=gif_bytes,
                            file_name=f"{Path(uploaded_file.name).stem}.gif",
                            mime="image/gif",
                            use_container_width=True,
                        )

                        # Cleanup
                        os.unlink(sprite_path)
                        os.unlink(output_path)
                    else:
                        st.error("❌ Failed to create GIF")

else:
    # Instructions when no file uploaded - 2 Column Layout
    c_help_left, c_help_right = st.columns(2, gap="large")

    with c_help_left:
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1); height: 100%;">
                <div class="settings-title">📖 How to Use</div>
                <ol style="color: #e0e0e0; line-height: 2;">
                    <li>Upload your sprite sheet (PNG format)</li>
                    <li>Configure frame dimensions and grid layout</li>
                    <li>Adjust animation settings</li>
                    <li>Click "Convert to GIF"</li>
                    <li>Download your animation!</li>
                </ol>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with c_help_right:
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 2rem; border: 1px solid rgba(255, 255, 255, 0.1); height: 100%;">
                <div class="settings-title">💡 Tips</div>
                <ul style="color: #e0e0e0; line-height: 2;">
                    <li>Use power-of-2 dimensions (64, 128, 256, 512) for best results</li>
                    <li>Lower frame duration = faster animation</li>
                    <li>Enable optimization to reduce file size</li>
                    <li>Select specific rows to create partial animations</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )
