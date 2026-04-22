import streamlit as st
import os
from compressor import compress_to_target

st.set_page_config(page_title="PDF Compressor <7MB", layout="centered")

st.title("📄 PDF Compressor (Auto Target <7MB)")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    original_size = len(uploaded.getvalue()) / (1024 * 1024)
    st.write(f"Original Size: **{original_size:.2f} MB**")

    if st.button("Compress to <7MB"):
        with open("input.pdf", "wb") as f:
            f.write(uploaded.getvalue())

        st.info("Processing… please wait")

        output_path, compressed_size, level_used = compress_to_target("input.pdf", target_mb=7)

        st.success(f"Compressed Size: **{compressed_size:.2f} MB** (Mode: {level_used})")

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Compressed PDF",
                data=f,
                file_name="compressed.pdf",
                mime="application/pdf"
            )
