from ait.src.combination_result import CombinationResult
from ait.src.share import Share
from ait.src.share_holder import ShareHolder
from ait.src.csv import Csv, CSV_FIELD_SHARE_NAME, CSV_FIELD_SHARE_COST, CSV_FIELD_SHARE_PROFIT


CSV_SAMPLES = "ait/tests/samples.csv"
CSV_PROD = "dataFinance.csv"


def main():
    shares: ShareHolder = retrieve_data(CSV_SAMPLES)
    # result: ShareHolder = brute_force(shares, ShareHolder(), 500)
    result: ShareHolder = smarter_brute_force(shares, ShareHolder(), 500)
    result: ShareHolder = dynamic(shares, ShareHolder(), 500)
    display(result)

    shares: ShareHolder = retrieve_data(CSV_PROD)
    # shares = shares.filter(predicate=lambda s: s.cost > 500 or s.cost == 0)
    # shares.sort(key=lambda s: s.cost, reverse=False)
    # shares.distinct()
    # result: ShareHolder = recurse(shares, ShareHolder(), 500)
    result: ShareHolder = dynamic(shares, ShareHolder(), 500)
    display(result)


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


def recurse(shares: ShareHolder, combinations: ShareHolder, wallet: float, need_filter: bool = True) -> ShareHolder:
    filtered_shares: ShareHolder = shares
    if need_filter:
        filtered_shares = shares.filter(predicate=lambda s: s.cost > wallet)
    if filtered_shares.empty or wallet == 0:
        return combinations
    r1: ShareHolder = ShareHolder()
    current_share: Share = filtered_shares.pop(0)
    wallet_new: float = wallet - current_share.cost
    if wallet_new >= 0:
        r1 = recurse(filtered_shares, combinations.append(current_share), wallet_new)
    r2 = recurse(filtered_shares, combinations, wallet, False)
    return max([r1, r2], key=lambda sh: sh.total_profit())


def dynamic(shares: ShareHolder, combinations: ShareHolder, wallet: float) -> ShareHolder:
    shares.sort(key=lambda s: s.benefices(), reverse=True)
    for share in shares:
        wallet_new: float = wallet - share.cost
        if wallet_new > 0 and share.cost != 0:
            combinations.append(share)
            shares.pop(0)
            wallet = wallet_new
        elif wallet_new == 0:
            combinations.append(share)
            break
        else:
            shares.pop(0)
    return combinations


def display(result: ShareHolder):
    print("--------- RESULT ----------")
    print(result)
    print("Total cost: ", result.total_cost())
    print("Total profit: ", result.total_profit())


def print_step(combinations: ShareHolder, total_cost: int, total_profit: float) -> None:
    print(combinations)
    print("Total cost: ", total_cost)
    print("Total profit: ", total_profit)
    print("----------\n")


def retrieve_data(path: str) -> ShareHolder:
    csv: Csv = Csv()
    return ShareHolder([Share(row[CSV_FIELD_SHARE_NAME], float(row[CSV_FIELD_SHARE_COST]), float(row[CSV_FIELD_SHARE_PROFIT])) for row in csv.read(path)])
