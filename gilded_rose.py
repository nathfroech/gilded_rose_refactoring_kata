from typing import List

AGED_BRIE = 'Aged Brie'
SULFURAS = 'Sulfuras, Hand of Ragnaros'
BACKSTAGE_PASS = 'Backstage passes to a TAFKAL80ETC concert'

MIN_QUALITY = 0
MAX_QUALITY = 50
LEGENDARY_QUALITY = 80


class GildedRose:
    def __init__(self, items: List['Item']) -> None:
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            item.update()


class Item:
    def __new__(cls, name: str, *args, **kwargs) -> 'Item':
        klass = Item
        if name == AGED_BRIE:
            klass = QualityIncreasingItem
        elif name == SULFURAS:
            klass = LegendaryItem
        elif name == BACKSTAGE_PASS:
            klass = BackstagePass
        elif name.startswith('Conjured '):
            klass = ConjuredItem
        return object.__new__(klass)  # noqa: WPS609

    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

    def update(self) -> None:
        self._update_sell_in()
        self.quality = self._calculate_new_quality(self.sell_in)

    def _update_sell_in(self) -> None:
        self.sell_in -= 1

    def _calculate_new_quality(self, new_sell_in: int) -> int:
        if new_sell_in >= 0:
            return max(self.quality - 1, MIN_QUALITY)
        else:
            return max(self.quality - 2, MIN_QUALITY)


class QualityIncreasingItem(Item):
    def _calculate_new_quality(self, new_sell_in: int) -> int:
        if new_sell_in >= 0:
            return min(self.quality + 1, MAX_QUALITY)
        else:
            return min(self.quality + 2, MAX_QUALITY)


class LegendaryItem(Item):
    def __init__(self, name: str, sell_in: int, quality: int = LEGENDARY_QUALITY) -> None:
        super().__init__(name, sell_in, quality)
        # Parameter is kept for signatures compatibility, but we don't care about the value.
        self.quality = LEGENDARY_QUALITY

    def _update_sell_in(self) -> None:
        pass  # noqa: WPS420

    def _calculate_new_quality(self, new_sell_in: int) -> int:
        return self.quality


class BackstagePass(Item):
    def _calculate_new_quality(self, new_sell_in: int) -> int:
        if new_sell_in > 10:
            return min(self.quality + 1, MAX_QUALITY)
        elif new_sell_in > 5:
            return min(self.quality + 2, MAX_QUALITY)
        elif new_sell_in >= 0:
            return min(self.quality + 3, MAX_QUALITY)
        else:
            return MIN_QUALITY


class ConjuredItem(Item):
    def _calculate_new_quality(self, new_sell_in: int) -> int:
        # From requirements: "Conjured" items degrade in Quality twice as fast as normal items
        # It would probably be better to bind it somehow to parent method's result - but I'm afraid that this may make
        # other quality change checks uglier.
        if new_sell_in >= 0:
            return max(self.quality - 2, MIN_QUALITY)
        else:
            return max(self.quality - 4, MIN_QUALITY)
