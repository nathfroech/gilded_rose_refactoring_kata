import pytest
from hamcrest import assert_that, contains_exactly, has_properties  # type: ignore

from gilded_rose import (
    AGED_BRIE,
    BACKSTAGE_PASS,
    LEGENDARY_QUALITY,
    MAX_QUALITY,
    MIN_QUALITY,
    SULFURAS,
    GildedRose,
    Item,
)


class TestGildedRose:
    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(10, 20, 9, 19, id='common_case'),
        pytest.param(1, 20, 0, 19, id='near_sell_by_date'),
        pytest.param(0, 20, -1, 18, id='sell_by_date_passed'),
        pytest.param(10, MIN_QUALITY, 9, MIN_QUALITY, id='zero_quality'),
        pytest.param(0, MIN_QUALITY, -1, MIN_QUALITY, id='zero_quality_and_sell_by_date_passed'),
        pytest.param(0, 1, -1, MIN_QUALITY, id='quality_is_1_and_sell_by_date_passed'),
    ])
    def test_updates_regular_item(self, sell_in, quality, expected_sell_in, expected_quality):
        items = [
            Item(name='+5 Dexterity Vest', sell_in=sell_in, quality=quality),
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        assert_that(gilded_rose.items, contains_exactly(
            has_properties(sell_in=expected_sell_in, quality=expected_quality),
        ))

    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(2, 1, 1, 2, id='common_case'),
        pytest.param(1, 1, 0, 2, id='near_sell_by_date'),
        pytest.param(0, 1, -1, 3, id='sell_by_date_passed'),
        pytest.param(10, 0, 9, 1, id='zero_quality'),
        pytest.param(0, 0, -1, 2, id='zero_quality_and_sell_by_date_passed'),
        pytest.param(2, 50, 1, MAX_QUALITY, id='quality_is_50'),
        pytest.param(0, 49, -1, MAX_QUALITY, id='quality_is_49_and_sell_by_date_passed'),
    ])
    def test_updates_item_that_increases_quality_with_age(self, sell_in, quality, expected_sell_in, expected_quality):
        items = [
            Item(name=AGED_BRIE, sell_in=sell_in, quality=quality),
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        assert_that(gilded_rose.items, contains_exactly(
            has_properties(sell_in=expected_sell_in, quality=expected_quality),
        ))

    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(2, LEGENDARY_QUALITY, 2, LEGENDARY_QUALITY, id='common_case'),
        pytest.param(0, LEGENDARY_QUALITY, 0, LEGENDARY_QUALITY, id='sell_by_date_passed'),
        pytest.param(-1, LEGENDARY_QUALITY, -1, LEGENDARY_QUALITY, id='negative_sell_in'),
    ])
    def test_does_not_update_legendary_item(self, sell_in, quality, expected_sell_in, expected_quality):
        items = [
            Item(name=SULFURAS, sell_in=sell_in, quality=quality),
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        assert_that(gilded_rose.items, contains_exactly(
            has_properties(sell_in=expected_sell_in, quality=expected_quality),
        ))

    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(12, 1, 11, 2, id='common_case'),
        pytest.param(12, 50, 11, MAX_QUALITY, id='quality_is_50'),
        pytest.param(10, 1, 9, 3, id='sell_in_is_10'),
        pytest.param(10, 49, 9, MAX_QUALITY, id='sell_in_is_10_and_quality_is_49'),
        pytest.param(5, 1, 4, 4, id='sell_in_is_5'),
        pytest.param(5, 48, 4, MAX_QUALITY, id='sell_in_is_5_and_quality_is_48'),
        pytest.param(1, 1, 0, 4, id='near_sell_by_date'),
        pytest.param(0, 42, -1, MIN_QUALITY, id='sell_by_date_passed'),
        pytest.param(-1, MIN_QUALITY, -2, MIN_QUALITY, id='negative_sell_in'),
    ])
    def test_backstage_passes(self, sell_in, quality, expected_sell_in, expected_quality):
        items = [
            Item(name=BACKSTAGE_PASS, sell_in=sell_in, quality=quality),
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        assert_that(gilded_rose.items, contains_exactly(
            has_properties(sell_in=expected_sell_in, quality=expected_quality),
        ))

    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(10, 20, 9, 18, id='common_case'),
        pytest.param(0, 20, -1, 16, id='sell_by_date_passed'),
        pytest.param(10, MIN_QUALITY, 9, MIN_QUALITY, id='zero_quality'),
        pytest.param(0, MIN_QUALITY, -1, MIN_QUALITY, id='zero_quality_and_sell_by_date_passed'),
        pytest.param(0, 3, -1, MIN_QUALITY, id='quality_is_3_and_sell_by_date_passed'),
    ])
    def test_conjured_items(self, sell_in, quality, expected_sell_in, expected_quality):
        items = [
            Item(name='Conjured Mana Cake', sell_in=sell_in, quality=quality),
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        assert_that(gilded_rose.items, contains_exactly(
            has_properties(sell_in=expected_sell_in, quality=expected_quality),
        ))

    def test_combined_case(self):
        items = [
            Item(name='+5 Dexterity Vest', sell_in=10, quality=20),
            Item(name=AGED_BRIE, sell_in=2, quality=MIN_QUALITY),
            Item(name='Elixir of the Mongoose', sell_in=5, quality=7),
            Item(name=SULFURAS, sell_in=0, quality=LEGENDARY_QUALITY),
            Item(name=SULFURAS, sell_in=-1, quality=LEGENDARY_QUALITY),
            Item(name=BACKSTAGE_PASS, sell_in=15, quality=20),
            Item(name=BACKSTAGE_PASS, sell_in=10, quality=49),
            Item(name=BACKSTAGE_PASS, sell_in=5, quality=49),
            Item(name='Conjured Mana Cake', sell_in=3, quality=6),
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        assert_that(gilded_rose.items, contains_exactly(
            has_properties(sell_in=9, quality=19),
            has_properties(sell_in=1, quality=1),
            has_properties(sell_in=4, quality=6),
            has_properties(sell_in=0, quality=LEGENDARY_QUALITY),
            has_properties(sell_in=-1, quality=LEGENDARY_QUALITY),
            has_properties(sell_in=14, quality=21),
            has_properties(sell_in=9, quality=MAX_QUALITY),
            has_properties(sell_in=4, quality=MAX_QUALITY),
            has_properties(sell_in=2, quality=4),
        ))
