# MIT License
#
# Copyright (c) 2018 David Sprenkle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import anki_vector
from anki_vector.util import parse_command_args, degrees
from ReadCard import ReadCard
import time

done = False
args = anki_vector.util.parse_command_args()

with anki_vector.Robot(args.serial, enable_camera_feed=True, show_viewer=False) as robot:
    cardRead = ReadCard(robot)
    robot.behavior.set_head_angle(degrees(0.0))
    while not done:
        card, percentage = cardRead.extract_card()
        print(card + " " + str(percentage))
        robot.say_text(cardRead.card_to_name(card))
