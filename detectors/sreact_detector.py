import sys

from GPIO import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

player_dict = {'waffle_man': 17, 'zzz': 27, 'jojo_pie': 22}
action_dict = {'joined': GPIO.HIGH, 'left': GPIO.LOW}

if __name__ == '__main':
    player_name = sys.argv[1]
    pin = player_dict[player_name]
    action = action_dict[sys.argv[2]]
    print("Player: {}\tPin: {}\tAction: {}".format(player_name, pin, action))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, action)
