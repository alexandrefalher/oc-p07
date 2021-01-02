from ait.src.combination_result import CombinationResult
from ait.src.share import Share
from ait.src.share_holder import ShareHolder
from ait.src.csv import Csv, CSV_FIELD_SHARE_NAME, CSV_FIELD_SHARE_COST, CSV_FIELD_SHARE_PROFIT
import sys


CSV_SAMPLES = "ait/tests/samples.csv"
CSV_PROD = "dataFinance.csv"


def main():
    sys.setrecursionlimit(150000)
    shares: ShareHolder = retrieve_data(CSV_PROD)
    # combination_result: CombinationResult = brute_force(shares, ShareHolder(), 500)
    combination_result: CombinationResult = smart_dyn(shares, 500)
    print("--------- RESULT ----------")
    print(combination_result.combinations)
    print("Total cost: ", combination_result.total_cost)
    print("Total profit: ", combination_result.total_profit)


def brute_force(shares: ShareHolder, combinations: ShareHolder, limit: float) -> CombinationResult:
    if len(shares) > 0:
        shares_temp: ShareHolder = shares.copy()
        result_1: CombinationResult = brute_force(shares_temp, combinations.copy().append(shares_temp.pop(0)), limit)
        result_2: CombinationResult = brute_force(shares_temp, combinations, limit)
        return result_1 if result_1.total_profit > result_2.total_profit else result_2
    elif len(shares) == 0:
        total_cost: int = combinations.total_cost()
        total_profit: float = combinations.total_profit()
        print_step(combinations, total_cost, total_profit)
        return CombinationResult(combinations, total_cost, total_profit) if total_cost <= limit else CombinationResult(combinations, total_cost, 0)


def smart_dyn(shares: ShareHolder, limit: int) -> CombinationResult:
    shares.sort(key=lambda s: s.cost, reverse=True)
    shares.filter(predicate=lambda s: s.cost > limit)
    shares.sort(key=lambda s: s.benefices(), reverse=True)
    can_continue: bool = True
    i: int = 0
    combinations: ShareHolder = ShareHolder()
    while can_continue:
        if combinations.total_cost() > limit:
            pass
        elif combinations.total_cost() < limit:
            combinations.append(shares[i])
            i += 1
        else:
            return CombinationResult(combinations, combinations.total_cost(), combinations.total_profit())


def print_step(combinations: ShareHolder, total_cost: int, total_profit: float) -> None:
    print(combinations)
    print("Total cost: ", total_cost)
    print("Total profit: ", total_profit)
    print("----------\n")


def retrieve_data(path: str) -> ShareHolder:
    csv: Csv = Csv()
    return ShareHolder([Share(row[CSV_FIELD_SHARE_NAME], float(row[CSV_FIELD_SHARE_COST]), float(row[CSV_FIELD_SHARE_PROFIT])) for row in csv.read(path)])
