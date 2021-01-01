from io import TextIOWrapper
import csv
from typing import Dict, List


CSV_FIELD_SHARE_NAME: str = "Shares #"
CSV_FIELD_SHARE_COST: str = "Cost per share (in Euros)"
CSV_FIELD_SHARE_PROFIT: str = "Profit (post 2 years)"


class Csv:
    def __init__(self) -> None:
        pass

    def read(self, path: str) -> Dict:
        result: Dict = dict()
        with open(path, "r") as file:
            result = self.__read_in_csv_file(file)
        return result

    def __read_in_csv_file(self, file: TextIOWrapper) -> Dict:
        reader = csv.DictReader(file)
        result: List = []
        for row in reader:
            row_dict: Dict = {}
            for field in row:
                row_dict[field] = row[field]
            result.append(row_dict)
        return result
