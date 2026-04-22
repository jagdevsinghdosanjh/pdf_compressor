import streamlit as st
import os
from Old.compressor import compress_pdf

st.set_page_config(page_title="PDF Compressor", layout="centered")

st.title("📄 PDF Compressor (High Quality <7MB)")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

quality = st.selectbox(
    "Compression Quality",
    ["high", "medium", "max"],
    index=0
)

if uploaded:
    original_size = len(uploaded.getvalue()) / (1024 * 1024)
    st.write(f"Original Size: **{original_size:.2f} MB**")

    if st.button("Compress PDF"):
        with open("input.pdf", "wb") as f:
            f.write(uploaded.getvalue())

        st.info("Processing… please wait")

        output_path = compress_pdf("input.pdf", quality)

        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        st.success(f"Compressed Size: **{compressed_size:.2f} MB**")

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Compressed PDF",
                data=f,
                file_name="compressed.pdf",
                mime="application/pdf"
            )
