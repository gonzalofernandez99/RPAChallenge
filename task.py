from RPA.Browser.Selenium import Selenium
import time
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import urllib.request
import re
from function import create_file_directory
from function import contains_amount
from openpyxl import Workbook

## constant ##
browser = Selenium()

def open_nytimes(url):
    #Opens the browser and loads the provided URL.
    
    browser.open_available_browser(url)
    browser.maximize_browser_window()

def search_for(pharase): 
    #Searches for the provided phrase on the website.
    
    button_search = "xpath://button[@data-test-id='search-button']"
    input_pharase = "xpath://input[@data-testid='search-input']"
    
    browser.wait_until_element_is_visible(button_search)
    browser.click_element(button_search)
    browser.wait_until_element_is_visible(input_pharase)
    browser.input_text(input_pharase,pharase)
    browser.press_keys(input_pharase,"ENTER")
    
def get_date(Number):
    #Gets today's date and the date N months ago.
    today = datetime.now()

    if Number == 0 or Number == 1:
        date = today.replace(day=1)
    else:
        months_ago = Number - 1
        date = today.replace(day=1) - relativedelta(months=months_ago)
        
    formatted_date = date.strftime("%m/%d/%Y")
    formatted_today = today.strftime('%m/%d/%Y')
    return formatted_today,formatted_date

def apply_date(today,date):
    #Applies the date range in the search filter.
    
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
   
def apply_section(category):
    #Applies the provided sections to the search filter.
    counter_section = 0
    list_category = convert_string_to_list(category)
    button_section = "xpath://button[@data-testid='search-multiselect-button']"
    
    
    browser.wait_until_element_is_visible(button_section)
    browser.click_element(button_section)
    
    time.sleep(2)
    
    for section in list_category:
        input_seccion = f"xpath://span[text()='{section}']"
        try:
            browser.wait_until_element_is_visible(input_seccion,timeout=1)
            browser.click_element(input_seccion)
            counter_section +=1
        except Exception as e:
            print(f"Error finding the section: {section} : {e}")
            
    return counter_section
    

def click_show_more():
    #Clicks the 'Show more' button until there are no more results.
    time_out = 10
    show_more_button= "xpath://button[@data-testid='search-show-more-button']"
    
    time.sleep(2)
   
    while(browser.is_element_enabled(show_more_button,time_out)):
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
        
    # Save the Excel file
    wb.save(name_file)
      
def load_news(pharase,directory):
    #Loads the news and extracts relevant information.
    
    element_title = "xpath://h4[@class='css-2fgx4k']"
    element_date = "xpath://span[@data-testid='todays-date']"
    element_description = "xpath://p[@class='css-16nhkrn']"
    element_img = "xpath://img[@class='css-rq4mmj']"
    
    result = []
    click_show_more()
    
    browser.wait_until_page_contains_element(element_date)
    titles = browser.find_elements(element_title)
    descriptions = browser.find_elements(element_description)
    imagenes = browser.find_elements(element_img)
    dates = browser.find_elements(element_date)
    
    for i in range(len(titles)):
        title = titles[i].text
        description = descriptions[i].text
        date = dates[i+1].text
        src_imagen = imagenes[i].get_attribute("src")
        
        name_file = create_file_directory(directory,pharase,"jpg")
        print(name_file)
        download_image(src_imagen, name_file)
        
        number_of_phrases = len(re.findall(pharase, title + description, re.IGNORECASE))
        contains_money = contains_amount(title,description)
        
        result.append({
            "title":title,
            "date":date,
            "description":description,
            "name_file":name_file,
            "number_of_phrases":number_of_phrases,
            "contains_money":contains_money
        })
        
    load_excel(pharase,directory,result)

# Define a main() function that calls the other functions in order:
def main():
    url = "https://www.nytimes.com/"
    date_number = 0
    pharase = "Biden"
    categories = "U.S.,New York,Business" 
    directory = "output"
    try:
        today,last=get_date(date_number)
        open_nytimes(url)
        search_for(pharase)
        apply_date(today,last)
        counter_section=apply_section(categories)
        if counter_section != 0:
            load_news(pharase,directory)
        else:
            print("No se ingreso ninguna categoria valida")
    except TimeoutError as te:
        print("Error: A TimeoutError occurred: ",te)
    except Exception as e:
        print("Error: An unexpected error occurred: ", e)
    finally:
        
        browser.close_all_browsers()
    
# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()

