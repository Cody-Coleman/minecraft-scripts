from threading import Thread
from time import sleep
from mcpi.minecraft import Minecraft


class HitDetector:
    """
    Class that can take any number of check_hits functions and spins off a thread to process them,
    passing the list of hit blocks data
    """
    def __init__(self):
        """
        Init the class with an empty check_list, and various flags
        """
        self.check_list = []
        self.running = True
        self.t1 = None
        self.mc = Minecraft.create()

    def check_on(self):
        """
        Starts the checker, setting the flag to true, creating the thread, and starting it.
        Needs to clear out all previous events first.
        :return:
        """
        self.mc.events.clearAll()
        self.running = True
        self.t1 = Thread(target=self.check_hits)
        self.t1.setDaemon(True)
        self.t1.start()

    def check_hits(self):
        """
        Gets all the events and then loops through all the functions that could be matches to this.
        Would be smarter to thread this out further as well.
        :return:
        """
        while self.running:
            sleep(0.5)
            hits = self.mc.events.pollBlockHits()
            for func in self.check_list:
                func(hits)

    def check_off(self):
        """ Simple command disables all checks """
        self.running = False

    def add_check(self, func):
        if not self.running:
            self.check_list.append(func)
        else:
            print("You cannot add a new check to the already running checker. Stop it first then add a check")

    def del_check(self, func):
        if not self.running:
            self.check_list.remove(func)
        else:
            print("You cannot remove a check to an already running checker. Stop it first then add a check")

    def __del__(self):
        """
        shut down the threads. Calling the check_off in case there is more that needs / wants to be added to the shut down
        :return:
        """
        self.check_off()
