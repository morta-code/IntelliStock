import unittest
from unittest.mock import Mock, MagicMock
from simulation.simulation import Simulation


class SimulationTest(unittest.TestCase):

    def setUp(self):
        self.mock_application = Mock()
        self.mock_application.get_stock_price = MagicMock(return_value=100)
        self.simulation = Simulation(self.mock_application)

    def testBuy(self):
        self.simulation.buy_stock("OTP", 100)
        self.assertEquals(100, self.simulation.stocks["OTP"])

    def testSell(self):
        self.simulation.sell_stock("OTP", 100)
        self.assertEquals(-100, self.simulation.stocks["OTP"])

    def testMultipleBuyFromSameStock(self):
        self.simulation.buy_stock("OTP", 100)
        self.simulation.buy_stock("OTP", 50)
        self.assertEquals(150, self.simulation.stocks["OTP"])

    def testMultipleBuyAndSellFromSameStock(self):
        self.simulation.buy_stock("OTP", 100)
        self.simulation.sell_stock("OTP", 50)
        self.assertEquals(50, self.simulation.stocks["OTP"])

    def testMultipleBuyFromDifferentStocks(self):
        self.simulation.buy_stock("MOL", 30)
        self.simulation.buy_stock("OTP", 40)
        self.assertEquals(30, self.simulation.stocks["MOL"])
        self.assertEquals(40, self.simulation.stocks["OTP"])

    def testBuyPrice(self):
        self.simulation.set_interest(0) #0%
        self.simulation.set_money(1000)
        self.simulation.buy_stock("MOL", 3)
        self.assertEquals(700, self.simulation.money)

    def testBuyPriceWithInterest(self):
        self.simulation.set_interest(0.1) #10%
        self.simulation.set_money(1000)
        self.simulation.buy_stock("MOL", 3)
        self.assertEquals(670, self.simulation.money)

    def testSellPrice(self):
        self.simulation.set_interest(0) #0%
        self.simulation.set_money(1000)
        self.simulation.sell_stock("MOL", 3)
        self.assertEquals(1300, self.simulation.money)

    def testSellPrice(self):
        self.simulation.set_interest(0.1) #10%
        self.simulation.set_money(1000)
        self.simulation.sell_stock("MOL", 3)
        self.assertEquals(1270, self.simulation.money)

    def testBuyAndSellPrice(self):
        self.simulation.set_interest(0) #0%
        self.simulation.set_money(1000)
        self.simulation.buy_stock("MOL", 3)
        self.simulation.sell_stock("MOL", 3)
        self.assertEquals(1000, self.simulation.money)

    def testBuyAndSellPriceWithInterest(self):
        self.simulation.set_interest(0.1) #10%
        self.simulation.set_money(1000)
        self.simulation.buy_stock("MOL", 3)
        self.simulation.sell_stock("MOL", 3)
        self.assertEquals(940, self.simulation.money)

    def testBuyAndSellAtDifferentPrices(self):
        self.simulation.set_interest(0) #0%
        self.simulation.set_money(1000)
        self.mock_application.get_stock_price = MagicMock(return_value=100)
        self.simulation.buy_stock("MOL", 3)
        self.mock_application.get_stock_price = MagicMock(return_value=200)
        self.simulation.sell_stock("MOL", 3)
        self.assertEquals(1000-300+600, self.simulation.money)

    def testBuyAndSellAtDifferentPricesWithInterest(self):
        self.simulation.set_interest(0.1) #10%
        self.simulation.set_money(1000)
        self.mock_application.get_stock_price = MagicMock(return_value=100)
        self.simulation.buy_stock("MOL", 3)
        self.mock_application.get_stock_price = MagicMock(return_value=200)
        self.simulation.sell_stock("MOL", 3)
        self.assertEquals(1000-300-30+600-60, self.simulation.money)
