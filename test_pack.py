
import unittest

import pack


class TestCaseFunctions(unittest.TestCase):
    def setUp(self):
        self.inv = pack.load_inv()
        self.capacity = 20000

    def test_full_inventory_len(self):
        expected = self.inv['number'].sum()
        actual = len(pack.produce_full_inventory(self.inv))
        assert (actual, expected)

    def test_full_inventory_item(self):
        # inventory with summarized values
        item = 'socks'  # assuming it is unique id
        summary_number = int(self.inv[self.inv['description'] == item]['number'])
        # inventory with single values
        full_inv = pack.produce_full_inventory(self.inv)
        row_count = len(full_inv[full_inv.description == item])
        assert summary_number == row_count

    def test_get_inv_for_days_len(self):
        days = 3
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.get_items_days(full_inv, days)
        assert len(new_inv) <= len(full_inv)

    def test_get_inv_for_days_item(self):
        days = 5
        item = 'underwear'
        inv = pack.produce_full_inventory(self.inv)
        inv = pack.get_items_days(inv, days)
        actual_no_items = int(inv[inv['meta_category'] == item]['number'].sum())
        expected_no_items = 5
        assert actual_no_items == expected_no_items

    def test_get_inv_volume_len(self):
        """
        testing that there is no more elements in the new inventory
        cut on volume than was in original
        """
        volume = 20000
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.add_rank(full_inv)
        new_inv = pack.get_items_volume(new_inv, volume)
        assert len(new_inv) <= len(full_inv)

    def test_capacity(self):
        """
        testing that capacity is not bigger than one specified
        """
        capacity = 20000
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.add_rank(full_inv)
        items_packed = pack.get_items_volume(new_inv, capacity)[0]
        total_items_volume = items_packed.volume.sum()
        assert total_items_volume <= capacity

    def test_rank_necessities(self):
        expected_rank = 0
        new_inv = pack.add_rank(self.inv)
        actual_rank = new_inv.loc[new_inv['importance'] == 0, 'rank'].sum()
        assert actual_rank == expected_rank

    def test_rank_diversity(self):
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.add_rank(full_inv)
        new_inv = pack.get_items_volume(new_inv, 20000)[0]
        category_counts = new_inv.query('importance != 0').groupby('meta_category')['number'].count()
        print category_counts
        assert category_counts.max()-category_counts.min() < 2

    def test_rank_options(self):
        """
        testing that rank function assigns priority to specified options
        """
        options = ['dance']
        expected_importance = 0
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.add_rank(full_inv, options)
        actual_importance = new_inv[new_inv['options'].isin(options)]['rank'].max()
        assert actual_importance == expected_importance


class TestCaseResults(unittest.TestCase):

    def setUp(self):
        self.inv = pack.load_inv()

    def test_minimum(self):
        """
        testing minimum when travelling
        """
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.add_rank(full_inv)
        items = pack.get_items_volume(new_inv, 20000)[0]['meta_category']
        assert (set(['toothbrush', 'laptop', 'phone']).issubset(set(items)))

    def test_full_body_covered(self):
        days = 3
        volume = 20000
        inv = pack.load_inv()
        inv = pack.produce_full_inventory(inv)
        inv = pack.add_rank(inv)
        baggage = pack.get_items_days(inv, days)
        baggage = pack.get_items_volume(baggage, volume)[0]
        expected_parts = set(['shoes', 'socks', 'bottom', 'top'])
        actual_parts = set(baggage['meta_category'].unique())
        assert expected_parts.issubset(actual_parts)


if __name__ == '__main__':
    unittest.main()
