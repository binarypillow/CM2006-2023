import os
import subprocess


def make_exe():
    """
    Makes an executable file using PyInstaller.
    """
    name = "run"
    os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}/..")
    subprocess.run(
        [
            "pyinstaller",
            f"{name}.py",
            "--onefile",
            "--noconsole",
            "--icon",
            "logo.ico",
            "--add-data",
            "app/resources;app/resources",
            "--clean",
        ]
    )
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    make_exe()

    print("Executable file created")
