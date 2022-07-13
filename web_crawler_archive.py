#!/usr/bin/env python
# coding: utf-8

# In[20]:
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re,os
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as ex

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')
def main():
    getpath=get_download_path()
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
    "download.default_directory": getpath, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })


    # In[17]:

    
        #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    print("Enter your query: ")
    str1=str(input())
    search = str1.replace(" ","")
    driver.get('https://archive.org/details/digitallibraryindia?query='+search+'&and[]=languageSorter%3A%22Bengali%22')


    # In[16]:


    pattern = re.compile('https://archive.org/details/in.ernet.dli+')
    try:
        elems = driver.find_elements("xpath","//a[@href]")
        catalog=[]

        for elem in elems:
          if elem is not None:
             if re.match(pattern,elem.get_attribute("href")):
                catalog.append(elem.get_attribute("href"))
                print(elem.get_attribute("href"))
          else:
            print("There is nothing to download. Search Again!")
    except ex.WebDriverException as ex:
        print("Restart the program")


    # In[21]:



    try:
        for link in catalog:

            driver.get(link)
            lnk=driver.find_element("xpath","//a[contains(@href,'.pdf')]")
            print(lnk.get_attribute("href"))
            driver.get(lnk.get_attribute("href"))

    except (ex.NoSuchWindowException,ex.WebDriverException) as err:
            print("The window is closed or Chrome is not reachable. Restart the program")
            driver.quit()

if __name__ =="__main__":
    main()
# In[ ]:




