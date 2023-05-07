from datetime import datetime
from pathlib import Path
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def create_file_directory(path_directory,phrase,ext):
    #create directory according to month, day, and year, return the file name with the path + phrase + full hour + file extension.#
    now = datetime.now()
    date = now.strftime('%m-%d-%Y')
    hours_and_minutes = now.strftime('%H%M%S-%f')
    directory = path_directory+"\\"+phrase+"-"+date
    file = directory+"\\"+phrase+date+hours_and_minutes+"."+ext
    Path(directory).mkdir(exist_ok=True)
    
    return file

def contains_amount(title, description):
    # Patterns for the money amount formats#
    #Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD#
    patterns = [
        r'\$\d{1,3}(?:,\d{3})*\.\d{2}',  # Example: $111,111.11
        r'\$\d{1,3}(?:,\d{3})*',         # Example: $11.1
        r'\d+\s+dollars',                # Example: 11 dollars
        r'\d+\s+USD'                     # Example: 11 USD
    ]

    for pattern in patterns:
        if re.search(pattern, title) or re.search(pattern, description):
            return True

    return False

def get_date(Number):
    #Gets today's date and the date N months ago.#
    #postcondition: Returns the formatted current date as the first argument and the formatted date according to the input data as the second argument. #
    #Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on#
    today = datetime.now()

    if Number == 0 or Number == 1:
        date = today.replace(day=1)
    else:
        months_ago = Number - 1
        date = today.replace(day=1) - relativedelta(months=months_ago)
        
    formatted_date = date.strftime("%m/%d/%Y")
    formatted_today = today.strftime('%m/%d/%Y')
    return formatted_today,formatted_date