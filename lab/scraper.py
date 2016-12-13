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
            if k in self.ALLOWED_KEYS:
                setattr(self, k, kwargs.get(k))

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

            kwargs['name'] = data[0]

            status = data[1]
            if status == 'up':
                kwargs['status'] = True
            elif status == 'down':
                kwargs['status'] = False

            kwargs['uptime'] = data[2]

            users = data[3]
            if len(users) == 0:
                kwargs['users'] = 0
            else:
                kwargs['users'] = int(data[3])

            load = data[4]
            if len(load) == 0:
                kwargs['load'] = 0
            else:
                kwargs['users'] = float(data[4])

            host = Host(**kwargs)
            hosts.append(host)

        return hosts
