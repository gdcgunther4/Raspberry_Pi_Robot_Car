'''
This was inspired by the book 'Learn Robotics with Raspberry Pi
'''
#This sets up the motors
import cwiid
from adafruit_motorkit import MotorKit

kit = MotorKit()
#Now we connect to the Wii remote
import cwiid, time

button_delay = 0.1

print ('Please press buttons 1 + 2 on your Wiimote now ...')
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
    wii=cwiid.Wiimote()
except RuntimeError:
    print ("Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!")
    quit()

print ('Wiimote connection established!\n')


time.sleep(3)
#This activates the buttons, acclerometer, and the nunchuck
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK
#Now we set up the motor functions
def moveR(speedR):
    kit.motor1.throttle = speedR
    kit.motor2.throttle = speedR

def moveL(speedL):
    kit.motor3.throttle = speedL
    kit.motor4.throttle = speedL

while True:
    #This section defines the wii values. In the future, I will be using NunchuckStickX and NunchuckStickY to control mecanum wheels. Other properties will probably also be used.
    #Wiimote buttons
    buttons = wii.state['buttons']
    #this is the nunchuck buttons
    NunchuckBTN = wii.state['nunchuk']['buttons']
    #The joystick X axis
    NunchukStickX = (wii.state['nunchuk']['stick'][cwiid.X] - 127)
    #Now for the joystick's Y axis
    NunchukStickY = (wii.state['nunchuk']['stick'][cwiid.Y] - 128)
    #Now for the acclerometer
    #Nunchuck X axis
    NAccx = (wii.state['nunchuk']['acc'][cwiid.X] - 130)
    #Nunchuck Y axis
    NAccy = (wii.state['nunchuk']['acc'][cwiid.Y] - 130) / 50
    #Nunchuck Z axis
    NAccz = (wii.state['nunchuk']['acc'][cwiid.Z] - 130)
    forward = -(wii.state['acc'][cwiid.Y] - 125) /100 * 4
    #This section makes
    if (forward > .96):
        forward  = .96
    if (forward < -.96):
        forward  = -.96
    if (NAccy > .96):
        NAccy  = .96
    if (NAccy < -.96):
        NAccy = -.96
    #these sections control motion
    if (buttons & cwiid.BTN_B):
        moveR(forward)
    else:
        moveR(0)


    if (NunchuckBTN == 1):
        moveL(NAccy)
    else:

        moveL(0)
