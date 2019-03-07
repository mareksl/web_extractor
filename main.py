import json
import os
import sys
import time
import msvcrt

from pick import pick
from termcolor import cprint, colored

from extractor import Extractor


path_to_config = "./config.json"


def extract_data():
    config = get_config(path_to_config)
    extractor = Extractor(config, restart)

    raw_data = extractor.get_file_contents()
    extracted_data = extractor.extract_data(raw_data)

    extractor.save_file(extracted_data)


def title_map(option):
    try:
        title = option["title"]
    except:
        cprint("Invalid configuration. No title set.", "red")
    return title


def get_config(path_to_config):
    if os.path.exists(path_to_config):
        with open(path_to_config) as f:
            config = json.load(f)
    else:
        config = []
        with open(path_to_config, 'w+') as f:
            f.write(json.dumps(config))

    if len(config) > 0:
        prompt = 'Please choose data to extract:'

        (option, _) = pick(config, prompt, indicator="=>",
                           options_map_func=title_map)
        return option
    else:
        restart(colored('No configurations available!', "red"))


def run_tool():
    prompt = 'What would you like to do?'
    (option, _) = pick(["Extract Data", "Exit"], prompt, indicator="=>")

    if option == "Exit":
        sys.exit(colored("Bye!", "green"))

    if option == "Extract Data":
        extract_data()


def restart(status):
    print(status)
    print("Press any key to continue...")
    msvcrt.getch()
    run_tool()


if __name__ == "__main__":
    run_tool()
