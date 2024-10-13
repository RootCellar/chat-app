#!/bin/sh
pyinstaller bin/client.py --onefile --paths .
pyinstaller bin/server.py --onefile --paths .
