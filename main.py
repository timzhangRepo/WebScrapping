import json
from bs4 import BeautifulSoup
import requests
from random import randint
import re

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# text = "This is the third largest oceans "
# url = 'http://www.search.yahoo.com/search?p=' + text
# request_result = requests.get(url, headers=USER_AGENT);
# soup = BeautifulSoup(request_result.text, "html.parser")
# results = soup.find_all("a", class_='ac-algo fz-l ac-21th lh-24')
# for result in results:
#     link = result.get("href")
#     if ("https://r.search.yahoo.com/" in link):
#         link = link.split("RU=")[1].split("/RK=2")[0].replace('%2f', '/').replace('%3a', ':')
#     print(link)

class SearchEngine:
    @staticmethod
    def search(query):
        temp_url = '+'.join(query.split())  # for adding + between words for the query
        url = "http://www.search.yahoo.com/search?p=" + temp_url + "&n=30"
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("a", class_='ac-algo fz-l ac-21th lh-24')
        Set = set()
        # implement a check to get only 10 resutls and also check that URLs must not be duplicated
        for result in raw_results:
            if (len(Set) >= 10): return Set;
            link = result.get('href')
            if("https://r.search.yahoo.com/" in link):
                link = link.split("RU=")[1].split("/RK=2")[0].replace('%2f', '/').replace('%3a', ':')
            Set.add(link)
        return Set
myResults = []
se = SearchEngine()
queries = open("100QueriesSet1.txt").read().splitlines(); #read from search query
count = 0;
for query in queries:
    count += 1
    print(count)
    result = []
    result.append(query)
    result.append(list(se.search(query)))
    myResults.append(result)
jsonString = json.dumps(myResults)
print(jsonString)
