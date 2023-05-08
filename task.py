from RPA.Browser.Selenium import Selenium
import time
import urllib.request
import re
from function import create_file_directory
from function import contains_amount
from function import get_date
from openpyxl import Workbook
import json


def init_config(path):
    with open(path, "r") as f:
        config = json.load(f)
    return config
    
def open_nytimes(url,browser):
    #Opens the browser and loads the provided URL.
    
    browser.open_available_browser(url)
    browser.maximize_browser_window()

def search_for(pharase,browser): 
    #Searches for the provided phrase on the website.
    
    button_search = "xpath://button[@data-test-id='search-button']"
    input_pharase = "xpath://input[@data-testid='search-input']"
    
    browser.wait_until_element_is_visible(button_search)
    browser.click_element(button_search)
    browser.wait_until_element_is_visible(input_pharase)
    browser.input_text(input_pharase,pharase)
    browser.press_keys(input_pharase,"ENTER")
    


def apply_date(today,date,browser):
    #Applies the date range in the search filter.
    #Precondition: The current date and the date obtained in 'get_date' are entered as arguments.#
    
    button_date = "xpath://button[@data-testid='search-date-dropdown-a']"
    label_dates = "xpath://button[@aria-label='Specific Dates']"
    input_date = "xpath://input[@id='startDate']"
    input_today = "xpath://input[@id='endDate']"
    
    browser.wait_until_element_is_visible(button_date)
    browser.click_element(button_date)
    browser.wait_until_element_is_visible(label_dates)
    browser.click_element(label_dates)
    browser.wait_until_element_is_visible(input_date)
    browser.input_text(input_date,date)
    browser.input_text(input_today,today)
    browser.press_keys(input_today,"ENTER")
    
def convert_string_to_list(Category):
    #Converts a comma-separated string of categories into a list.
    return ["Any"] if not Category else Category.split(',')
   
def apply_section(category,browser):
    #Applies the provided sections to the search filter.
    #Precondition: The categories in which the search is to be performed are entered#
    #Postcondition: Returns the number of times the categories were successfully selected. If it remains at 0, it means that no valid category was selected#
    counter_section = 0
    list_category = convert_string_to_list(category)
    button_section = "xpath://button[@data-testid='search-multiselect-button']"
    
    
    browser.wait_until_element_is_visible(button_section)
    browser.click_element(button_section)
    
    time.sleep(1)
    
    for section in list_category:
        input_seccion = f"xpath://span[text()='{section}']"
        try:
            browser.wait_until_element_is_visible(input_seccion,timeout=1)
            browser.click_element(input_seccion)
            counter_section +=1
        except Exception:
            print(f"Error finding the section: {section}")
            
    return counter_section
    

def click_show_more(browser):
    #Clicks the 'Show more' button until there are no more results.#
    #Postcondition: If the 'Show More' button does not appear, it means that the entire page has already been loaded.#
    timeout = 10
    show_more_button= "xpath://button[@data-testid='search-show-more-button']"
    
    time.sleep(2)
   
    while(browser.is_element_enabled(show_more_button,timeout)):
        browser.set_focus_to_element(show_more_button)
        browser.click_element(show_more_button)
        time.sleep(2)
        
def download_image(url, nombre_archivo):
    #Downloads the image from the provided URL and saves it with the given file name.
    urllib.request.urlretrieve(url, nombre_archivo)

def load_excel(pharase,directory,result):
    #Creates and saves an Excel file with the search results.
    
    name_file = create_file_directory(directory,pharase,"xlsx")
    wb = Workbook()
    ws = wb.active
    ws.append(["title", "date", "description", "name_file", "number_of_phrases", "contains_money"])
    for res in result:
        ws.append([
            res["title"],
            res ["date"],
            res["description"],
            res["name_file"],
            res["number_of_phrases"],
            res["contains_money"]
            ])
        
    wb.save(name_file)
      
def extract_news_data(titles, descriptions, images, dates, phrase, directory):
    #Information is obtained to later load it into the Excel file. The images are also saved in the 'download_image' function#
    #Precondition: All the necessary information from the news articles is entered as arguments#
    #Postcondition: Returns the list with all the loaded data to be entered into the Excel file.#
    news_data = []

    for i in range(len(titles)):
        title = titles[i].text
        description = descriptions[i].text
        date = dates[i+1].text
        src_image = images[i].get_attribute("src")
        
        name_file = create_file_directory(directory, phrase, "jpg")
        download_image(src_image, name_file)
        
        number_of_phrases = len(re.findall(phrase, title + description, re.IGNORECASE))
        contains_money = contains_amount(title, description)
        
        news_data.append({
            "title": title,
            "date": date,
            "description": description,
            "name_file": name_file,
            "number_of_phrases": number_of_phrases,
            "contains_money": contains_money
        })

    return news_data


def load_news(phrase, directory,browser):
    # Obtains all the necessary data from the news articles: title, description, images, and dates.#
    #Precondition: Receives the used @phrase and the @directory as arguments where the files and images will be saved#
    #Postcondition: Loads the information into the extract_news_data function and then saves it to an Excel file#

    element_title = "xpath://h4[@class='css-2fgx4k']"
    element_date = "xpath://span[@data-testid='todays-date']"
    element_description = "xpath://p[@class='css-16nhkrn']"
    element_img = "xpath://img[@class='css-rq4mmj']"

    click_show_more(browser)
    
    browser.wait_until_page_contains_element(element_date)
    titles = browser.find_elements(element_title)
    descriptions = browser.find_elements(element_description)
    images = browser.find_elements(element_img)
    dates = browser.find_elements(element_date)
    
    news_data = extract_news_data(titles, descriptions, images, dates, phrase, directory)
    load_excel(phrase, directory, news_data)

def main():
    browser = Selenium()
    config=init_config("devdata\env.json")
    url = config["URL"]
    date_number = config["DATE_NUMBER"]
    pharase = config["PHARASE"]
    categories = config["CATEGORIES"] 
    directory = config["DIRECTORY"] 
    try:
        today,last=get_date(date_number)
        open_nytimes(url,browser)
        search_for(pharase,browser)
        apply_date(today,last,browser)
        counter_section=apply_section(categories,browser)
        if counter_section != 0:
            load_news(pharase,directory,browser)
        else:
            print("No se ingreso ninguna categoria valida")
    except TimeoutError as te:
        print("Error: A TimeoutError occurred: ",te)
    except Exception as e:
        print("Error: An unexpected error occurred: ", e)
    finally:
        
        browser.close_all_browsers()
    
if __name__ == "__main__":
    main()