from __future__ import annotations


class Share:
    def __init__(self, name: str, cost: float, profit: float):
        self.name: str = name
        self.cost: float = cost
        self.profit: float = profit

    def benefices(self) -> float:
        return (self.profit * self.cost) / 100

    def __gt__(self, other: Share) -> bool:
        return self.benefices() > other.benefices()

    def __eq__(self, other: Share) -> bool:
        return self.benefices() == other.benefices()
