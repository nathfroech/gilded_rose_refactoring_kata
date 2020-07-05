import pytest
from hamcrest import assert_that, contains_exactly, equal_to, has_properties, is_  # type: ignore

import gilded_rose


class TestGildedRose:
    def test_combined_case(self):
        items = [
            gilded_rose.Item(name='+5 Dexterity Vest', sell_in=10, quality=20),
            gilded_rose.Item(name=gilded_rose.AGED_BRIE, sell_in=2, quality=gilded_rose.MIN_QUALITY),
            gilded_rose.Item(name='Elixir of the Mongoose', sell_in=5, quality=7),
            gilded_rose.Item(name=gilded_rose.SULFURAS, sell_in=0, quality=gilded_rose.LEGENDARY_QUALITY),
            gilded_rose.Item(name=gilded_rose.SULFURAS, sell_in=-1, quality=gilded_rose.LEGENDARY_QUALITY),
            gilded_rose.Item(name=gilded_rose.BACKSTAGE_PASS, sell_in=15, quality=20),
            gilded_rose.Item(name=gilded_rose.BACKSTAGE_PASS, sell_in=10, quality=49),
            gilded_rose.Item(name=gilded_rose.BACKSTAGE_PASS, sell_in=5, quality=49),
            gilded_rose.Item(name='Conjured Mana Cake', sell_in=3, quality=6),
        ]
        gilded_rose_instance = gilded_rose.GildedRose(items)

        gilded_rose_instance.update_quality()

        assert_that(gilded_rose_instance.items, contains_exactly(
            has_properties(sell_in=9, quality=19),
            has_properties(sell_in=1, quality=1),
            has_properties(sell_in=4, quality=6),
            has_properties(sell_in=0, quality=gilded_rose.LEGENDARY_QUALITY),
            has_properties(sell_in=-1, quality=gilded_rose.LEGENDARY_QUALITY),
            has_properties(sell_in=14, quality=21),
            has_properties(sell_in=9, quality=gilded_rose.MAX_QUALITY),
            has_properties(sell_in=4, quality=gilded_rose.MAX_QUALITY),
            has_properties(sell_in=2, quality=4),
        ))


class TestItem:
    @pytest.mark.parametrize('name,expected_class', [
        pytest.param('+5 Dexterity Vest', gilded_rose.Item, id='regular_item'),
        pytest.param(
            gilded_rose.AGED_BRIE,
            gilded_rose.QualityIncreasingItem,
            id='item_that_increases_quality_with_age',
        ),
        pytest.param(gilded_rose.SULFURAS, gilded_rose.LegendaryItem, id='legendary_item'),
        pytest.param(gilded_rose.BACKSTAGE_PASS, gilded_rose.BackstagePass, id='backstage_pass'),
        pytest.param('Conjured Mana Cake', gilded_rose.ConjuredItem, id='conjured_item'),
    ])
    def test_creating_instances_of_proper_subclasses(self, name, expected_class):
        item = gilded_rose.Item(name=name, sell_in=10, quality=20)

        assert_that(type(item), is_(equal_to(expected_class)))

    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(10, 20, 9, 19, id='common_case'),
        pytest.param(1, 20, 0, 19, id='near_sell_by_date'),
        pytest.param(0, 20, -1, 18, id='sell_by_date_passed'),
        pytest.param(10, gilded_rose.MIN_QUALITY, 9, gilded_rose.MIN_QUALITY, id='zero_quality'),
        pytest.param(
            0,
            gilded_rose.MIN_QUALITY,
            -1,
            gilded_rose.MIN_QUALITY,
            id='zero_quality_and_sell_by_date_passed',
        ),
        pytest.param(0, 1, -1, gilded_rose.MIN_QUALITY, id='quality_is_1_and_sell_by_date_passed'),
    ])
    def test_item_update(self, sell_in, quality, expected_sell_in, expected_quality):
        item = gilded_rose.Item(name='+5 Dexterity Vest', sell_in=sell_in, quality=quality)

        item.update()

        assert_that(item, has_properties(sell_in=expected_sell_in, quality=expected_quality))


