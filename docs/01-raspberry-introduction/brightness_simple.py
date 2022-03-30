from gpiozero import PWMLED
from signal import pause

led = PWMLED(14)

led.pulse()

pause()