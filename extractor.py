import datetime
import os

import pandas as pd
from halo import Halo
from termcolor import colored, cprint

from file_fetcher import FileFetcher
from utils import decode_content, slugify


class Extractor:

    def __init__(self, config, restart):
        self.restart = restart
        try:
            self.title = config["title"]
        except KeyError:
            self.restart(
                colored("Invalid configuration. Title missing.", "red"))

        self.protocol = config.get("protocol", "http")

        self.url = config.get("url", None)
        self.__build_url_date()

        self.host = config.get("host", None)
        self.filename = config.get("filename", None)

        if self.url is None and (self.host is None or self.filename is None):
            self.restart(
                colored(
                    "Invalid configuration. Check url or host and filename.",
                    "red")
            )

        self.date_format = config.get("dateFormat", "%Y%m%d")
        self.authentication = config.get("authentication", None)
        self.encoding = config.get("encoding", "utf8")
        self.separator = config.get("separator", ";")
        self.columns = config.get("columns", [])
        self.aliases = config.get("aliases", [])
        self.filters = config.get("filters", None)

        self.date = self.__set_date()

    def __set_date(self):
        now = datetime.datetime.now()
        return now.strftime(self.date_format)

    def __build_url_date(self):
        if self.url:
            self.url = self.url.format(date=self.date)

    def get_file_contents(self):
        spinner = Halo(text='Getting File', spinner='simpleDotsScrolling')
        spinner.start()

        try:
            fetcher = FileFetcher.create(
                self.protocol, self.url, self.host, self.filename)
            data = fetcher.fetch(self.authentication)
            decoded_data = decode_content(data, self.encoding)
            # data_file = open("./dummy_data/TradedInstrument.txt",
            #                  "r", encoding=self.encoding)
            # data = data_file

        except Exception as e:
            spinner.stop()
            self.restart(colored("Could not get file: {}".format(e), "red"))

        spinner.stop()
        return decoded_data

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
        filename_slug = slugify(self.title)
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
