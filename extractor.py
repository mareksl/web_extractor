import datetime
import io
import os
import sys
from ftplib import FTP

import pandas as pd
import requests


class Extractor:

    def __init__(self, config):
        self.protocol = config.get("protocol", "http")

        try:
            self.title = config["title"]

            if self.protocol == "http":
                self.url = config["url"]

            if self.protocol == "ftp":
                self.host = config["host"]

        except KeyError:
            sys.exit("Invalid configuration")

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

    def get_file(self):
        try:
            authentication = (
                (self.authentication["username"],
                 self.authentication["password"]) if self.authentication
                else None)
        except KeyError as e:
            sys.exit("Invalid authentication details: {}".format(e))

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
            sys.exit("Could not get file: {}".format(e))

        return data

    def extract_data(self, raw_data):
        csv_data = pd.read_csv(raw_data,
                               sep=self.separator)
        if self.filters:
            for key, value in self.filters.items():
                csv_data = csv_data[csv_data[key].isin(value)]

        if len(self.columns) > 0:
            csv_data = csv_data[self.columns]

        return csv_data.rename(
            columns=dict(
                zip(
                    self.columns,
                    self.aliases
                )
            ))

    def save_file(self, data):
        directory = "./{}".format(self.title)

        if not os.path.exists(directory):
            os.makedirs(directory)

        data.to_csv(
            "{}/{}_{}.csv".format(
                directory,
                self.title,
                self.date),
            index=False, encoding=self.encoding)
