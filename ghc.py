#
#       Greenhouse Controller Main Program
#
#       12/21/2024      George Schreck  Initial design
#

import argparse, sys, time, threading
import logging
from datetime import datetime
from typing import NamedTuple
from flask import Flask, render_template
from ghc_read_temp import thermostat_program

## parse incoming arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", help="debug mode - terminates")
parser.add_argument("-i", action="store_true", help="initialize the databaes - erase it!")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

args = parser.parse_args()

class Program_Control (NamedTuple):
        Sunday: bool
        Monday: bool
        Tuesday: bool
        Wednesday: bool
        Thursday: bool
        Friday: bool
        Saturday: bool
        Number_of_weeks: int
        Start_time: str
        End_time: str
        Frequency: int
        Duration: int
        On_device_control: int
        Off_device_control: int

######## initial configuration data
run = 1                         # this is used as a global debug character to kill all threads
monitor_loop_time = 10          # period of time in seconds between monitor thread running

######## global variables for non-critical data passing
temp_vars = [0.0, 0.0, " "]  # = [temperature_f, humidity, temperature_update_time]


######## Flask setup
app = Flask(__name__)
logger = logging.getLogger('werkzeug') # specific to Flask
logger.setLevel(logging.CRITICAL) # tell it the log is full
@app.route('/')

def web_if():
        return str("Time:{}    Temp:{:.2f} F    Humidity: {}%".format(temp_vars[2], temp_vars[0], temp_vars[1]))
#def home():
#       return render_template('index.html')


##############################
if args.verbose:
        print("verbose mode")


##############################
# this resets the system to an original (never used) state

if args.i:
        print("initializing database")

##############################

def command_interface():
        print("executing command interface")

my_item = Program_Control(True, False, True, False, True, True, False, -1, 'begin', 'end', 12, 10, 2, 5)


########### Web page interface
def web_interface():
        app.run(host='192.168.1.209', port=5000)


########### monitor program
#def monitor_interface(threads, temperature_f, humidity, temperature_update_time):
#def monitor_interface(threads):
def monitor_interface(threads, temp_vars):
        while(run):
                if args.verbose: print("executing monitoring interface")
                if args.debug: print("\n", threads)

                print(temp_vars[2], "\tTemp:{:.1f} F    Humidity: {}%".format(temp_vars[0], temp_vars[1]))

                time.sleep(monitor_loop_time)

        if args.verbose: print("exiting program monitor")

####################################################################

def main():
        if args.verbose: print("executing main program")

if __name__ == "__main__":
        main()
        threads = []

        # starting web server
        t = threading.Thread(target=web_interface, args=())
        threads.append(t)
        t.start()

        # starting thremostat process
        t = threading.Thread(target=thermostat_program, args=(temp_vars, run, args, ))
        threads.append(t)
        t.start()

        # starting monitor process
        t = threading.Thread(target=monitor_interface, args=(threads, temp_vars, ))
        threads.append(t)
        t.start()

        ############# Debug Control ####################
        ##### --> terminate the program and all threads
        if args.debug:
                time.sleep(30)  # debug run time in seconds
                run = 0
                if args.verbose: print("exiting main")
