import unittest
from unittest.mock import Mock, MagicMock
from simulation.simulation import Simulation


class SimulationTest(unittest.TestCase):

    def setUp(self):
        mock_application = Mock()
        mock_application.get_stock_price = MagicMock(return_value=100)
        self.simulation = Simulation(mock_application)

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
