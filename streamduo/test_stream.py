from unittest import TestCase

import stream


class Test(TestCase):
    def test_get_table_list(self):
        res= stream.get_table_list()
        print(res)
