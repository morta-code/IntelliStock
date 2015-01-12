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
