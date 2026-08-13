from machine import Pin, ADC, PWM
import neopixel
import utime
import urandom

# Hardware pins
LED_PIN = 28
NUM_LEDS = 8

X_PIN = 27
Y_PIN = 26

SW_PIN = 14
BUZZER_PIN = 15

# Joystick limits
MIN_VAL = 5000
MAX_VAL = 60535

# Set up NeoPixel ring
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# Set up joystick
x_axis = ADC(X_PIN)
y_axis = ADC(Y_PIN)

# Set up joystick button
button = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

# Set up buzzer
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty_u16(0)

# Colours for each LED
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

# Different buzzer frequency for each LED
tones = [300, 400, 500, 600, 700, 800, 900, 1000]

# Game variables
sequence = []
player = 0
score = 0


# Converts joystick values into -1, 0 or 1
def zone(value):
    if value < MIN_VAL:
        return -1
    elif value > MAX_VAL:
        return 1
    return 0


# Converts joystick direction into an LED number
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


# Turns all LEDs off
def clear():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)

    np.write()


# Displays one LED
def show(position):
    clear()
    np[position] = colours[position]
    np.write()


# Plays the tone for an LED
def beep(position, time):
    buzzer.freq(tones[position])
    buzzer.duty_u16(20000)

    utime.sleep_ms(time)

    buzzer.duty_u16(0)


# Flashes all LEDs a colour
def flash(colour):
    for _ in range(2):

        for i in range(NUM_LEDS):
            np[i] = colour

        np.write()
        utime.sleep_ms(100)

        clear()
        utime.sleep_ms(100)


# Checks if the joystick button was pressed
def pressed():
    if button.value() == 0:

        utime.sleep_ms(20)

        if button.value() == 0:

            while button.value() == 0:
                utime.sleep_ms(5)

            return True

    return False


# Adds a random LED to the sequence
def add_led():
    new_led = urandom.getrandbits(3)
    sequence.append(new_led)

    print("New LED:", new_led)


# Shows the memory sequence
def show_sequence():

    print("Showing sequence...")

    clear()
    utime.sleep_ms(500)

    for position in sequence:

        print("LED:", position)

        show(position)
        beep(position, 250)

        clear()
        utime.sleep_ms(200)

    utime.sleep_ms(400)

    print("Sequence finished")


# Handles the player's turn
def play_round():

    global player
    global score

    print("Waiting for answer...")

    for target in sequence:

        while True:

            pos = joystick()

            if pos is not None:

                player = pos
                show(player)

            # Lock in answer
            if pressed():

                print("Selected:", player)
                print("Target:", target)

                # Check answer
                if player == target:

                    score += 100

                    print("Correct!")
                    print("Score:", score)

                    beep(target, 100)

                    break

                else:

                    print("Wrong!")

                    return False

            utime.sleep_ms(50)

    return True


# Resets the game
def game_over():

    global score
    global player

    print()
    print("GAME OVER")
    print("Final score:", score)
    print()

    flash((255, 0, 0))

    sequence.clear()

    score = 0
    player = 0

    utime.sleep_ms(700)


# Start game
print("Press joystick to start")

while not pressed():
    utime.sleep_ms(10)

print("GAME START")
print()

beep(0, 150)


# Main game loop
while True:

    print("Round:", len(sequence) + 1)

    # Add another LED to the sequence
    add_led()

    # Show sequence
    show_sequence()

    # Reset player
    player = 0
    show(player)

    # Check player's answers
    if play_round():

        print("Round complete!")
        print()

        flash((0, 255, 0))

        utime.sleep_ms(500)

    else:

        game_over()

        print("Press joystick to restart")

        while not pressed():
            utime.sleep_ms(10)

        print()

        beep(0, 150)
