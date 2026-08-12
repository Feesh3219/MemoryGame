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

sequence = [0, 2, 4, 6]  # hardcoded for now, add_led() replaces this in v0.8


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


def show(position):
    clear()
    np[position] = colours[position]
    np.write()


def show_sequence():
    clear()
    utime.sleep_ms(500)

    for position in sequence:
        show(position)
        utime.sleep_ms(250)
        clear()
        utime.sleep_ms(200)

    utime.sleep_ms(400)


# Timing test: replay the fixed sequence on a loop and check it's readable
while True:
    show_sequence()
    utime.sleep_ms(1000)
