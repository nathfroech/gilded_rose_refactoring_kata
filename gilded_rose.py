from typing import Callable, Dict, List

AGED_BRIE = 'Aged Brie'
SULFURAS = 'Sulfuras, Hand of Ragnaros'
BACKSTAGE_PASS = 'Backstage passes to a TAFKAL80ETC concert'

MIN_QUALITY = 0
MAX_QUALITY = 50
LEGENDARY_QUALITY = 80


class GildedRose:
    def __init__(self, items: List['Item']) -> None:
        self.items = items
        self.special_handlers: Dict[str, Callable[[Item], None]] = {
            AGED_BRIE: self._update_aged_brie,
            SULFURAS: self._update_legendary_item,
            BACKSTAGE_PASS: self._update_backstage_pass,
        }

    def update_quality(self) -> None:
        for item in self.items:
            handle_item = self.special_handlers.get(item.name, self._update_regular_item)
            handle_item(item)

    def _update_regular_item(self, item: 'Item') -> None:
        item.sell_in -= 1
        if item.sell_in >= 0:
            item.quality = max(item.quality - 1, MIN_QUALITY)
        else:
            item.quality = max(item.quality - 2, MIN_QUALITY)

    def _update_aged_brie(self, item: 'Item') -> None:
        item.sell_in -= 1
        if item.sell_in >= 0:
            item.quality = min(item.quality + 1, MAX_QUALITY)
        else:
            item.quality = min(item.quality + 2, MAX_QUALITY)

    def _update_legendary_item(self, item: 'Item') -> None:
        """Update sell_in and quality for a legendary item (i.e. don't do anything)."""

    def _update_backstage_pass(self, item: 'Item') -> None:
        item.sell_in -= 1
        if item.sell_in > 10:
            item.quality = min(item.quality + 1, MAX_QUALITY)
        elif item.sell_in > 5:
            item.quality = min(item.quality + 2, MAX_QUALITY)
        elif item.sell_in >= 0:
            item.quality = min(item.quality + 3, MAX_QUALITY)
        else:
            item.quality = MIN_QUALITY


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
