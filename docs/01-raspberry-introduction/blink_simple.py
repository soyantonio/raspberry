from gpiozero import LED
from signal import pause

led = LED(14)

led.blink()

pause()