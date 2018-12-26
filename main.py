# Required libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # how the pins are read

# Pins in use:
GP_MOTOR = [
    [17, 27],
    [22, 23]
]

GP_DISTANCE = [
    # TRIG, ECHO
    [2, 3], # front
    [4, 14], # right
    [15, 18] # left
]

# set motor mode
for a in GP_MOTOR:
    GPIO.setup(a[0], GPIO.OUT)
    GPIO.setup(a[1], GPIO.OUT)

# turn them into PWM
l1 = GPIO.PWM(17, 50)
l2 = GPIO.PWM(27, 50)
r1 = GPIO.PWM(22, 50)
r2 = GPIO.PWM(23, 50)

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

# Used for wheel and direction driving.
def drive(left, right, reverse):
    if reverse:
        GPIO.output(17, False)
        GPIO.output(22, False)
        l2.start(left)
        r2.start(right)
    else:
        GPIO.output(27, False)
        GPIO.output(23, False)
        l1.start(left)
        r1.start(right)

try:
    while True:
        drive(75, 75, False)
        print(round(distance(0)))
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()