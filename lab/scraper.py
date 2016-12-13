from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen

class Host:

    ALLOWED_KEYS = [
        'name',
        'status',
        'uptime',
        'users',
        'load'
    ]

    def __init__(self, **kwargs):
        for k in kwargs:
            if k not in self.ALLOWED_KEYS:
                raise AttributeError

        self.name = kwargs.get('name')

        self.status = kwargs.get('status')
        if self.status == 'up':
            self.status = True
        elif self.status == 'down':
            self.status = False

        self.uptime = kwargs.get('uptime')

        self.users = kwargs.get('users')
        if len(self.users) == 0:
            self.users = 0
        else:
            self.users = int(self.users)

        self.load = kwargs.get('load')
        if len(self.load) == 0:
            self.load = 0.0
        else:
            self.load = float(self.load)

class Scraper:

    PARSER = 'html.parser'

    def __init__(self, url: str):
        self.url = url

    def get_soup(self):
        html = urlopen(self.url)
        soup = BeautifulSoup(html, self.PARSER)
        return soup

    def parse_html(self):
        soup = self.get_soup()
        hosts = []

        rows = soup.find_all('tr')
        for i in range(3, len(rows)):
            data = []
            kwargs = {}

            for row in rows[i].children:
                if type(row) != NavigableString:
                    text = row.get_text()
                    data.append(text)

            for i in range(len(data)):
                key = Host.ALLOWED_KEYS[i]
                kwargs[key] = data[i]

            host = Host(**kwargs)
            hosts.append(host)

        return hosts
