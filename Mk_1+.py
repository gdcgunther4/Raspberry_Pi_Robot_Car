# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following lines of code demonstrate many of the features realted to wiimotes, such as capturing button presses and rumbling the controller.
# I have managed to map the home button to the accelerometer - simply hold it and values will appear!

# Coded by The Raspberry Pi Guy. Work based on some of Matt Hawkins's!
import cwiid
from adafruit_motorkit import MotorKit

kit = MotorKit()
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
print ('Go ahead and press some buttons\n')
print ('Press PLUS and MINUS together to disconnect and quit.\n')

time.sleep(3)

wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK

def moveR(speedR):
    kit.motor1.throttle = speedR
    kit.motor2.throttle = speedR

def moveL(speedL):
    kit.motor3.throttle = speedL
    kit.motor4.throttle = speedL

while True:
    buttons = wii.state['buttons']
    NunchuckBTN = wii.state['nunchuk']['buttons']
    #X axis:LeftMax = 25, Middle = 125, RightMax = 225
    NunchukStickX = (wii.state['nunchuk']['stick'][cwiid.X] - 127)
    #Y axis:DownMax = 30, Middle = 125, UpMax = 225
    NunchukStickY = (wii.state['nunchuk']['stick'][cwiid.Y] - 128)
    #The nunchuk has an accelerometer that records in a similar manner to the wiimote, but the number range is different
    #The X range is: 70 if tilted 90 degrees to the left and 175 if tilted 90 degrees to the right
    NAccx = (wii.state['nunchuk']['acc'][cwiid.X] - 127)
    #The Y range is: 70 if tilted 90 degrees down (the buttons pointing down), and 175 if tilted 90 degrees up (buttons pointing up)
    NAccy = (wii.state['nunchuk']['acc'][cwiid.Y] - 130) / 50
    #I still don't understand the z axis completely (on the wiimote and nunchuk), but as far as I can tell it's main change comes from directly pulling up the mote without tilting it
    NAccz = (wii.state['nunchuk']['acc'][cwiid.Z] - 127)
    forward = -(wii.state['acc'][cwiid.Y] - 125) /100 * 4

    if (forward > .96):
        forward  = .96
    if (forward < -.96):
        forward  = -.96
    if (NAccy > .96):
        NAccy  = .96
    if (NAccy < -.96):
        NAccy = -.96

    # Detects whether + and - are held down and if they are it quits the program

    if (buttons & cwiid.BTN_B):
        moveR(forward)
    else:
        moveR(0)


    if (NunchuckBTN == 1):
        moveL(NAccy)
    else:

        moveL(0)