import unittest
import pack


class TestCaseFunctions(unittest.TestCase):
    def setUp(self):
        self.inv = pack.load_inv()
        self.capacity = 20000

    def test_full_inventory_len(self):
        expected = self.inv['number'].sum()
        actual = len(pack.produce_full_inventory(self.inv))
        assert actual == expected

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
        volume = 20000
        full_inv = pack.produce_full_inventory(self.inv)
        new_inv = pack.get_items_volume(full_inv, volume)
        assert len(new_inv) <= len(full_inv)

    def test_capacity(self):
        capacity = 20000
        items_packed = pack.get_items_volume(self.inv, capacity)
        total_items_volume = items_packed.volume.sum()
        assert total_items_volume <= capacity


class TestCaseResults(unittest.TestCase):

    def setUp(self):
        self.inv = pack.load_inv()

    def test_minimum(self):
        """
        testing minimum when travelling
        """
        items = pack.get_items(self.inv)
        assert set(['toothbrush', 'laptop', 'phone']).intersection(set(items))

    def test_item_duration(self):
        days = 3
        items = pack.get_items(self.inv, days=days)
        count = len([x for x in items if x == 'underwear'])
        assert count == days

    def test_full_body_covered(self):
        days = 3
        volume = 20000
        inv = pack.load_inv()
        inv = pack.produce_full_inventory(inv)
        baggage = pack.get_items_days(inv, days)
        baggage = pack.get_items_volume(baggage, volume)
        expected_parts = set(['shoes', 'socks', 'bottom', 'top'])
        actual_parts = set(baggage['meta_category'].unique())
        assert expected_parts.issubset(actual_parts)


if __name__ == '__main__':
    unittest.main()
