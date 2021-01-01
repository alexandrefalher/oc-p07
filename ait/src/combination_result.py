from ait.src.share_holder import ShareHolder


class CombinationResult:
    def __init__(self, combinations: ShareHolder, total_cost: int, total_profit: float):
        self.combinations: ShareHolder = combinations
        self.total_cost: int = total_cost
        self.total_profit: float = total_profit
