import json
from pick import pick

from extractor import Extractor

path_to_config = "./config.json"


def get_config(path_to_config):
    with open(path_to_config) as f:
        config = json.load(f)
    prompt = 'Please choose data to extract:'

    def title_map(option): return option["title"]

    (option, _) = pick(config, prompt, indicator="=>",
                       options_map_func=title_map)
    return option


config = get_config(path_to_config)

extractor = Extractor(config)

raw_data = extractor.get_file()
extracted_data = extractor.extract_data(raw_data)
extractor.save_file(extracted_data)
