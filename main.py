# Required libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # how the pins are read

# Pins in use:
GP_DISTANCE = [
    # TRIG, ECHO
    [2, 3], # front
    [4, 14], # right
    [15, 18] # left
]

# set distance mode
for a in GP_DISTANCE:
    GPIO.setup(a[0], GPIO.OUT)
    GPIO.setup(a[1], GPIO.IN)

# Calculates the distance
def distance(side): # pass in index of side
    GPIO.output(GP_DISTANCE[side][0], True)
    time.sleep(0.00001) # let it process
    GPIO.output(GP_DISTANCE[side][0], False)

    start = time.time()
    stop = time.time()
    
    # send request
    while GPIO.input(GP_DISTANCE[side][1]) == 0:
        start = time.time()

    # get response
    while GPIO.input(GP_DISTANCE[side][1]) == 1:
        stop = time.time()

    return ((stop - start) * 34300) / 2

try:
    while True:
        print(round(distance(0)))
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()