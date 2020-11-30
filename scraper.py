from crawler import Browser
from bs4 import BeautifulSoup
import re
import argparse
import csv
from config import xpath_dict, FILENAME
'''
Methods to scrape the stored webpage and populate the csv file "results.csv" with 
all the required data present on the webpage. 
Data to  scrape from search page : 
(keyword, rank, asin, prod_desc, seller_company, strike_price,
display_price, rating_count, five_rating, badge, sponsored)
'''


def extract_text_from_regex(text, regex):
    try:
        pattern = re.compile(regex)
        found = pattern.findall(text)
        if found:
            return found[0]
    except:
        return None

DOM = None
dom_soup = None


def load_file():
    global DOM
    with open(FILENAME, "r") as file:
            DOM = file.read()


def get_keyword(soup):
    return soup.find(xpath_dict.get('keyword')).text()


def get_asin(soup):
    x = soup.find_all(attrs={"data-asin": re.compile(".*")})
    return (x[0].get('data-asin'))


def get_prod_desc(soup):
    prod_desc = " "
    if soup.select(xpath_dict.get('prod_desc')):
        title = soup.select(xpath_dict.get('prod_desc'))[0].text.strip()
        list_ = title.split()
        prod_desc = prod_desc.join(list_[1:])
        prod_desc = prod_desc.strip("-").strip("|").strip()
        return prod_desc
    return None


def get_seller_company(soup):
    seller = " "
    if soup.select(xpath_dict.get('seller_company')):
        title = soup.select(xpath_dict.get('seller_company'))[0].text.strip()
        list_ = title.split()
        seller = seller.join(list_[:1])
        return seller
    return None


def get_strike_price(soup):
    if soup.select(xpath_dict.get('strike_price')):
        return extract_text_from_regex(soup.select
                                       (xpath_dict.get('strike_price'))
                                       [0].text.strip(), r'(\d*,?\d+\.?\d*)')
    return None


def get_display_price(soup):
    if soup.select(xpath_dict.get('display_price')):
        return extract_text_from_regex(soup.select
                                       (xpath_dict.get('display_price'))
                                       [0].text.strip(), r'(\d*,?\d+\.?\d*)')
    return None


def get_rating_count(soup):
    sponsored_rating_xpath = ".a-icon.a-icon-star.a-star-4-5+span,.sb_3dDFIaal"
    if soup.select_one(sponsored_rating_xpath):
        return soup.select_one(sponsored_rating_xpath).text.strip()
    if soup.select(xpath_dict.get('rating_count')):
        return soup.select(xpath_dict.get('rating_count'))[0].text.strip()
    return None


def get_five_rating(soup):
    value = None
    sponsored_fiverating_xpath = ".a-icon.a-icon-star.a-star-4-5+span"
    if soup.select_one(sponsored_fiverating_xpath):
        value = soup.select_one(sponsored_fiverating_xpath).get("data-rt")
    if soup.find_all(attrs={"data-rating": re.compile(".*")}):
        rating = soup.find_all(attrs={"data-rating": re.compile(".*")})
        value = rating[0].get('data-rating')
    if soup.select(xpath_dict.get('five_rating')):
        value = soup.select(xpath_dict.get('five_rating'))[0].text.strip()
    
    if value and "out of" in value:
        value = extract_text_from_regex(value, r'(.*) out of')
    return value


def get_badge(soup):
    if soup.select(xpath_dict.get('badge')):
        return soup.select(xpath_dict.get('badge'))[0].text.strip()
    return None


def get_sponsored(soup):
    global dom_soup
    sponsored_div_xpath = \
        "._multi-card-creative-desktop_DesktopContainer_content__EgtBX,.sbx_mcd"

    if dom_soup.select(sponsored_div_xpath):
        sponsored_div = dom_soup.select(sponsored_div_xpath)[0]
        spo_divs = sponsored_div.select(
            "._multi-card-creative-desktop_DesktopGridColumn_gridColumn__2evuV,.sbx_mcd div[data-asin]")
        sponsored = soup.select("html>div")[0]
        for div in spo_divs:
            if div == sponsored:
                return True, True

    if soup.select(xpath_dict.get('sponsored')):
        if "sponsored" in soup.select(
                xpath_dict.get('sponsored'))[0].text.lower():
            return True, False
    return False, False


def get_html(text):
    return "<html>{}</html>".format(text)


def soupify(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def write_to_file(data):
    with open('results.csv', 'w') as result_file:
        result_writer = csv.writer(result_file,
                                   delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            result_writer.writerow(row)


def scrape_page():
    load_file()
    global dom_soup
    dom_soup = soupify(DOM)
    keyword = dom_soup.select(
                        xpath_dict.get('keyword'))[0].text.strip('"').strip()

    search_result_xpath = xpath_dict.get('search_results')
    results = dom_soup.select(search_result_xpath)

    result_list = []
    count = 1
    for result in results:
        result = get_html(result)
        results_soup = soupify(result)
        keyword = keyword
        asin = get_asin(results_soup)
        prod_desc = get_prod_desc(results_soup)
        seller_company = get_seller_company(results_soup)
        strike_price = get_strike_price(results_soup)
        display_price = get_display_price(results_soup)
        rating_count = get_rating_count(results_soup)
        five_rating = get_five_rating(results_soup)
        badge = get_badge(results_soup)
        sponsored = get_sponsored(results_soup)[0]
        isFromSponsoredDiv = get_sponsored(results_soup)[1]
        rank = count
        if isFromSponsoredDiv:
            rank = None
        result_list.append([keyword, rank, asin, prod_desc,
                            seller_company, strike_price, display_price,
                            rating_count, five_rating, badge, sponsored])
        if not isFromSponsoredDiv:
            count += 1
    write_to_file(result_list)


def main(search_term):
    search = str(search_term)
    browser = Browser()
    browser.open_website()
    browser.navigate_to_search_page(search)
    browser.save_HTML()
    scrape_page()


if __name__ == "__main__":
    search_term = input("What would you like to search on amazon today?\n")
    main(search_term)
