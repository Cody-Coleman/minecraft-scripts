import sys

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

player_dict = {'waffleman1793': 13, 'zzz': 6, 'jojo_pie': 5, 'ziblez': 22}
action_dict = {'joined': GPIO.HIGH, 'left': GPIO.LOW}

if __name__ == '__main__':
    try:
        player_name = sys.argv[1].lower()
        if player_name in player_dict:
            pin = player_dict[player_name]
        else:
            raise SystemExit("Player not found")
        action = action_dict[sys.argv[2]]
        print("Player: {}\tPin: {}\tAction: {}".format(player_name, pin, action))
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, action)
    except Exception as e:
        print(e)
        GPIO.cleanup()
