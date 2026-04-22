import os
import subprocess
import pikepdf
import tempfile

def compress_with_ghostscript(input_path, output_path, quality="high"):
    quality_map = {
        "high": "/ebook",      # 150 dpi – best for <7MB
        "medium": "/screen",   # 72 dpi
        "max": "/printer"      # 300 dpi (larger)
    }

    gs_quality = quality_map.get(quality, "/ebook")

    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_quality}",
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


def compress_pdf(input_path, quality="high"):
    with tempfile.TemporaryDirectory() as tmp:
        gs_out = os.path.join(tmp, "gs.pdf")
        pike_out = os.path.join(tmp, "pike.pdf")
        final_out = os.path.join(tmp, "final.pdf")

        compress_with_ghostscript(input_path, gs_out, quality)
        optimize_with_pikepdf(gs_out, pike_out)
        linearize_with_qpdf(pike_out, final_out)

        return final_out
