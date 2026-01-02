import subprocess
from pathlib import Path

def export_xopp_to_pdf(directory="."):
    directory = Path(directory)

    xopp_files = list(directory.glob("*.xopp"))

    if not xopp_files:
        print("No se encontraron archivos .xopp")
        return

    for xopp_file in xopp_files:
        pdf_file = xopp_file.with_suffix(".pdf")

        cmd = [
            "xournalpp",
            f"--create-pdf={pdf_file}",
            str(xopp_file)
        ]

        print(f"Exportando: {xopp_file.name} → {pdf_file.name}")

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Error con {xopp_file.name}")
            print(e.stderr.decode())

    print("✅ Exportación finalizada")

if __name__ == "__main__":
    export_xopp_to_pdf(".")