class TestQualityIncreasingItem:
    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(2, 1, 1, 2, id='common_case'),
        pytest.param(1, 1, 0, 2, id='near_sell_by_date'),
        pytest.param(0, 1, -1, 3, id='sell_by_date_passed'),
        pytest.param(10, 0, 9, 1, id='zero_quality'),
        pytest.param(0, 0, -1, 2, id='zero_quality_and_sell_by_date_passed'),
        pytest.param(2, 50, 1, gilded_rose.MAX_QUALITY, id='quality_is_50'),
        pytest.param(0, 49, -1, gilded_rose.MAX_QUALITY, id='quality_is_49_and_sell_by_date_passed'),
    ])
    def test_item_update(self, sell_in, quality, expected_sell_in, expected_quality):
        item = gilded_rose.Item(name=gilded_rose.AGED_BRIE, sell_in=sell_in, quality=quality)

        item.update()

        assert_that(item, has_properties(sell_in=expected_sell_in, quality=expected_quality))


class TestLegendaryItem:
    def test_initialization_with_invalid_quality(self):
        item = gilded_rose.Item(name=gilded_rose.SULFURAS, sell_in=0, quality=42)

        assert_that(item.quality, is_(equal_to(gilded_rose.LEGENDARY_QUALITY)))

    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(2, gilded_rose.LEGENDARY_QUALITY, 2, gilded_rose.LEGENDARY_QUALITY, id='common_case'),
        pytest.param(0, gilded_rose.LEGENDARY_QUALITY, 0, gilded_rose.LEGENDARY_QUALITY, id='sell_by_date_passed'),
        pytest.param(-1, gilded_rose.LEGENDARY_QUALITY, -1, gilded_rose.LEGENDARY_QUALITY, id='negative_sell_in'),
    ])
    def test_item_update(self, sell_in, quality, expected_sell_in, expected_quality):
        item = gilded_rose.Item(name=gilded_rose.SULFURAS, sell_in=sell_in, quality=quality)

        item.update()

        assert_that(item, has_properties(sell_in=expected_sell_in, quality=expected_quality))


class TestBackstagePass:
    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(12, 1, 11, 2, id='common_case'),
        pytest.param(12, 50, 11, gilded_rose.MAX_QUALITY, id='quality_is_50'),
        pytest.param(10, 1, 9, 3, id='sell_in_is_10'),
        pytest.param(10, 49, 9, gilded_rose.MAX_QUALITY, id='sell_in_is_10_and_quality_is_49'),
        pytest.param(5, 1, 4, 4, id='sell_in_is_5'),
        pytest.param(5, 48, 4, gilded_rose.MAX_QUALITY, id='sell_in_is_5_and_quality_is_48'),
        pytest.param(1, 1, 0, 4, id='near_sell_by_date'),
        pytest.param(0, 42, -1, gilded_rose.MIN_QUALITY, id='sell_by_date_passed'),
        pytest.param(-1, gilded_rose.MIN_QUALITY, -2, gilded_rose.MIN_QUALITY, id='negative_sell_in'),
    ])
    def test_item_update(self, sell_in, quality, expected_sell_in, expected_quality):
        item = gilded_rose.Item(name=gilded_rose.BACKSTAGE_PASS, sell_in=sell_in, quality=quality)

        item.update()

        assert_that(item, has_properties(sell_in=expected_sell_in, quality=expected_quality))


class TestConjuredItem:
    @pytest.mark.parametrize('sell_in,quality,expected_sell_in,expected_quality', [
        pytest.param(10, 20, 9, 18, id='common_case'),
        pytest.param(0, 20, -1, 16, id='sell_by_date_passed'),
        pytest.param(10, gilded_rose.MIN_QUALITY, 9, gilded_rose.MIN_QUALITY, id='zero_quality'),
        pytest.param(
            0,
            gilded_rose.MIN_QUALITY,
            -1,
            gilded_rose.MIN_QUALITY,
            id='zero_quality_and_sell_by_date_passed',
        ),
        pytest.param(0, 3, -1, gilded_rose.MIN_QUALITY, id='quality_is_3_and_sell_by_date_passed'),
    ])
    def test_item_update(self, sell_in, quality, expected_sell_in, expected_quality):
        item = gilded_rose.Item(name='Conjured Mana Cake', sell_in=sell_in, quality=quality)

        item.update()

        assert_that(item, has_properties(sell_in=expected_sell_in, quality=expected_quality))
