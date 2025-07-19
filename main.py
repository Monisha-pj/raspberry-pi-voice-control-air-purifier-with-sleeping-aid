import speech_recognition as sr
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from datetime import date
from gpiozero import LED
from time import sleep
import pygame

# File paths for audio
sleeping_music = "/home/pi/sleeping_music.mp3"
turn_on = "/home/pi/on.mp3"
turn_off = "/home/pi/off.mp3"

# Initialize audio
pygame.mixer.init()
speaker_volume = 0.5
pygame.mixer.music.set_volume(speaker_volume)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)

# LCD setup (modify pins as per your circuit)
lcd1 = 2
lcd2 = 3
lcd3 = 27
lcd4 = 22
lcd5 = 10
lcd6 = 9
lcd = LCD.Adafruit_CharLCD(lcd1, lcd2, lcd3, lcd4, lcd5, lcd6, 0, 16, 2)

# Date
today_date = date.today()

# LED Setup
red_led = LED(17)

# Speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("System initialized. Listening...")

try:
    while True:
        # Display air quality status based on GPIO input
        if GPIO.input(14):
            lcd.clear()
            lcd.message("Date: " + str(today_date))
            lcd.message("\nAir Quality: Bad")
        else:
            lcd.clear()
            lcd.message("Date: " + str(today_date))
            lcd.message("\nAir Quality: Good")
        sleep(2)
        lcd.clear()

        # Voice command block
        with mic as source:
            print("Listening for command...")
            audio = recognizer.listen(source)

        try:
            words = recognizer.recognize_google(audio).lower()
            print("You said:", words)

            if "turn on" in words:
                print("Turning red LED on")
                pygame.mixer.music.load(turn_on)
                pygame.mixer.music.play()
                red_led.on()

            elif "turn off" in words:
                print("Turning red LED off")
                pygame.mixer.music.load(turn_off)
                pygame.mixer.music.play()
                red_led.off()

            elif "music on" in words:
                print("Playing sleeping music")
                pygame.mixer.music.load(sleeping_music)
                pygame.mixer.music.play()

            elif "music off" in words:
                print("Stopping music")
                pygame.mixer.music.stop()

            elif "exit" in words:
                print("Exiting program...")
                sleep(1)
                print("Goodbye!")
                break

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    lcd.clear()
    lcd.message("Cleaning up...")
    GPIO.cleanup()
    print("GPIO cleaned up.")
