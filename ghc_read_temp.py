#
#
#  This is the code that reads the temperature
#
#

import sys, time, argparse
import adafruit_dht
import board, logging
from datetime import datetime
from typing import NamedTuple

thermostat_loop_time = 10

#dht_device = adafruit_dht.DHT22(board.D4)
dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=True)


##########  temperature polling loop
#def thermostat_program(temperature_f, humidity, temperature_update_time):
def thermostat_program(temp_vars, run, args):
        ctr = 0
        read_errors = 0

        while(run):
                if args.verbose: print("executing thermostat controller")

                try:
                        temperature_c = dht_device.temperature
                        temperature_f = temperature_c * (9 / 5) + 32
                        temp_vars[0] = temperature_f

                        humidity = dht_device.humidity
                        temp_vars[1] = humidity

                        if args.verbose:
                                print(ctr, "\terror= ", read_errors, "\tTemp:{:.1f} C / {:.1f} F    Humidity: {}%".format(
                                temperature_c, temperature_f, humidity))
                        temp_vars[2] = datetime.now().replace(microsecond=0)
                        ctr = ctr + 1


                except RuntimeError as error:
                        if args.debug: print(error.args[0])
                        time.sleep(1)
                        read_errors = read_errors + 1
                        continue

                except Exception as error:
                        print ("++>> exiting thermostat error")
                        exit()
                        raise error     # need to fix this

                time.sleep(thermostat_loop_time)

        if args.verbose: print("exiting thermostat interface")

####################################################################i
