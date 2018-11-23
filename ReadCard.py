import cv2
import numpy as np

class ReadCard:
    def __init__(self, robot):
        """Initializer."""
        self._robot = robot

    cardNames = {'Ah': "Ace of Hearts", 'Kh': "King of Hearts", 'Qh': "Queen of Hearts", 'Jh': "Jack of Hearts",
                 '10h': "Ten of Hearts", '9h': "Nine of Hearts",
                 '8h': "Eight of Hearts", '7h': "Seven of Hearts", '6h': "Six of Hearts", '5h': "Five of Hearts",
                 '4h': "Four of Hearts", '3h': "Three of Hearts",
                 '2h': "Two of Hearts", 'Ad': "Ace of Diamonds", 'Kd': "King of Diamonds", 'Qd': "Queen of Diamonds",
                 'Jd': "Jack of Diamonds", '10d': "Ten of Diamonds",
                 '9d': "Nine of Diamonds", '8d': "Eight of Diamonds", '7d': "Seven of Diamonds",
                 '6d': "Six of Diamonds", '5d': "Five of Diamonds",
                 '4d': "Four of Diamonds", '3d': "Three of Diamonds", '2d': "Two of Diamonds", 'Ac': "Ace of Clubs",
                 'Kc': "King of Clubs", 'Qc': "Queen of Clubs",
                 'Jc': "Jack of Clubs", '10c': "Ten of Clubs", '9c': "Nine of Clubs", '8c': "Eight of Clubs",
                 '7c': "Seven of Clubs", '6c': "Six of Clubs",
                 '5c': "Five of Clubs", '4c': "Four of Clubs", '3c': "Three of Clubs", '2c': "Two of Clubs",
                 'As': "Ace of Spades", 'Ks': "King of Spades",
                 'Qs': "Queen of Spades", 'Js': "Jack of Spades", '10s': "Ten of Spades", '9s': "Nine of Spades",
                 '8s': "Eight of Spades", '7s': "Seven of Spades",
                 '6s': "Six of Spades", '5s': "Five of Spades", '4s': "Four of Spades", '3s': "Three of Spades",
                 '2s': "Two of Spades"}

    classes = ['Ah', 'Kh', 'Qh', 'Jh', '10h', '9h', '8h', '7h', '6h', '5h', '4h', '3h',
               '2h', 'Ad', 'Kd', 'Qd', 'Jd', '10d', '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', 'Ac', 'Kc',
               'Qc', 'Jc', '10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'As', 'Ks', 'Qs', 'Js', '10s', '9s',
               '8s', '7s', '6s', '5s', '4s', '3s', '2s' ,'Ah', 'Kh', 'Qh', 'Jh', '10h', '9h', '8h', '7h', '6h', '5h',
               '4h', '3h', '2h', 'Ad', 'Kd', 'Qd', 'Jd', '10d', '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', 'Ac',
               'Kc', 'Qc', 'Jc', '10c', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'As', 'Ks', 'Qs', 'Js', '10s',
               '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s',
               ]
    image_id = 0
    scale = 0.00392
    Width = 640
    Height = 352
    conf_threshold = 0.5

    def card_to_name(self, c):
        return self.cardNames[c]

    # function to get the output layer names
    # in the architecture
    def get_output_layers(self, net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    def get_card(self, robot, net, image_array):
        image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        blob = cv2.dnn.blobFromImage(image, self.scale, (self.Width, self.Height), (0, 0, 0), True, crop=True)
        net.setInput(blob)
        outs = net.forward(self.get_output_layers(net))
        max_confidence = 0
        card = None
        cards_found = 0
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.conf_threshold and (card is None or (card is not None and card == self.classes[class_id])):
                    cards_found = cards_found + 1
                    card = self.classes[class_id]
                    if confidence > max_confidence:
                        max_confidence = confidence
        if cards_found < 2:
            card = None
            max_confidence = 0
        return card, max_confidence

    def extractCard(self, robot):
        done = False
        weights = "yolov3-tiny_15000.weights"
        cfg = "yolov3-tiny-c104.cfg"
        net = cv2.dnn.readNet(weights, cfg)

        same_image_count = 0
        cards = []

        while not (done):
            current_image_id = robot.camera.latest_image_id
            pil_image = robot.camera.latest_image
            same_image_count = same_image_count + 1

            # This is a hack,images just keep repeating not sure if it is something I coded or the Beta SDK, should be removed when fixed
            if (current_image_id == self.image_id and same_image_count < 2):
                self._robot.camera.init_camera_feed()

            if (current_image_id != self.image_id and pil_image != None):
                same_image_count = 0
                pil_image = self._robot.camera.latest_image
                self.image_id = self._robot.camera.latest_image_id
                image_array = np.array(pil_image)
                card, confidence = self.get_card(robot, net, image_array)
                if card is None:
                    continue
                # cards.append(card)
                # if len(cards) < 2:
                #     continue
                # if len(cards) == 2 and cards[0] != cards[1]:
                #     cards = []
                #     continue
                # pil_image.save('out.jpg')
                # cards.append(card)
                if card[-1] == 'w':
                    card = card[:-1]
                return card, confidence
