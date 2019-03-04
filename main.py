import json
import sys

from halo import Halo
from pick import pick

from extractor import Extractor

path_to_config = "./config.json"


@Halo(text="Extracting", spinner="simpleDotsScrolling")
def extract_data():
    config = get_config(path_to_config)

    extractor = Extractor(config)

    raw_data = extractor.get_file()
    extracted_data = extractor.extract_data(raw_data)

    extractor.save_file(extracted_data)


def title_map(option):
    try:
        title = option["title"]
    except:
        sys.exit("Invalid configuration")
    return title


def get_config(path_to_config):
    with open(path_to_config) as f:
        config = json.load(f)
    prompt = 'Please choose data to extract:'

    (option, _) = pick(config, prompt, indicator="=>",
                       options_map_func=title_map)
    return option


def run_tool():
    prompt = 'What would you like to do?'
    (option, _) = pick(["Extract Data", "Exit"], prompt, indicator="=>")

    if option == "Exit":
        sys.exit("Bye!")

    if option == "Extract Data":
        extract_data()


if __name__ == "__main__":
    run_tool()
