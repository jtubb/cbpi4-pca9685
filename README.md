# PCA9685 I2C PWM Actor Plugin for CraftBeerPi4 

Tested on Waveshare Servo Driver Hat on a Raspberry PI 3B. Will likely work with the Adafruit PCA9685 breakout board as well.

## Installation/Upgrade

From your command line run the following:

```
sudo pip3 install --upgrade https://github.com/jtubb/cbpi4-pca9685/archive/main.zip
cbpi add cbpi4-pca9685
```

Requires cbpi>=4.0.0.45, current development branch.


## Settings

Settings will be added by this plugin:
- Address: Address of the PCA9685 device. Boards typically display both a low (0x40) and high (0x70) address. Select the low address. If no devices are listed ensure you have enabled I2C on your Raspberry PI and check if the device exists in ("/dev/i2c-*").
- Channel (0-15): Output pin to use on the PCA9685.
- Frequency (50 HZ): Frequency to output. Frequency is set for all channels at once, do not mix and match frequencies on a single device (address). Typically 50 hz is good for servos and 1000 hz is good for general PWM outputs.
- Servo_Min_Pulse_Width - Value between 0 and 4095 that corresponds to your servos minimum rotation angle, you will need to test on your specific servo to determine this value (usually ~100). If using as a general PWM output set to 0 (12bit PWM resolution). This will be ranged to 0% output of the actor.
- Servo_Max_Pulse_Width - Value between 0 and 4095 that corresponds to your servos maximum rotation angle, you will need to test on your specific servo to determine this value (usually ~600). If using as a general PWM output set to 4095 (12bit PWM resolution). This will be ranged to 100% output of the actor.

## Use as a servo controller

If you are intending to use the Waveshare Servo Driver Hat to control servos, several modifications are required. Note that these modifications are not guaranteed and they may destroy your Raspberry PI, fry the PCA9685 breakout board, smoke your servos, steal your truck, and run off with your girlfriend. Proceed at your own risk. If you don't know what the following means on the first read through I would not recommend attempting the modifications unless you expect to replace all your hardware at least once.

First you should isolate the power supply of the Raspberry PI from the Waveshare Servo Hat. This will prevent any voltage transients from the motors from feeding back through the 5V rail and destroying your Raspberry PI. This can be accomplished by removing the "R0" resistor from the board. After this you will have to provide a 5v power supply to the Raspberry PI and a 6-12V power supply to the PCA9685 board.

<img src="/artifacts/IsolateRPI.jpg?raw=true" width="400" height="400">

Next you need to add a beefy capacitor across the 5V rail. I had a 6.3V 1500uF handy so that's what I used, somewhere between 1000uF and 2000uF should be good. This will prevent voltage drops and subsequent positioning errors that may occur when operating multiple servos. This capacitor is already built into the Adafruit PCA9685 shield.

Install the capacitor on the exposed header. Ensure you match the polarity correctly!

<img src="/artifacts/CapLocation.jpg?raw=true" width="400" height="400">

The capacitor will look like this when completed.

<img src="/artifacts/AddCap.jpg?raw=true" width="400" height="400">

If you are using heat sinks on your Raspberry PI ensure that the leads of the capacitor aren't shorted.

<img src="/artifacts/CapClearance.jpg?raw=true" width="400" height="400">


## Use as a 5V PWM controller

By default the Waveshare board outputs 3.3V on the signal line, if 5V PWM is required one more modification is necessary. This modification will also raise the I2C pins on the PCA9685 board to 5V, your Raspberry PI IO is at 3.3V. The appropriate way to account for this is to add a level shift chip between the Raspberry PI and the PCA9685 controller SDA and SCL lines.

However as long as the SDA and SCL lines do not have a pullup resistor (they do not on the Waveshare board), the risk of sinking more current than the Raspberry PI can support is very low. Low but not zero, this is not supported and will once again fry your Raspberry PI if you don't know what you're doing. Anyway here's how to do it.

First you need to remove the RT9193 3.3V regulator chip from the board.

<img src="/artifacts/RemoveRT9193.jpg?raw=true" width="400" height="400">

Jumper wire to connect the 5v bus across to what used to be the 3.3v bus.

<img src="/artifacts/Jumper5v.jpg?raw=true" width="400" height="400">

Your PCA9685 PWM outputs will now output at 5V.

##  Changelog

**11.16.21: Initial release
