import unittest
from BlackJack import BlackJack


class Robot():
  None

class BlackJackActions():
  None

class ReadCard():
  None

class TestCount(unittest.TestCase):
  def testCounting(self):
    robot = Robot()
    readCard = ReadCard()
    blackJackActions= BlackJackActions()

    blackJack = BlackJack(robot, blackJackActions, readCard)

    results = blackJack.draw('As', ['9h','7s'], 0, [], [])

    self.assertEqual(1,results)
    