from datetime import datetime
from pathlib import Path
import re

def create_file_directory(path_directory,phrase,ext):
    """create directory according to month, day, and year, return the file name with the path + phrase + full hour + file extension."""
    now = datetime.now()
    date = now.strftime('%m-%d-%Y')
    hours_and_minutes = now.strftime('%H%M%S-%f')
    directory = path_directory+"\\"+phrase+"-"+date
    file = directory+"\\"+phrase+date+hours_and_minutes+"."+ext
    Path(directory).mkdir(exist_ok=True)
    
    return file

def contains_amount(title, description):
    # Patterns for the money amount formats
    patterns = [
        r'\$\d{1,3}(?:,\d{3})*\.\d{2}',  # Example: $111,111.11
        r'\$\d{1,3}(?:,\d{3})*',         # Example: $11.1
        r'\d+\s+dollars',                # Example: 11 dollars
        r'\d+\s+USD'                     # Example: 11 USD
    ]

    for pattern in patterns:
        if re.search(pattern, title) or re.search(pattern, description):
            return "True"

    return "False"
