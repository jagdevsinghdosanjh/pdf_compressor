import os
import subprocess
import pikepdf
import tempfile

def gs_compress(input_path, output_path, quality):
    quality_map = {
        "high": "/ebook",      # 150 dpi
        "medium": "/screen",   # 72 dpi
        "aggressive": "/screen"
    }

    gs_quality = quality_map.get(quality, "/ebook")

    # command = [
    #     "gs",
    #     "-sDEVICE=pdfwrite",
    #     "-dCompatibilityLevel=1.4",
    #     f"-dPDFSETTINGS={gs_quality}",
    #     "-dDownsampleColorImages=true",
    #     "-dColorImageResolution=150" if quality == "high" else "-dColorImageResolution=100",
    #     "-dNOPAUSE",
    #     "-dQUIET",
    #     "-dBATCH",
    #     f"-sOutputFile={output_path}",
    #     input_path
    # ]

    command = [
    "gswin64c",
    "-sDEVICE=pdfwrite",
    "-dCompatibilityLevel=1.4",
    f"-dPDFSETTINGS={gs_quality}",
    "-dDownsampleColorImages=true",
    "-dColorImageResolution=150",
    "-dNOPAUSE",
    "-dQUIET",
    "-dBATCH",
    f"-sOutputFile={output_path}",
    input_path
]

    
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def optimize_with_pikepdf(input_path, output_path):
    pdf = pikepdf.open(input_path)
    pdf.save(output_path, optimize_version=True, compress_streams=True)


def linearize_with_qpdf(input_path, output_path):
    os.system(f"qpdf --linearize {input_path} {output_path}")


def compress_to_target(input_path, target_mb=7):
    compression_levels = ["high", "medium", "aggressive"]

    with tempfile.TemporaryDirectory() as tmp:
        current_input = input_path

        for level in compression_levels:
            gs_out = os.path.join(tmp, f"gs_{level}.pdf")
            pike_out = os.path.join(tmp, f"pike_{level}.pdf")
            final_out = os.path.join(tmp, f"final_{level}.pdf")

            # Step 1: Ghostscript
            gs_compress(current_input, gs_out, level)

            # Step 2: PikePDF optimization
            optimize_with_pikepdf(gs_out, pike_out)

            # Step 3: qpdf linearization
            linearize_with_qpdf(pike_out, final_out)

            size_mb = os.path.getsize(final_out) / (1024 * 1024)

            if size_mb <= target_mb:
                return final_out, size_mb, level

            current_input = final_out

        # If still above target, return last attempt
        return final_out, size_mb, "aggressive"
