from anki_vector.util import parse_command_args, radians, degrees, distance_mm, speed_mmps


class RobotActions:
    def __init__(self, robot):
        """Initializer."""
        self._robot = robot

    def busted(self, count):
        self.robot_say(str(count) + " Busted")

    def blackjack(self, count):
        self.robot_say(str(count) + " Blackjack")

    def double(self, count):
        self.robot_say(str(count) + " Double, one card more")

    def split(self, card_num):
        self.robot_say(str(card_num) + " Split")

    def say_count(self, count):
        self.robot_say(str(count))

    def win(self):
        self._robot.anim.play_animation("anim_blackjack_victorbjackwin_01")
        self._robot.behavior.set_head_angle(degrees(5.0))
        self.robot_say("I win")

    def lose(self):

        self._robot.anim.play_animation("anim_blackjack_victorlose_01")
        self._robot.behavior.set_head_angle(degrees(5.0))
        self.robot_say("I lose")

    def tie(self):
        self.robot_say("I tie")

    def dealer_count(self, count):
        self._robot.say_text("Dealer " + str(count))

    def hit(self, count):
        self._robot.say_text(str(count) + " Hit me")
        self._robot.behavior.set_lift_height(.5, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        self._robot.behavior.set_lift_height(0, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        self._robot.behavior.set_lift_height(.5, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        self._robot.behavior.set_lift_height(0, accel=50.0, max_speed=10.0, duration=0)

    def stand(self, count):
        self._robot.say_text(str(count) + " I Stand")
        self._robot.behavior.set_lift_height(1, accel=50.0, max_speed=10.0, duration=0)
        self._robot.behavior.set_lift_height(0, accel=50.0, max_speed=10.0, duration=0)

    def robot_say(self, txt):
        self._robot.say_text(txt)




