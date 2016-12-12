from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen

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
            kwargs['users'] = int(data[3])
            kwargs['load'] = float(data[4])

            host = Host(kwargs)
            hosts.append(host)

        return hosts

s = Scraper('http://apps.cs.utexas.edu/unixlabstatus/')
s.parse_html()
