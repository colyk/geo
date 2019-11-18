import requests

from bs4 import BeautifulSoup


class Wiki:
    __slots__ = ("query", "lang", "api", "page")

    def __init__(self, query: str, lang: str = "en"):
        self.query = query.strip()
        self.lang = lang.lower().strip()
        self.api = "https://{}.wikipedia.org/w/api.php".format(self.lang)

    def get_page(self) -> str:
        params = {
            "prop": "text",
            "action": "parse",
            "page": self.query,
            "format": "json",
        }
        res = requests.get(self.api, params=params)
        page = res.json()["parse"]["text"]["*"]
        return page

    def get_infobox(self):
        params = {
            "prop": "revisions",
            "action": "query",
            "rvprop": "content",
            "rvsection": "0",
            "titles": self.query,
            "format": "json",
            "uselang": "en",
        }
        res = requests.get(self.api, params=params)
        soup = BeautifulSoup(res, "html.parser")


if __name__ == "__main__":
    ws = Wiki("ukraina", lang="pl")
    p = ws.get_page()
    ws.get_infobox()
