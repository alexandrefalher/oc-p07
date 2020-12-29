from ait.src.share import Share, ShareHolder
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
    print(combination_result[0])
    print("Total cost: ", combination_result[1])
    print("Total profit: ", combination_result[2])


def get_combination(shares: ShareHolder, combinations: ShareHolder, limit: float) -> Tuple[ShareHolder, int, float]:
    if len(shares) > 0:
        shares_temp: ShareHolder = shares.copy()
        combinations_temp: ShareHolder = combinations.copy()
        combination_reulst_1: Tuple[ShareHolder, int, float] = get_combination(shares_temp, combinations_temp.append(shares_temp.remove(0)), limit)
        combination_reulst_2: Tuple[ShareHolder, int, float] = get_combination(shares_temp, combinations, limit)
        if combination_reulst_1[2] > combination_reulst_2[2]:
            return combination_reulst_1
        else:
            return combination_reulst_2
    elif len(shares) == 0:
        total_cost_shares_combinations: int = combinations.calculate_total_cost()
        total_profit_current_shares_combination: float = combinations.calculate_final_value()
        print(combinations)
        print("Total cost: ", total_cost_shares_combinations)
        print("Total profit: ", total_profit_current_shares_combination)
        print("----------\n")
        if total_cost_shares_combinations <= limit:
            return (combinations, total_cost_shares_combinations, total_profit_current_shares_combination)
        else:
            return (combinations, total_cost_shares_combinations, 0)


def retrieve_data() -> Dict[str, str]:
    csv: Csv = Csv()
    data: Dict[str, str] = csv.read()
    return data
