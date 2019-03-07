import io
from ftplib import FTP

import requests


class FileFetcher:
    @staticmethod
    def create(protocol, url, host, filename):
        if protocol == 'ftp':
            return FileFetcherFTP(host, filename)
        elif protocol == 'http':
            return FileFetcherHTTP(url)
        else:
            raise ValueError(protocol)


class FileFetcherFTP:
    def __init__(self, host, filename):
        self.host = host
        self.filename = filename

    def fetch(self, auth=None):
        ftp = FTP(self.host)

        if auth:
            ftp.login(auth["username"], auth["password"])

        output = io.BytesIO()
        ftp.retrbinary('RETR ' + self.filename, output.write)
        ftp.quit()

        output.seek(0)
        content = output.read()

        return content


class FileFetcherHTTP:
    def __init__(self, url):
        self.url = url

    def fetch(self, auth=None):
        if auth:
            auth = (auth["username"], auth["password"])

        data_file = requests.get(
            self.url,
            auth
        )
        content = data_file.content

        return content
