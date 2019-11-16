import requests

from bs4 import BeautifulSoup


class WikiSearch:
    def __init__(self, query, lang="en"):
        self.query = query.strip()
        self.lang = lang.lower().strip()
        self.api = "http://{}.wikipedia.org/w/api.php".format(self.lang)

    def get_page(self):
        params = {
            "prop": "text",
            "action": "parse",
            "page": self.query,
            "format": "json",
        }
        res = requests.get(self.api, params=params)
        page = res.json()["parse"]["text"]["*"]
        return page


if __name__ == "__main__":
    ws = WikiSearch("python")
    p = ws.get_page()
    print(p)
