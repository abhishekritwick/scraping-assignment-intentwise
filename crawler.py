import time
from selenium import webdriver
from config import PATH, FILENAME

class Browser():
    '''
    Class to open the browser(chrome), navigate to amazon.in,
    query the search string 
    and save the web page
    '''

    def __init__(self):
        self.browser = webdriver.Chrome(PATH)
        self.url = "https://www.amazon.in"
        

    def open_website(self):
        self.browser.get(self.url)
        return


    def navigate_to_search_page(self, search_str):
        time.sleep(2)
        search_bar = self.browser.find_element_by_css_selector("#twotabsearchtextbox")
        search_bar.send_keys(str(search_str))
        search_btn = self.browser.find_element_by_css_selector("#nav-search-submit-text input")
        search_btn.click()
        return


    def save_HTML(self):
        time.sleep(2)
        with open(FILENAME,"w") as file:
            file.write(str(self.__HTML)) 
        self.browser.quit()


    @property
    def __HTML(self):
        return self.browser.page_source


# browser = Browser()
# browser.open_website()
# browser.navigate_to_search_page("learning toys")
# browser.save_HTML()