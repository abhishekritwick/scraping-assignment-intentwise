# scraping-assignment-readme    

Steps to run the code:
- Go to the working directory where you clone the project
- Activate the virtualenv pushed along with the code : source venv/bin/activate (on mac)
- Incase you want to create your own virtualenv, use any tools like virtualenv, pipenv etc to create it and then activate it accordingly.
  You can install the dependencies using this command:
  pip install -r requirements.txt


- After the venv is activate you can see (venv) written on the terminal on the left side.
- You need to run the file scraper.py. Use this comaand to do so:
  python scraper.py
  It will ask you : What would you like to search on amazon today? 
  Provide the input string that you want to search on amazon.in (eg: learning toys)
  You will see the browser(chrome) window open and navigate to amazon.in and then search for the search term. 
  After it has loaded completely, the browser will shut and the data will be scraped and the result will be populated to the file
   "results.csv". By default the file contains the most recently scraped data. 
- By default it will scrape "testdata.html" which right now contains the most recently crawled page. 
- You can change the filename in which you want to save the html DOM and scrape from it in the config.py file using the FILENAME variable. 
- search_page.html and search_page_2.html are both the learning toys page saved at different times and have different xpaths(especially for sponsored products)
- Support is provided for both of them but in case the xpath comes different in a new hit, we wouldn't be able to capture that with the existing xpaths configured in the config.py file. 
- To enable scraping of an existing page, change the value of the variable "scrape_existing_page" to True in the __name__ == __main__ block. It is set to False by default, which will enable fresh crawl of the search page.



Please let me know if anything is unclear. 