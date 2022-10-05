import unittest
import nbp_api

class TestAPI_NBP(unittest.TestCase):
    def setUp(self):
        self.api = nbp_api.NBPAPI()

    def tearDown(self) -> None:
        self.api.destructor()

    def test_get_current_rate(self):
        rate = self.api.get_current_rate("EUR")
        self.assertGreater(rate, 0)

        rate = self.api.get_current_rate("KOM")
        self.assertEqual(rate, self.api.ERR_CODE)

        rate = self.api.get_current_rate("KOMA")
        self.assertEqual(rate, self.api.ERR_ASCII)
    
    def test_get_rate_for_date(self):
        rate_for_date = self.api.get_rate_for_date("EUR", "2021-12-13")
        self.assertGreater(rate_for_date, 0)

        rate_for_date = self.api.get_rate_for_date("KOM", "2021-12-13")
        self.assertEqual(rate_for_date, self.api.ERR_CODE)

        rate_for_date = self.api.get_rate_for_date("EUR", "2021-12-131")
        self.assertEqual(rate_for_date, self.api.ERR_ASCII)

        rate_for_date = self.api.get_rate_for_date("KOMA", "2021-12-13")
        self.assertEqual(rate_for_date, self.api.ERR_ASCII)

    







    

    
if __name__ == "__main__":
    unittest.main()