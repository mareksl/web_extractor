import datetime
import io
import os
import re
import unicodedata
from ftplib import FTP

import pandas as pd
import requests
from halo import Halo
from termcolor import cprint, colored


class Extractor:

    def __init__(self, config, restart):
        self.restart = restart
        self.protocol = config.get("protocol", "http")

        try:
            self.title = config["title"]

            if self.protocol == "http":
                self.url = config["url"]

            if self.protocol == "ftp":
                self.host = config["host"]

        except KeyError:
            self.restart(colored("Invalid configuration", "red"))

        self.date_format = config.get("dateFormat", "%Y%m%d")
        self.authentication = config.get("authentication", None)
        self.encoding = config.get("encoding", "utf8")
        self.separator = config.get("separator", ";")
        self.columns = config.get("columns", [])
        self.aliases = config.get("aliases", [])
        self.filters = config.get("filters", None)
        self.filename = config.get("filename", None)

        self.date = self.__set_date()

    def __set_date(self):
        now = datetime.datetime.now()
        return now.strftime(self.date_format)

    def __get_file_ftp(self, ftp, filename):
        output = io.BytesIO()
        ftp.retrbinary('RETR ' + filename, output.write)
        ftp.quit()
        output.seek(0)
        byte_str = output.read()
        decoded = byte_str.decode(self.encoding)
        return io.StringIO(decoded)

    def __slugify(self, value):
        """
        Convert to ASCII if 'allow_unicode' is False.
        Convert spaces to hyphens.
        Remove characters that aren't alphanumerics, underscores, or hyphens.
        Convert to lowercase. Also strip leading and trailing whitespace.
        """
        value = str(value)
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)

    def get_file(self):
        spinner = Halo(text='Getting File', spinner='simpleDotsScrolling')
        spinner.start()
        try:
            authentication = (
                (self.authentication["username"],
                 self.authentication["password"]) if self.authentication
                else None)
        except KeyError as e:
            spinner.stop()
            self.restart(
                colored("Invalid authentication details: {}".format(e), "red"))

        try:
            if self.protocol == "http":
                data_file = requests.get(
                    self.url.format(date=self.date),
                    auth=authentication
                ).content
                data = io.StringIO(data_file.decode(self.encoding))
                # data_file = open("./dummy_data/TradedInstrument.txt",
                #                  "r", encoding=self.encoding)
                # data = data_file
            if self.protocol == "ftp":
                ftp = FTP(self.host)
                if authentication:
                    ftp.login(authentication[0], authentication[1])
                data = self.__get_file_ftp(ftp, self.filename)

        except Exception as e:
            spinner.stop()
            self.restart(colored("Could not get file: {}".format(e), "red"))

        spinner.stop()
        return data

    def extract_data(self, raw_data):
        spinner = Halo(text='Extracting', spinner='simpleDotsScrolling')
        spinner.start()
        try:
            csv_data = pd.read_csv(raw_data,
                                   sep=self.separator)
            if self.filters:
                for key, value in self.filters.items():
                    csv_data = csv_data[csv_data[key].isin(value)]

            if len(self.columns) > 0:
                csv_data = csv_data[self.columns]

            spinner.stop()
            return csv_data.rename(
                columns=dict(
                    zip(
                        self.columns,
                        self.aliases
                    )
                ))
        except Exception as e:
            spinner.stop()
            self.restart(
                colored("Unable to extract data: {}".format(e), "red"))

    def save_file(self, data):
        spinner = Halo(text='Saving', spinner='simpleDotsScrolling')
        spinner.start()
        filename_slug = self.__slugify(self.title)
        directory = "./output/{}".format(filename_slug)

        if not os.path.exists(directory):
            os.makedirs(directory)

        data.to_csv(
            "{}/{}_{}.csv".format(
                directory,
                filename_slug,
                self.date),
            index=False, encoding=self.encoding)
        spinner.stop()
        self.restart(colored('Successfully extracted data!', "green"))
