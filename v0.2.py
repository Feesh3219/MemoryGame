from machine import Pin, ADC, PWM
import neopixel
import utime

LED_PIN = 28
NUM_LEDS = 8

X_PIN = 27
Y_PIN = 26

SW_PIN = 14
BUZZER_PIN = 15

MIN_VAL = 5000
MAX_VAL = 60535

np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

x_axis = ADC(X_PIN)
y_axis = ADC(Y_PIN)

button = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty_u16(0)

colours = [
    (255, 0, 0),
    (255, 80, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (150, 0, 255),
    (255, 0, 100)
]


def zone(value):
    if value < MIN_VAL:
        return -1
    elif value > MAX_VAL:
        return 1
    return 0


def joystick():
    x = zone(x_axis.read_u16())
    y = zone(y_axis.read_u16())

    mapping = {
        (0, 1): 0,
        (-1, 1): 1,
        (-1, 0): 2,
        (-1, -1): 3,
        (0, -1): 4,
        (1, -1): 5,
        (1, 0): 6,
        (1, 1): 7
    }

    return mapping.get((x, y))


def clear():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()


# Direction test: the LED that lights should always match the joystick's
# physical direction, all the way around the ring, with no dead spots.
while True:
    pos = joystick()

    if pos is not None:
        clear()
        np[pos] = colours[pos]
        np.write()

    utime.sleep_ms(50)
