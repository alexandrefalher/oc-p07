from typing import ForwardRef, List
from ait.src.combination_result import CombinationResult
from ait.src.share import Share
from ait.src.share_holder import ShareHolder
from ait.src.csv import Csv, CSV_FIELD_SHARE_NAME, CSV_FIELD_SHARE_COST, CSV_FIELD_SHARE_PROFIT
import sys


CSV_SAMPLES = "ait/tests/samples.csv"
CSV_PROD = "dataFinance.csv"


def main():
    # sys.setrecursionlimit(50000)
    shares: ShareHolder = retrieve_data(CSV_SAMPLES)
    # shares: ShareHolder = ShareHolder([
    #     Share("1", 200, 100),
    #     Share("2", 150, 100),
    #     Share("3", 100, 100),
    #     Share("4", 75, 100),
    #     Share("5", 50, 100)
    # ])
    # combination_result: CombinationResult = brute_force(shares, ShareHolder(), 500)
    # combination_result: CombinationResult = smart_dyn(shares, 500)
    result: ShareHolder = smarter_brute_force(shares, ShareHolder(), 500)
    print("--------- RESULT ----------")
    print(result.shares)
    print("Total cost: ", result.total_cost())
    print("Total profit: ", result.total_profit())


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


def smarter_brute_force(shares: ShareHolder, combinations: ShareHolder, wallet: float) -> ShareHolder:
    if shares.empty or wallet == 0:
        return combinations
    r1: ShareHolder = ShareHolder()
    current_share: Share = shares.pop(0)
    wallet_new: float = wallet - current_share.cost
    if wallet_new >= 0:
        r1 = smarter_brute_force(shares, combinations.append(current_share), wallet_new)
    r2 = smarter_brute_force(shares, combinations, wallet)
    return max([r1, r2], key=lambda sh: sh.total_profit())


# def smart_dyn(shares: ShareHolder, limit: int) -> CombinationResult:
    # shares.sort(key=lambda s: s.cost, reverse=True)
    # shares.filter(predicate=lambda s: s.cost > limit)
    # shares.sort(key=lambda s: s.benefices(), reverse=True)
#     i: int = 0
#     combinations: List[ShareHolder] = []
#     share_holder: ShareHolder = ShareHolder()

#     while len(shares) > 0:
#         if share_holder.total_cost() == limit:
#             combinations.append(share_holder.copy())
#             share_holder.clear()
#             i = 0
#         elif share_holder.total_cost() > limit:
#             shares.insert(0, share_holder.pop())
#             i += 1
#         elif share_holder.total_cost() < limit:
#             share_holder.append(shares.pop(i))

#     combinations.sort(key=lambda s: s.total_profit())
#     return CombinationResult(combinations[0], combinations[0].total_cost(), combinations[0].total_profit())

# def smart_dyn(shares: ShareHolder, wallet: float) -> ShareHolder:
    # shares.sort(key=lambda s: s.cost, reverse=True)
    # shares.filter(predicate=lambda s: s.cost > wallet)
    # shares.sort(key=lambda s: s.benefices(), reverse=True)

#     previous_result: ShareHolder = ShareHolder()
#     for share in shares:
#         current_result: ShareHolder = smart_dyn_recurse(shares, ShareHolder(), wallet)
#         max([previous_result, current_result], key=lambda sh: sh.total_profit())


# def smart_dyn_recurse(shares: ShareHolder, combinations: ShareHolder, wallet: float) -> ShareHolder:
#     if shares.empty or wallet == 0:
#         return combinations
#     current_share: Share = shares.pop(0)
#     wallet_new: float = wallet - current_share.cost
#     if wallet_new >= 0:
#         smart_dyn_recurse(shares, combinations.append(current_share), wallet_new)
#     else:
#         smart_dyn_recurse(shares, combinations, wallet)


def smart(shares: ShareHolder, wallet: float) -> ShareHolder:
    shares.sort(key=lambda s: s.cost, reverse=True)
    shares.filter(predicate=lambda s: s.cost > wallet)
    shares.sort(key=lambda s: s.benefices(), reverse=True)


def erase_uniftable(shares: ShareHolder, fit_value: float) -> ShareHolder:
    shares.filter(predicate=lambda s: s.cost > fit_value)


def print_step(combinations: ShareHolder, total_cost: int, total_profit: float) -> None:
    print(combinations)
    print("Total cost: ", total_cost)
    print("Total profit: ", total_profit)
    print("----------\n")


def retrieve_data(path: str) -> ShareHolder:
    csv: Csv = Csv()
    return ShareHolder([Share(row[CSV_FIELD_SHARE_NAME], float(row[CSV_FIELD_SHARE_COST]), float(row[CSV_FIELD_SHARE_PROFIT])) for row in csv.read(path)])
