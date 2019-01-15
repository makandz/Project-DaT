# Self Driving Car Project
# By Makan D ~ Computer Engineering Class 2018 - 2019
# This car has been designed to drive and turn on it's own
# through a path. It can stop at stop signs, handle curves,
# make turns, stop if path is blocked, and more!

# AI detection was made possible by Tensorflow, this is my
# first AI project, thanks to EdjeElectronics for the tutorial.
# https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi

# Feel free to use any part of this code to make your own.
# ----------BEGIN THE CODE!---------------------------------

tick = 0

# Configuration
GP_MOTOR = [ # Motors (OUT1, OUT2)
    [17, 27],
    [22, 23]
]

GP_DISTANCE = [ # Distance sensors (TRIG, ECHO)
    [2, 3], # front
    [4, 14], # right
    [15, 18], # left
    [24, 10], # front left
    [9, 25] # front right
]

BACK_LED = 11 # Debugging or stopping.
USE_AI = True # For debugging
IM_WIDTH = 1024 # Camera x
IM_HEIGHT = 512 # Camera Y

# Required libraries
import RPi.GPIO as GPIO
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

# Stop sign data
STOP = [
    False, # begin count, seen
    0, # seconds stopped + grace period
]

GPIO.setmode(GPIO.BCM)

# set led mode
GPIO.setup(BACK_LED, GPIO.OUT)

# set motor mode
for a in GP_MOTOR:
    GPIO.setup(a[0], GPIO.OUT)
    GPIO.setup(a[1], GPIO.OUT)

# turn them into PWM
l1 = GPIO.PWM(GP_MOTOR[0][0], 50)
l2 = GPIO.PWM(GP_MOTOR[0][1], 50)
r1 = GPIO.PWM(GP_MOTOR[1][0], 50)
r2 = GPIO.PWM(GP_MOTOR[1][1], 50)

# set distance mode
for a in GP_DISTANCE:
    GPIO.setup(a[0], GPIO.OUT)
    GPIO.setup(a[1], GPIO.IN)

# Tensorflow setup
if USE_AI:
    # Required libraries for AI
    import os
    import numpy as np
    import tensorflow as tf
    import argparse
    import sys

    sys.path.append('..') # move one dir out for models

    # Even more imports!
    from utils import label_map_util
    from utils import visualization_utils as vis_util
    MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb') # Path to models used
    PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt') # path for mapping files
    NUM_CLASSES = 90 # can get 90 different things
    
    # More category and label stuff
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = NUM_CLASSES, use_display_name = True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name = '')
        sess = tf.Session(graph = detection_graph)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0') # input tensor
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0') # output tensor
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0') # confidence score of detection
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0') # what it detects
    num_detections = detection_graph.get_tensor_by_name('num_detections:0') # Number of objects detected

frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Stop detection function
def stop_detector(frame):
    global STOP # transfer data

    frame_expanded = np.expand_dims(frame, axis = 0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.40)
    
    # check for stop sign
    if int(classes[0][0]) == 13:
        # Location of detected object
        x = int(((boxes[0][0][1]+boxes[0][0][3])/2) * IM_WIDTH)
        y = int(((boxes[0][0][0]+boxes[0][0][2])/2) * IM_HEIGHT)
        cv2.circle(frame,(x,y), 5, (75, 13, 180), -1) # Draw a circle at center of object
        print("I see stop sign")
        STOP[0] = True
    return frame

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
    if reverse: # go in reverse?
        l1.start(0)
        r1.start(0)
        l2.start(left)
        r2.start(right)
    else: # nou
        l2.start(0)
        r2.start(0)
        l1.start(left)
        r1.start(right)
    print("Left", left, "Right", right, "Reverse", reverse) # debugging

# reverse and do a turn.
def processTurn(left):
    drive(70, 70, True) # backwards
    time.sleep(0.5)
    # process turn
    if left:
        drive(75, 25, False)
    else:
        drive(25, 75, False)
    time.sleep(0.5) # time for turn to complete

# Camera setup
camera = PiCamera()
camera.resolution = (IM_WIDTH, IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH, IM_HEIGHT))
rawCapture.truncate(0)

# DEBUGGING
drive(0, 0, False)

try:
    for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        tick += 1
        GPIO.output(BACK_LED, True)

        # front blocked
        if distance(0) < 15:
            ld = distance(2)
            rd = distance(1)
            if ld > rd and ld > 30: # can it turn left?
                processTurn(True)
            elif rd > ld and rd > 30: # can it turn right?
                processTurn(False)
            else: # just stop until cleared
                drive(0, 0, False)

        # front is not blocked
        else:
            f_ld = distance(3)
            f_rd = distance(4)
            if f_ld < 25: # curve front left?
                push = (25 - f_ld) * 2
                drive(30, 50 + push, False)
            elif f_rd < 25: # curve front right?
                push = (25 - f_rd) * 2
                drive(50 + push, 30, False)
            else: # drive straight, nothing wrong.
                drive(70, 70, False)

        # Stop sign detection
        t1 = cv2.getTickCount()
        frame = frame1.array
        frame.setflags(write = 1)

        if STOP[0]:
            STOP[1] += 1
            if STOP[1] < 5: # don't drive for 5 seconds.
                drive(0, 0, False)
            elif STOP[1] < 10: # passed grace period
                STOP[0] = False
                STOP[1] = 0
            time.sleep(0.3)
        elif (tick % 2 == 0) and USE_AI:
            frame = stop_detector(frame)
        else:
            time.sleep(0.3)

        # Draw FPS
        cv2.imshow('Object detector', frame)

        # FPS calculation
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        if cv2.waitKey(1) == 27: 
            break  # esc to quit

        rawCapture.truncate(0)
        
        GPIO.output(BACK_LED, False)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
    camera.close()
    cv2.destroyAllWindows()

camera.close()
cv2.destroyAllWindows()
