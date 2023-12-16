import subprocess
import glob
import re


def compile_ui(input_file: str, output_file: str):
    """
    Compiles a Qt Designer UI file into a Python module.

    Args:
        input_file (str): The path to the input UI file.
        output_file (str): The path to the output Python file.
    """
    command = ["pyuic6", "-x", input_file, "-o", output_file]
    subprocess.run(command)


if __name__ == "__main__":
    # Get all .ui files in the 'ui' directory
    ui_files = glob.glob("../app/ui/*.ui")

    # Run compile_ui for each .ui file
    for ui_file in ui_files:
        python_file = ui_file.replace(".ui", ".py")
        compile_ui(ui_file, python_file)

        # Fix the path to resources in compiled files
        with open(python_file, "r+") as file:
            content = file.read()
            content = re.sub(
                r"from PyQt6 import QtCore, QtGui, QtWidgets",
                "from PyQt6 import QtCore, QtGui, QtWidgets\nfrom app.utils import get_abs_path",
                content,
            )
            content = re.sub(
                r'"../app/ui\\\\../',
                'get_abs_path("',
                re.sub(r'("../app/ui\\\\../.*?")', r"\1)", content),
            )
            file.seek(0)
            file.write(content)
            file.truncate()

    print(".ui files compiled to python!")
