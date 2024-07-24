import re
import subprocess
import sys


def convert_docx_to_pdf(dest_folder, source_file_path, timeout=None):
    try:
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', dest_folder, source_file_path]

        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

        if process.returncode != 0:
            error_message = f"LibreOffice conversion failed. stderr: {process.stderr.decode()}"
            raise LibreOfficeError(error_message)

        return "Conversion successful"

    except subprocess.TimeoutExpired as timeout_error:
        raise LibreOfficeError(f"LibreOffice conversion timed out: {timeout_error}")

    except Exception as e:
        raise LibreOfficeError(f"Error during LibreOffice conversion: {str(e)}")


def libreoffice_exec():
    # TODO: Provide support for more platforms
    if sys.platform == 'darwin':
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    return 'libreoffice'


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output
