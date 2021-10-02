import json

import analysis
import parser

OUTPUT_FILE = 'result.json'


def write_to_file(info):
    with open(OUTPUT_FILE, 'w', encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    data = parser.get_data()
    print(data)
    analysis_of_data = analysis.analysis_of_data(data)
    print(analysis_of_data)
    write_to_file(analysis_of_data)



