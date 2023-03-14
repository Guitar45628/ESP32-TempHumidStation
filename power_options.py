from machine import Pin, SoftI2C
from time import sleep
import ssd1306, time, machine
import sys
import utime
import G_System

# Set foreground and background colors
fg = 1
bg = 0

BUZZER_PIN = Pin(5, Pin.OUT)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


def sound():
    BUZZER_PIN.value(0)
    sleep(0.1)
    BUZZER_PIN.value(1)
    sleep(0.1)
    
def show_power_options():
    options = ["Shutdown", "Reboot", "Sleep","Back"]
    current_option = 0
    def show_options():
        oled.fill(bg)
        oled.text("Power option:", 0, 0,fg)
        oled.line(0, 10, 128, 10, fg)
        a,b,c,d = 0,14,128,9
        oled.fill_rect(a, b, c, d, fg)
        oled.text("> " + options[current_option], 0, 15,bg)
        if current_option == 1:
            oled.text(options[2], 0, 25,fg)
            oled.text(options[3], 0, 35,fg)
            oled.text(options[0], 0, 45,fg)
        elif current_option == 2:
            oled.text(options[3], 0, 25,fg)
            oled.text(options[0], 0, 35,fg)
            oled.text(options[1], 0, 45,fg)
        elif current_option == 3:
            oled.text(options[0], 0, 25,fg)
            oled.text(options[1], 0, 35,fg)
            oled.text(options[2], 0, 45,fg)
        else:
            oled.text(options[1], 0, 25,fg)
            oled.text(options[2], 0, 35,fg)
            oled.text(options[3], 0, 45,fg)
        
            
        oled.show()

    select_pin = Pin(4, Pin.IN, Pin.PULL_UP)
    confirm_pin = Pin(23, Pin.IN, Pin.PULL_UP)

    while True:
        show_options()

        if select_pin.value()==0:
            sound()
            current_option += 1
            if current_option >= len(options):
                current_option = 0
            time.sleep(0.2)

        if confirm_pin.value() == 0:
            sound()
            selected_option = options[current_option]

            if selected_option == "Shutdown":
                G_System.msgbox("Shutting down..",125)
                oled.poweroff()
                print("System is shutting down...")
                sys.exit()
            elif selected_option == "Reboot":
                G_System.msgbox("Rebooting...",110)
                machine.reset()
            elif selected_option == "Back":
                break
                machine.reset()
            elif selected_option == "Sleep":
                G_System.msgbox("Use EN to wake",125)
                oled.poweroff()
                machine.lightsleep()
                
            time.sleep(2)

