import os
import subprocess
import pikepdf
import tempfile
import time
import shutil

# def gs_compress(input_path, output_path, quality):
#     quality_map = {
#         "high": "/ebook",
#         "medium": "/screen",
#         "aggressive": "/screen"
#     }

#     gs_quality = quality_map.get(quality, "/ebook")

#     command = [
#         "gswin64c",
#         "-sDEVICE=pdfwrite",
#         "-dCompatibilityLevel=1.4",
#         f"-dPDFSETTINGS={gs_quality}",
#         "-dDownsampleColorImages=true",
#         "-dColorImageResolution=150",
#         "-dNOPAUSE",
#         "-dQUIET",
#         "-dBATCH",
#         f"-sOutputFile={output_path}",
#         input_path
#     ]

#     subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# def gs_compress(input_path, output_path, quality):
#     quality_map = {
#         "high": "/ebook",
#         "medium": "/screen",
#         "aggressive": "/screen"
#     }

#     gs_quality = quality_map.get(quality, "/ebook")

#     command = [
#         "gswin64c",
#         "-sDEVICE=pdfwrite",
#         "-dCompatibilityLevel=1.4",
#         f"-dPDFSETTINGS={gs_quality}",
#         "-dDownsampleColorImages=true",
#         "-dColorImageResolution=150",
#         "-dNOPAUSE",
#         "-dQUIET",
#         "-dBATCH",
#         f"-sOutputFile=\"{output_path}\"",
#         f"\"{input_path}\""
#     ]

#     subprocess.run(" ".join(command), shell=True)

def gs_compress(input_path, output_path, quality):
    quality_map = {
        "high": "/ebook",
        "medium": "/screen",
        "aggressive": "/screen"
    }

    gs_quality = quality_map.get(quality, "/ebook")

    command = (
        f"gswin64c "
        f"-sDEVICE=pdfwrite "
        f"-dCompatibilityLevel=1.4 "
        f"-dPDFSETTINGS={gs_quality} "
        f"-dDownsampleColorImages=true "
        f"-dColorImageResolution=150 "
        f"-dNOPAUSE -dQUIET -dBATCH "
        f"-sOutputFile=\"{output_path}\" "
        f"\"{input_path}\""
    )

    subprocess.run(command, shell=True)


def optimize_with_pikepdf(input_path, output_path):
    # Modern PikePDF: no optimize_version
    with pikepdf.open(input_path) as pdf:
        pdf.save(output_path, compress_streams=True)


def linearize_with_qpdf(input_path, output_path):
    os.system(f"qpdf --linearize \"{input_path}\" \"{output_path}\"")


# def compress_to_target(input_path, target_mb=7):
#     compression_levels = ["high", "medium", "aggressive"]

#     # Windows-safe temp folder
#     tmp = tempfile.mkdtemp()

#     # Initialize to avoid Pylance warnings
#     final_out = None
#     size_mb = None

#     try:
#         current_input = input_path

#         for level in compression_levels:
#             gs_out = os.path.join(tmp, f"gs_{level}.pdf")
#             pike_out = os.path.join(tmp, f"pike_{level}.pdf")
#             final_out = os.path.join(tmp, f"final_{level}.pdf")

#             # Step 1: Ghostscript
#             gs_compress(current_input, gs_out, level)
#             time.sleep(0.3)

#             # Step 2: PikePDF
#             optimize_with_pikepdf(gs_out, pike_out)
#             time.sleep(0.2)

#             # Step 3: qpdf
#             linearize_with_qpdf(pike_out, final_out)
#             time.sleep(0.2)

#             size_mb = os.path.getsize(final_out) / (1024 * 1024)

#             if size_mb <= target_mb:
#                 return final_out, size_mb, level

#             current_input = final_out

#         return final_out, size_mb, "aggressive"

#     finally:
#         try:
#             shutil.rmtree(tmp, ignore_errors=True)
#         except Exception:
#             pass
def compress_to_target(input_path, target_mb=7):
    compression_levels = ["high", "medium", "aggressive"]
    tmp = tempfile.mkdtemp()

    final_out = None
    size_mb = None

    try:
        current_input = input_path

        for level in compression_levels:
            gs_out = os.path.join(tmp, f"gs_{level}.pdf")
            pike_out = os.path.join(tmp, f"pike_{level}.pdf")
            final_out = os.path.join(tmp, f"final_{level}.pdf")

            gs_compress(current_input, gs_out, level)
            optimize_with_pikepdf(gs_out, pike_out)
            linearize_with_qpdf(pike_out, final_out)

            size_mb = os.path.getsize(final_out) / (1024 * 1024)

            if size_mb <= target_mb:
                break

            current_input = final_out

        # ⭐ Copy final file OUTSIDE temp before deleting
        safe_output = os.path.abspath(f"compressed_{level}.pdf")
        shutil.copy(final_out, safe_output)

        return safe_output, size_mb, level

    finally:
        shutil.rmtree(tmp, ignore_errors=True)
