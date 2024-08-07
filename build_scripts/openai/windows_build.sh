#!/bin/sh
# Requireed installations
pip install ".[base]"
pip install '.[agentic]'
pip install pyinstaller==6.9.0


# Pyinstaller
pyinstaller --recursive-copy-metadata gpt_computer_assistant run.py --windowed --add-data="gpt_computer_assistant/utils/media/*":"gpt_computer_assistant/utils/media" --icon="gpt_computer_assistant/utils/media/icon.ico" --name="GPT Computer Assistant" --onefile

