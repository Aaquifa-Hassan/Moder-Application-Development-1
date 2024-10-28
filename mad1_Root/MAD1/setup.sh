#!/bin/bash

# Check if the virtual environment exists
if [ -d "myenv" ]; then
    # Activate the virtual environment
    source myenv/bin/activate
else
    # Create a virtual environment
    python3 -m venv myenv
    # Activate the virtual environment
    source myenv/bin/activate
    # Install requirements
    pip install -r requirements.txt
fi

file_path="/instance/library.sqlite3"

# Check if the file does not exist
if [ ! -f "$file_path" ]; then
    python3 createDatabase.py
fi 

python3 main.py
