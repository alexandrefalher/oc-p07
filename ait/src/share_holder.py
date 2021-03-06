from __future__ import annotations
from typing import Any, Callable, List, OrderedDict
from ait.src.share import Share


class ShareHolder:
    def __init__(self, shares: List[Share] = []):
        self.shares: List[Share] = [Share(share.name, share.cost, share.profit) for share in shares]

    @property
    def empty(self):
        return True if len(self.shares) == 0 else False

    def pop(self, index: int = None) -> Share:
        if index is None:
            return self.shares.pop(len(self.shares) - 1)
        else:
            return self.shares.pop(index)

    def remove(self, index: int) -> ShareHolder:
        self.shares.pop(index)
        return self

    def append(self, value: Share) -> ShareHolder:
        self.shares.append(value)
        return self

    def filter(self, predicate: Callable[[Share], bool]) -> ShareHolder:
        new_share_holder: ShareHolder = ShareHolder()
        for share in self.shares:
            if not predicate(share):
                new_share_holder.append(share)
        return new_share_holder

    def distinct(self) -> None:
        for i, share_reference in enumerate(self.shares):
            j: int = i + 1
            while j < len(self.shares):
                if self.shares[j].cost == share_reference.cost and self.shares[j].profit == share_reference.profit:
                    self.shares.pop(j)
                else:
                    break

    def clear(self) -> None:
        self.shares = []

    def insert(self, index: int, share: Share) -> None:
        self.shares.insert(index, share)

    def total_cost(self) -> int:
        return sum([share.cost for share in self.shares])

    def total_profit(self) -> float:
        return sum([share.cost + share.benefices() for share in self.shares])

    def sort(self, key: Callable[[Share], Any], reverse: bool = True) -> None:
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
