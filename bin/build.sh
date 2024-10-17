#!/bin/sh
pyinstaller bin/client.py --collect-submodules nacl --collect-submodules cffi --onefile --paths .
pyinstaller bin/server.py --collect-submodules nacl --collect-submodules cffi --onefile --paths .
