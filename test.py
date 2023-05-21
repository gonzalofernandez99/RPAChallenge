
from RPA.Browser.Selenium import Selenium

from datetime import datetime


from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import shutil

def main():
    browser = Selenium()
    url = "https://www.nytimes.com/search?query=tesla"
    carpeta = 'C:\\Users\\ferna\\OneDrive\\Desktop\\RPAChallenge\\output\\drink-05-06-2023'
    carpetazip = 'C:\\Users\\ferna\\OneDrive\\Desktop\\RPAChallenge\\output\\drink-05-06-2023'
    #open_nytimes(url,browser)
    #time.sleep(2)
    #click_show_more(browser)

    #create directory according to month, day, and year, return the file name with the path + phrase + full hour + file extension.#
    path_directory = "output"
    phrase = "tesla"
    ext = "txt"
    now = datetime.now()
    date = now.strftime('%m-%d-%Y')
    hours_and_minutes = now.strftime('%H%M%S-%f')
    directorycompleto =os.path.join(path_directory,phrase+"-"+date)
    print(directorycompleto)
    artifacts_dir = os.path.join(os.getcwd(),directorycompleto)
    name_excel = phrase+date+hours_and_minutes+"."+ext
    Excel = os.path.join(artifacts_dir, name_excel)
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)
    
    return Excel
if __name__ == "__main__":
    main()