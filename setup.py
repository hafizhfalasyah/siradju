from cx_Freeze import setup, Executable

setup(
    name="SIRADJU",
    version="1.0",
    executables=[Executable("main.py", icon="LOGO-JUNREJO.ico")]
)
