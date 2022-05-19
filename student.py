#!/usr/bin python3
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 70
        self.RIGHT_DEFAULT = 70
        self.MIDPOINT = 1575  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "g": ("Gia", self.gia),
                "m": ("Move", self.move),
                "t": ("Turn", self.turn_around),
                "b": ("Box", self.move_around_box)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''
    def gia(self):
      for edge in range(4):
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(75)
        time.sleep(0.8)
      self.stop()
      

    
    def safe_to_dance(self):
        self.servo(self.MIDPOINT - 400)
        time.sleep(2)
        if self.read_distance()<= 300:
          print("I see Something")
          self.servo(self.MIDPOINT)
          return False
        self.servo(self.MIDPOINT + 400)
        time.sleep(2)
        if self.read_distance()<= 300:
          print("I see Something")
          self.servo(self.MIDPOINT)

          return False
        else:
          print("I see nothing")
          self.servo(self.MIDPOINT)

          return True


    def dance(self):
      if self.safe_to_dance():
          self.fwd()
          time.sleep(1)
          self.stop()
          self.right()
          time.sleep(5)
          self.stop()
      else:
        print("Can't dance")

    def shake(self):
        """ Another example move """
        self.deg_fwd(720)
        self.stop()

    def move(self):
      while self.read_distance()>= 600:
        self.fwd()
        time.sleep(0.5)
      
      else:
        self.stop()

    def turn_around(self):
      while True:
        self.servo(self.MIDPOINT)
        self.fwd()
        if self.read_distance()<= 500:
          self.stop()
          self.turn_by_deg(180)

    def move_around_box(self):
      while self.safe_to_dance():
        for edge in range (4):
          self.turn_by_deg(80)
          self.fwd()
          time.sleep(2)
      else:
        self.fwd()
        time.sleep(0.5)
        
      

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        while self.read_distance() > 250:  # TODO: fix this magic number
            self.fwd()
            time.sleep(.01)
        self.stop()
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
