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

    def __init__(self, **kwargs: dict) -> None:
        for k in kwargs:
            if k not in self.ALLOWED_KEYS:
                raise AttributeError

        self.name = kwargs.get('name')
        self.status = self.__status(kwargs.get('status'))
        self.uptime = self.__uptime(kwargs.get('uptime'))
        self.users = self.__users(kwargs.get('users'))
        self.load = self.__load(kwargs.get('load'))

    def __status(self, status):
        if status == 'up':
            return True
        if status == 'down':
            return False

    def __uptime(self, uptime):
        if not '+' in uptime:
            return 0
        else:
            hour = uptime.split('+')[0]
            return int(hour)

    def __users(self, users):
        if len(users) == 0:
            return 0
        else:
            return int(users)

    def __load(self, load):
        if len(load) == 0:
            return 0.0
        else:
            return float(load)

class Scraper:

    PARSER = 'html.parser'

    def __init__(self, url):
        self.url = url
        self.hosts = []
        self.timestamp = ''

    def __get_soup(self):
        html = urlopen(self.url)
        soup = BeautifulSoup(html, self.PARSER)
        return soup

    def __parse_html(self):
        soup = self.__get_soup()
        rows = soup.find_all('tr')

        for _ in rows[0].children:
            time = _.get_text()
            self.timestamp = time

        for i in range(3, len(rows)):
            data = []
            for row in rows[i].children:
                if type(row) != NavigableString:
                    text = row.get_text()
                    data.append(text)

            host = Host(name=data[0], status=data[1], uptime=data[2],
                users=data[3], load=data[4])
            self.hosts.append(host)

    def get_hosts(self):
        return self.hosts

    def get_timestamp(self):
        return self.timestamp

    def update(self):
        self.__parse_html()
