#! /usr/bin/env python3

import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

player_dict = {'waffleman1793': 13, 'kid_gamer_888': 6, 'jojo_pie': 5, 'yaboidatboi': 6}
action_dict = {'joined': GPIO.HIGH, 'left': GPIO.LOW}

if __name__ == '__main__':
    try:
        player_name = sys.argv[1].lower()
        if player_name in player_dict:
            pin = player_dict[player_name]
        else:
            pin = 22
        action = action_dict[sys.argv[2]]
        print("Player: {}\tPin: {}\tAction: {}".format(player_name, pin, action))
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, action)
    except Exception as e:
        print(e)
        GPIO.cleanup()
