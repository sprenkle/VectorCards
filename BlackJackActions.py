import asyncio
import concurrent
from math import cos, sin, inf, acos
import os
import sys
import anki_vector   # pylint: disable=wrong-import-position
from anki_vector.util import parse_command_args, radians, degrees, distance_mm, speed_mmps, Vector3  # pylint: disable=wrong-import-position
import cv2
import argparse
import numpy as np
from PIL import Image
from ReadCard import ReadCard
import time

class BlackJackActions :
  noacematrix = [
                [], # 0 will not match
                # 0   1   2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17    18    19    20    21
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st', 'st'], # dealer has ace
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'ht', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st'], # 2
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'dl', 'ht', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st'], # 3
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'dl', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st'], # 4
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'dl', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st'], # 5
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st', 'st'], # 6
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st', 'st'], # 7
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st', 'st'], # 8
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st', 'st'], # 9
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'dl', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st', 'st'] # 10
                ]

  acematrix = [
                [], # 0 will not match
                # 0   1   2     3     4     5     6     7     8     9     10    11 
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st'], # dealer has ace
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st'], # 2
                ['', '', 'ht', 'ht', 'ht', 'ht', 'dl', 'dl', 'st', 'st', 'st'], # 3
                ['', '', 'ht', 'ht', 'dl', 'dl', 'dl', 'dl', 'st', 'st', 'st'], # 4
                ['', '', 'ht', 'ht', 'dl', 'dl', 'dl', 'dl', 'st', 'st', 'st'], # 5
                ['', '', 'dl', 'dl', 'dl', 'dl', 'dl', 'dl', 'st', 'st', 'st'], # 6
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st'], # 7
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st', 'st'], # 8
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st'], # 9
                ['', '', 'ht', 'ht', 'ht', 'ht', 'ht', 'ht', 'st', 'st', 'st'] # 10
                ]

  splitmatrix = [
                [], # 0 will not match
                # 0   1     2     3     4     5     6     7     8     9     10    11 
                ['', 'sp', 'na', 'na', 'na', 'na', 'na', 'na', 'sp', 'na', 'na'], # dealer has ace
                ['', 'sp', 'sp', 'sp', 'na', 'na', 'sp', 'sp', 'sp', 'sp', 'na'], # 2
                ['', 'sp', 'sp', 'sp', 'na', 'na', 'sp', 'sp', 'sp', 'sp', 'na'], # 3
                ['', 'sp', 'sp', 'sp', 'sp', 'na', 'sp', 'sp', 'sp', 'sp', 'na'], # 4
                ['', 'sp', 'sp', 'sp', 'sp', 'na', 'sp', 'sp', 'sp', 'sp', 'na'], # 5
                ['', 'sp', 'sp', 'sp', 'na', 'na', 'sp', 'sp', 'sp', 'sp', 'na'], # 6
                ['', 'sp', 'sp', 'sp', 'na', 'na', 'na', 'sp', 'sp', 'na', 'na'], # 7
                ['', 'sp', 'na', 'na', 'na', 'na', 'na', 'na', 'sp', 'sp', 'na'], # 8
                ['', 'sp', 'na', 'na', 'na', 'na', 'na', 'na', 'sp', 'sp', 'na'], # 9
                ['', 'sp', 'na', 'na', 'na', 'na', 'na', 'na', 'sp', 'na', 'na'] # 10
                ]

  black_jack_values =	{'Ah':1,'Kh':10,'Qh':10,'Jh':10,'10h':10,'9h':9,'8h':8,'7h':7,'6h':6,'5h':5,'4h':4,'3h':3,'2h':2,'Ad':1,'Kd':10,'Qd':10,'Jd':10,'10d':10,'9d':9,'8d':8,'7d':7,'6d':6,'5d':5,'4d':4,'3d':3,'2d':2,
                       'Ac':1,'Kc':10,'Qc':10,'Jc':10,'10c':10,'9c':9,'8c':8,'7c':7,'6c':6,'5c':5,'4c':4,'3c':3,'2c':2,'As':1,'Ks':10,'Qs':10,'Js':10,'10s':10,'9s':9,'8s':8,'7s':7,'6s':6,'5s':5,'4s':4,'3s':3,'2s':2}


  def black_jack_value(self, c):
    return self.black_jack_values[c]

  def get_count(self, hand):
    count = 0
    ace = False
    for c in hand :
      cardValue = self.black_jack_value(c);
      count = count + cardValue
      if cardValue == 1 : ace = True
    if count <= 11 and ace :
      count = count + 10
    else :
      ace = False
    return count, ace


  def player_action(self, dealer_card, cards, index):
    dealer_card = self.black_jack_values[dealer_card]

    count, ace = self.get_count(cards[index])
  
    if len(cards[index]) == 2 and ace and count == 21 : # checks for blackjack for special reactions from Vector
      return 'bl'

    if len(cards[index]) == 2 and self.black_jack_values[cards[index][0]] == self.black_jack_values[cards[index][1]] : # pair consider a split, NOT Implemented
      results = self.splitmatrix[dealer_card][self.black_jack_values[cards[index][0]]]
      if results == 'sp' :
        return results

    if (not ace and count > 21) or (ace and count - 10) > 21: 
      return 'bu'
    
    if ace and count - 10 <= 11 and count != 21:
      return self.acematrix[dealer_card][count-10]

    return self.noacematrix[dealer_card][count]







    