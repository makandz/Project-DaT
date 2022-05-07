# Project DaT
This is my grade 12 computer engineering final project, a self driving car.

## The goal
The goal of this project was to make a car that can do the following the things:
- Well, drive! It should be able to make slight turns even if the path isn't straight.
- Ability to stop at dead ends and make a decision on whether to turn right or left.
- Make use of an onboard camera to detect stop signs and stop for a few seconds, then keep driving.
- It should be able to do everything above, even in the dark.

## How it was made
<img src="https://user-images.githubusercontent.com/9423347/167263729-6be024b7-4100-4ee8-b237-a6a21aee03e2.jpg" width="300" />

The final design was made with the following components:
- A car with three wheels, two of which are powered by motors.
- 5 proximity detectors.
  - One directly in the front used to detect walls.
  - Two on the edges to handle slight curves.
  - Two directly on the sides used for making sharp turn decisions.
- A camera sending data to Tensorflow detecting stop signs.
- Two LEDs to give the car headlights for the dark.

## Demo
### Videos
A quick demo of the wall detection: [Google Drive Video](https://drive.google.com/file/d/1BF9IQMbp7y0gJ317yye41gjnS2xKctd7/view?usp=sharing)

### Pictures
Demo of the stop sign detection

<img src="https://user-images.githubusercontent.com/9423347/167267255-785d3b49-6237-4537-99fa-647daaa06fa6.jpg" width="500" />

## Progress pictures
Here are a few pictures of the progress leading up the final product.

### Initial motor and sensor wiring
<img src="https://user-images.githubusercontent.com/9423347/167267440-eeff9a59-7600-494b-9737-8a064b3dea32.jpg" width="500" />
<img src="https://user-images.githubusercontent.com/9423347/167267376-97718829-30ca-4513-ab3e-83a717619246.png" width="500" />

### First car setup
<img src="https://user-images.githubusercontent.com/9423347/167267520-340a5076-028c-4cf3-a67d-deba9d3557cc.png" width="500" />

### Updated setup
<img src="https://user-images.githubusercontent.com/9423347/167267575-f19856ee-233c-45ad-828f-377a7cc6c6e9.jpg" width="500" />
<img src="https://user-images.githubusercontent.com/9423347/167267625-77a11dcb-4fa7-4126-95bc-5164cdbdf8b7.jpg" width="500" />
<img src="https://user-images.githubusercontent.com/9423347/167267628-1cc69050-7093-46f8-b4e8-a95ef5b12a31.jpg" width="500" />
<img src="https://user-images.githubusercontent.com/9423347/167267639-61d4e58e-39b2-4c7a-bdfb-b3001c58a46d.jpg" width="500" />
