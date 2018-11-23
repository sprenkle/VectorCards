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
        card, percentage = cardRead.extractCard(robot)
        print(card + " " + str(percentage))
        robot.say_text(cardRead.card_to_name(card))
        time.sleep(2)
