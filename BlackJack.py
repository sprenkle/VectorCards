import anki_vector  # pylint: disable=wrong-import-position
from anki_vector.util import parse_command_args, radians, degrees, distance_mm, speed_mmps, \
    Vector3  # pylint: disable=wrong-import-position
import time


class BlackJack(object):
    def __init__(self, robot, blackJackActions, readCard):
        """Initializer."""
        self._blackJackActions = blackJackActions  # Engine is injected
        self._cardRead = readCard
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
        SetLiftHeightResponse = self._robot.behavior.set_lift_height(.5, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        SetLiftHeightResponse = self._robot.behavior.set_lift_height(0, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        SetLiftHeightResponse = self._robot.behavior.set_lift_height(.5, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        SetLiftHeightResponse = self._robot.behavior.set_lift_height(0, accel=50.0, max_speed=10.0, duration=0)

    def stand(self, count):
        self._robot.say_text(str(count) + " I Stand")
        SetLiftHeightResponse = self._robot.behavior.set_lift_height(1, accel=50.0, max_speed=10.0, duration=0)
        # time.sleep(.1)
        SetLiftHeightResponse = self._robot.behavior.set_lift_height(0, accel=50.0, max_speed=10.0, duration=0)

    def getNextCard(self, seenCards):
        card, percentage = self._cardRead.extractCard(self._robot)
        while card in seenCards:
            card, percentage = self._cardRead.extractCard(self._robot)
        seenCards.add(card)
        return card

    def robot_say(self, txt):
        self._robot.say_text(txt)
        # time.sleep(3)

    def draw(self, d, v, index, results, seenCards):
        done = False

        while not done:
            action = self._blackJackActions.player_action(d[0], v, index)
            count, ace = self._blackJackActions.get_count(v[index])

            if action == 'bu':
                self.busted(count)
                results.append(count)
                return results

            if action == 'st':
                self.stand(count)
                results.append(count)
                return results

            if action == 'dl':
                self.double(count)
                self.add_card(seenCards, v[index])
                count, ace = self._blackJackActions.get_count(v[index])
                results.append(count)
                self.say_count(count)
                return results

            if action == 'bl':
                self.blackjack(count)
                results.append(21.5)
                return results

            if action == 'sp':
                self.split(v[index][0])

                second = v[index].pop()
                splitHand = [second]
                self.add_card(seenCards, splitHand)
                v.append(splitHand)
                self.draw(d, v, index + 1, results, seenCards)

            if action == 'ht':
                self.hit(count)

            self.add_card(seenCards, v[index])

    def add_card(self, seenCards, cards):
        card = self.getNextCard(seenCards)
        cards.append(card)
        print(card)
        self.robot_say(self._cardRead.card_to_name(card))

    def run(self):
        self._robot.behavior.set_head_angle(degrees(5.0))
        deck_playable = True
        while deck_playable:
            self.robot_say("Play a round")
            seen_cards = set([])
            self._robot.camera.init_camera_feed()
            v = [[]]
            d = []

            # Deal first 3 cards
            self.add_card(seen_cards, v[0])
            self.add_card(seen_cards, d)
            self.add_card(seen_cards, v[0])

            results = self.draw(d, v, 0, [], seen_cards)

            all_busted = True
            for end_results in results:  # continue if all hands busted
                if end_results <= 21.5: all_busted = False
            if all_busted: continue

            self.robot_say("Show Dealer Card")

            # Deal dealer 4th card
            self.add_card(seen_cards, d)

            d_count, ace = self._blackJackActions.get_count(d)
            self.dealer_count(d_count)

            if len(d) == 2 and d_count == 21 and ace:
                self.robot_say("Dealer Backjack")
                self.lose()
                continue

            # if player blackjack check, note if a split and a bust dealer will still draw, should fix
            if len(results) == 1 and results[0] == 21.5:
                self.win()
                continue

            while (d_count < 17 and not ace) or (ace and d_count < 18):
                self.robot_say("Dealer Draw")
                card = self.getNextCard(seen_cards)
                self.robot_say(self._cardRead.card_to_name(card))
                d.append(card)
                d_count, ace = self._blackJackActions.get_count(d)
                self.dealer_count(d_count)

            d_count, ace = self._blackJackActions.get_count(d)

            if d_count <= 21:
                self.robot_say("Dealer Stand")
            else:
                self.robot_say("Dealer Busted")
                self.win()
                continue

            for values in results:
                if values == d_count:
                    self.tie()
                elif values > d_count:
                    self.win()
                else:
                    self.lose()


if __name__ == '__main__':
    from ReadCard import ReadCard
    from BlackJackActions import BlackJackActions

    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial, enable_camera_feed=True, show_viewer=False) as robot:
        readCard = ReadCard(robot)
        blackJackActions = BlackJackActions()
        blackJack = BlackJack(robot, blackJackActions, readCard)
        blackJack.run()
