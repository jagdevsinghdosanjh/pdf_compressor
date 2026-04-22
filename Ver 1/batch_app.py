import streamlit as st
import os
from compressor import compress_to_target

st.set_page_config(page_title="Batch PDF Compressor <7MB", layout="centered")

st.title("📄 Batch PDF Compressor (Auto Target <7MB Each)")

uploaded_files = st.file_uploader(
    "Upload Multiple PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Total PDFs uploaded: **{len(uploaded_files)}**")

    if st.button("Start Batch Compression"):
        st.info("Processing all PDFs… please wait")

        output_files = []

        for file in uploaded_files:
            st.write(f"🔧 Compressing: **{file.name}**")

            # Save input
            input_path = f"input_{file.name}"
            with open(input_path, "wb") as f:
                f.write(file.getvalue())

            # Compress to <7MB
            output_path, compressed_size, level_used = compress_to_target(input_path, target_mb=7)

            st.success(f"{file.name} → {compressed_size:.2f} MB (Mode: {level_used})")

            # Save final output
            final_name = f"compressed_{file.name}"
            os.rename(output_path, final_name)
            output_files.append(final_name)

        st.write("### Download Compressed PDFs")

        for f in output_files:
            with open(f, "rb") as pdf:
                st.download_button(
                    label=f"Download {f}",
                    data=pdf,
                    file_name=f,
                    mime="application/pdf"
                )
