from __future__ import annotations
from typing import Any, Callable, List
from ait.src.share import Share


class ShareHolder:
    def __init__(self, shares: List[Share] = []):
        self.shares: List[Share] = [Share(share.name, share.cost, share.profit) for share in shares]

    def pop(self, index: int) -> Share:
        share: Share = self.shares.pop(index)
        return share

    def remove(self, index: int) -> ShareHolder:
        self.shares.pop(index)
        return self

    def append(self, value: Share) -> ShareHolder:
        self.shares.append(value)
        return self

    def calculate_total_cost(self) -> int:
        return sum([share.cost for share in self.shares])

    def calculate_final_value(self) -> float:
        return sum([share.cost + share.benefices() for share in self.shares])

    def sort(self, key: Callable[[Share], Any], reverse: bool) -> None:
        self.shares.sort(key=key, reverse=reverse)

    def __str__(self) -> str:
        return "\n".join(["Name: {0}, cost: {1}, profit: {2}, benefices: {3}".format(share.name, share.cost, share.profit, share.benefices()) for share in self.shares])

    def __getitem__(self, index: int) -> Share:
        return self.shares[index]

    def __setitem__(self, index: int, value: Share) -> None:
        self.shares[index] = value

    def __len__(self) -> int:
        return len(self.shares)

    def copy(self) -> ShareHolder:
        copy: ShareHolder = ShareHolder(self.shares)
        return copy
