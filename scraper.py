from urllib.request import urlopen
from lxml import html
from datetime import date

import requests
import bs4
import pandas as pd
import re
import algorithm as alg


some_companies = ["adyen", "stripe", "paypal"]


def lookup(company):
    return company.strip().replace(' ', '-')


def find_competitors(company, page):
    soup = bs4.BeautifulSoup(page.text, features="lxml")
    elements = soup.select('div.css-1uackhz')
    result = []
    for el in elements:
        result.append(el.get_text())
    return result


def find_companies_that_use(tree):
    company_tree = tree.xpath(
        "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div[2]/div[3]/div/strong[1]/text()")
    if type(company_tree) == list and len(company_tree) > 0:
        return int(company_tree[0])
    return None


def find_developers(tree):
    # follower_expression = re.compile(
    #     '(\d+) developers on StackShare have stated that they use')
    dev_tree = tree.xpath(
        "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div[4]/div[3]/strong[1]/text()")
    if type(dev_tree) == list and len(dev_tree) > 0:
        return int(dev_tree[0])
    return None


def find_integrations(tree):
    integration_tree = tree.xpath(
        "/html/body/div[1]/div[2]/div[1]/main/div/div/div[4]/div[3]/strong[6]/text()"
    )
    if type(integration_tree) == list and len(integration_tree) > 0:
        return int(integration_tree[0])
    return None


def find_followers(page):
    soup = bs4.BeautifulSoup(page.text, features="lxml")
    follower_section = soup.select('div.css-13sfqhu')
    follower_expression = re.compile(
        "(\d+) developers follow \w+")
    for section in follower_section:
        follower_text = section.get_text()
        if bool(re.search(follower_expression, follower_text)):
            match = re.search(follower_expression, follower_text)
            return match.group(1)
    return None


def scrape(company):
    company_name = lookup(company)
    url = "https://stackshare.io/" + company_name

    page = requests.get(url)
    tree = html.fromstring(page.content)
    result_dict = {}

    result_dict["name"] = company_name
    result_dict["date"] = date.today()
    result_dict["num_companies"] = find_companies_that_use(tree)
    result_dict["num_developers"] = find_developers(tree)
    result_dict["num_integrations"] = find_integrations(tree)
    result_dict["num_followers"] = find_followers(page)
    result_dict["competitors"] = find_competitors(company, page)

    return result_dict


def add_company(company, company_list):
    company_result = scrape(company)
    company_list.append(company_result)


def main():
    company_list = []
    for company in some_companies:
        add_company(company, company_list)
    df = pd.DataFrame(company_list)
    interesting_companies = alg.find_interesting_companies(df)
    print(interesting_companies)


if __name__ == "__main__":
    main()
