import anki_vector
from anki_vector.util import parse_command_args, degrees


class BlackJack(object):
    def __init__(self, robot, blackJackActions, readCard, actions):
        self._blackJackActions = blackJackActions
        self._cardRead = readCard
        self._robot = robot
        self._actions = actions

    def get_next_card(self, seen_cards):
        card, percentage = self._cardRead.extractCard(self._robot)
        while card in seen_cards:
            card, percentage = self._cardRead.extractCard(self._robot)
        seen_cards.add(card)
        return card

    def draw(self, d, v, index, results, seen_cards):
        while True:
            action = self._blackJackActions.player_action(d[0], v, index)
            count, ace = self._blackJackActions.get_count(v[index])

            if action == 'bu':
                self._actions.busted(count)
                results.append(count)
                return results

            if action == 'st':
                self._actions.stand(count)
                results.append(count)
                return results

            if action == 'dl':
                self._actions.double(count)
                self.add_card(seen_cards, v[index])
                count, ace = self._blackJackActions.get_count(v[index])
                results.append(count)
                self._actions.say_count(count)
                return results

            if action == 'bl':
                self._actions.blackjack(count)
                results.append(21.5)
                return results

            if action == 'sp':
                self._actions.split(v[index][0])

                second = v[index].pop()
                split_hand = [second]
                self.add_card(seen_cards, split_hand)
                v.append(split_hand)
                self.draw(d, v, index + 1, results, seen_cards)

            if action == 'ht':
                self._actions.hit(count)

            self.add_card(seen_cards, v[index])

    def add_card(self, seen_cards, cards):
        card = self.get_next_card(seen_cards)
        cards.append(card)
        print(card)
        self._actions.robot_say(self._cardRead.card_to_name(card))

    def run(self):
        self._robot.behavior.set_head_angle(degrees(5.0))
        deck_playable = True
        while deck_playable:
            self._actions.robot_say("Play a round")
            seen_cards = set([])
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

            self._actions.robot_say("Show Dealer Card")

            # Deal dealer 4th card
            self.add_card(seen_cards, d)

            d_count, ace = self._blackJackActions.get_count(d)
            self._actions.dealer_count(d_count)

            if len(d) == 2 and d_count == 21 and ace:
                self._actions.robot_say("Dealer Backjack")
                self._actions.lose()
                continue

            # if player blackjack check, note if a split and a bust dealer will still draw, should fix
            if len(results) == 1 and results[0] == 21.5:
                self._actions.win()
                continue

            while (d_count < 17 and not ace) or (ace and d_count < 18):
                self._actions.robot_say("Dealer Draw")
                card = self.get_next_card(seen_cards)
                self._actions.robot_say(self._cardRead.card_to_name(card))
                d.append(card)
                d_count, ace = self._blackJackActions.get_count(d)
                self._actions.dealer_count(d_count)

            d_count, ace = self._blackJackActions.get_count(d)

            if d_count <= 21:
                self._actions.robot_say("Dealer Stand")
            else:
                self._actions.robot_say("Dealer Busted")
                self._actions.win()
                continue

            for values in results:
                if values == d_count:
                    self._actions.tie()
                elif values > d_count:
                    self._actions.win()
                else:
                    self._actions.lose()


if __name__ == '__main__':
    from ReadCard import ReadCard
    from BlackJackActions import BlackJackActions
    from RobotActions import RobotActions

    args = anki_vector.util.parse_command_args()

    with anki_vector.Robot(args.serial, enable_camera_feed=True, show_viewer=False) as robot:
        readCard = ReadCard(robot)
        blackJackActions = BlackJackActions()
        actions = RobotActions(robot)
        blackJack = BlackJack(robot, blackJackActions, readCard, actions)
        blackJack.run()
