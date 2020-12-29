from ait.src.share import CombinationResult, Share, ShareHolder
from typing import Dict, Tuple
from ait.src.csv import Csv, CSV_FIELD_SHARE_NAME, CSV_FIELD_SHARE_COST, CSV_FIELD_SHARE_PROFIT


def main():
    shares: ShareHolder = ShareHolder([
        Share("share-1", 10, 3),
        Share("share-2", 9, 5),
        Share("share-3", 15, 6)
    ])
    combination_result: float = get_combination(shares, ShareHolder(), 500)
    print("--------- RESULT ----------")
    print(combination_result.combinations)
    print("Total cost: ", combination_result.total_cost)
    print("Total profit: ", combination_result.total_profit)


def get_combination(shares: ShareHolder, combinations: ShareHolder, limit: float) -> CombinationResult:
    if len(shares) > 0:
        shares_temp: ShareHolder = shares.copy()
        result_1: CombinationResult = get_combination(shares_temp, combinations.copy().append(shares_temp.remove(0)), limit)
        result_2: CombinationResult = get_combination(shares_temp, combinations, limit)
        if result_1.total_profit > result_2.total_profit:
            return result_1
        else:
            return result_2
    elif len(shares) == 0:
        total_cost: int = combinations.calculate_total_cost()
        total_profit: float = combinations.calculate_final_value()
        print_step(combinations, total_cost, total_profit)
        if total_cost <= limit:
            return CombinationResult(combinations, total_cost, total_profit)
        else:
            return CombinationResult(combinations, total_cost, 0)


def print_step(combinations: ShareHolder, total_cost_shares_combinations: int, total_profit_current_shares_combination: float) -> None:
    print(combinations)
    print("Total cost: ", total_cost_shares_combinations)
    print("Total profit: ", total_profit_current_shares_combination)
    print("----------\n")


def retrieve_data() -> Dict[str, str]:
    csv: Csv = Csv()
    data: Dict[str, str] = csv.read()
    return data
