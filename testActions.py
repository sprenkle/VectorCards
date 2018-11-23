import unittest
from BlackJackActions import BlackJackActions


class TestCount(unittest.TestCase):
  def testCounting(self):
    actions = BlackJackActions()
    self.assertEqual((21, True), actions.get_count(['10d', 'Ac']))
    self.assertEqual((21, True), actions.get_count(['9d','Ad', 'Ac']))
    self.assertEqual((21, True), actions.get_count(['5d', '5d', 'Ac']))
    self.assertEqual((21, True), actions.get_count(['4d', '3d', '3s', 'Ac']))

    self.assertEqual((12, False), actions.get_count(['10d', 'Ac', 'Ad']))
    self.assertEqual((12, False), actions.get_count(['5d', '6s', 'Ad']))

    self.assertEqual((21, True), actions.get_count(['Ad', '10d']))
    self.assertEqual((17, False), actions.get_count(['9d', '8d']))
    self.assertEqual((27, False), actions.get_count(['7d', '6d', '5d', '4d', '3d', '2d']))

    self.assertEqual((21, True), actions.get_count(['Ah', '10h']))
    self.assertEqual((17, False), actions.get_count(['9h', '8h']))
    self.assertEqual((27, False), actions.get_count(['7h', '6h', '5h', '4h', '3h', '2h']))

    self.assertEqual((21, True), actions.get_count(['Ac', '10c']))
    self.assertEqual((17, False), actions.get_count(['9c', '8c']))
    self.assertEqual((27, False), actions.get_count(['7c', '6c', '5c', '4c', '3c', '2c']))

    self.assertEqual((21, True), actions.get_count(['Ad', '10d']))
    self.assertEqual((17, False), actions.get_count(['9d', '8d']))
    self.assertEqual((27, False), actions.get_count(['7s', '6s', '5s', '4s', '3s', '2s']))


class TestHand11(unittest.TestCase):
  def testc(self):
    actions = BlackJackActions()
    self.assertEqual('bl', actions.player_action('6d', [['10d', 'Ac']], 0))
    self.assertEqual('dl', actions.player_action('6d', [['9d', '2c']], 0))
    self.assertEqual('dl', actions.player_action('5d', [['8s', '3d']], 0))
    self.assertEqual('dl', actions.player_action('4d', [['7c', '4d']], 0))
    self.assertEqual('dl', actions.player_action('3d', [['6h', '5s']], 0))
    self.assertEqual('dl', actions.player_action('2d', [['5c', '6d']], 0))
    self.assertEqual('ht', actions.player_action('Ad', [['5c', '6d']], 0))

class TestHandPairA(unittest.TestCase):
  def testc(self):
    actions = BlackJackActions()
    self.assertEqual('sp', actions.player_action('Ad', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('10d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('9d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('8d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('7d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('6d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('5d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('4d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('3d', [['Ad', 'Ac']], 0))
    self.assertEqual('sp', actions.player_action('2d', [['Ad', 'Ac']], 0))

class TestHandPair10(unittest.TestCase):
  def testc(self):
    actions = BlackJackActions()
    self.assertEqual('st', actions.player_action('Ad', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('10d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('9d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('8d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('7d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('6d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('5d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('4d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('3d', [['10d', '10c']], 0))
    self.assertEqual('st', actions.player_action('2d', [['10d', '10c']], 0))

class TestHandPair9(unittest.TestCase):
  def testc(self):
    actions = BlackJackActions()
    self.assertEqual('st', actions.player_action('Ad', [['9d', '9c']], 0))
    self.assertEqual('st', actions.player_action('10d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('9d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('8d', [['9d', '9c']], 0))
    self.assertEqual('st', actions.player_action('7d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('6d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('5d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('4d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('3d', [['9d', '9c']], 0))
    self.assertEqual('sp', actions.player_action('2d', [['9d', '9c']], 0))
