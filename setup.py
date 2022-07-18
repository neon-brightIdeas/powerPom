import os
import subprocess
import sys

from sys import platform

# j_TODO : File path should be redone eventually
if platform == "linux" or platform == "linux2":
    print('Installing Proper Modules for Linux')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "./Tools/requirements_linux.txt", "--trusted-host", "pypi.org"])
elif platform == "darwin":
    # OS X
    print('This program is not currently compatible with Macs')
elif platform == "win32":
    # Windows...
    print('Installing Proper Modules for Windows')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "./Tools/requirements_windows.txt", "--trusted-host", "pypi.org"])
