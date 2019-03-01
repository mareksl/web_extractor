import datetime
import io
import os
import sys

import pandas as pd
import requests


class Extractor:

    def __init__(self, config):
        try:
            self.config = config["title"]
        except KeyError:
            sys.exit("Invalid Configuration. Please refer to documentation")

        self.date = self.__set_date()

    def __set_date(self):
        now = datetime.datetime.now()
        return now.strftime(self.config["dateFormat"])

    def get_file(self):
        data_file = requests.get(
            self.config["url"].format(date=self.date),
            auth=(
                self.config["authentication"]["username"],
                self.config["authentication"]["password"])
        ).content

        return io.StringIO(data_file.decode(self.config["encoding"]))

    def extract_data(self, raw_data):
        csv_data = pd.read_csv(raw_data,
                               sep=self.config["separator"])

        d = csv_data[["isin", "securityTypeDesc", "billingSegmentDesc"]]

        security_types = self.config["filter"]["securityTypeDesc"]

        filtered = d[d["securityTypeDesc"].isin(security_types)]

        return filtered[self.config["columns"]].rename(
            columns=dict(
                zip(
                    self.config["columns"],
                    self.config["aliases"]
                )
            ))

    def save_file(self, data):
        directory = "./{}".format(self.config["title"])

        if not os.path.exists(directory):
            os.makedirs(directory)

        data.to_csv(
            "{}/{}_{}.csv".format(
                directory,
                self.config["title"],
                self.date),
            index=False)
