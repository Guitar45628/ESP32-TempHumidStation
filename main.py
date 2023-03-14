from machine import Pin, SoftI2C
from time import sleep
import utime
import time
import ssd1306
import machine
import power_options
import network
import ntptime
import program
import G_System

#ประกาศตัวแปรสำหรับสีบนหน้าจอ ssd1306
fg = 1 #fg = สีพื้นหน้า
bg = 0 #bg = สีพื้นหลัง
# Set up the I2C connection and SSD1306 display
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
BUZZER_PIN = Pin(5, Pin.OUT)
sta_if = network.WLAN(network.STA_IF)

menu_options = ["IoT-ESP32", "Clock", "WiFi Setup", "Power"]
current_option = 0
# Define the pin numbers for the buttons
select_button = Pin(4, Pin.IN, Pin.PULL_UP)
confirm_button = Pin(23, Pin.IN, Pin.PULL_UP)
gmp7 = [07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00,01,02,03,04,05,06]

def sound():
    BUZZER_PIN.value(0)
    sleep(0.1)
    BUZZER_PIN.value(1)
    sleep(0.1)
    
def show_options(timy):
    oled.fill(0)
    for x in range(0, 10, 5):
        for y in range(0, 10, 5):
            oled.fill_rect(x, y, 4, 4, fg)
    oled.text("Start", 10, 1)
    oled.line(0, 10, 128, 10, 1)
    #oled.text("> " + menu_options[current_option], 0, 15)

    for i in range(len(menu_options)):
        if i == current_option:
            a,b,c,d = 0,12+10*i,128,9
            oled.fill_rect(a, b, c, d, fg)
            oled.text("> " + menu_options[i], 0, 13 + 10*i,bg)
        else:
            oled.text(menu_options[i], 0, 13 + 10*i)
            oled.line(0,53,128,53,fg)
            if sta_if.isconnected():
                x,y = 1,63
                for i in range(4):
                    oled.line(x, y, x, y - 2*i-1, fg)
                    x += 2
                oled.text(f'{sta_if.config('essid')}',8,56,fg)
            else:
                oled.text(f'No WiFi!',0,55,fg)
    #oled.fill_rect(80,0,48,9,bg)
    oled.line(82,0,82,10,fg)
    oled.text(timy,85,1,fg)
    oled.text(":",101,1,fg)
    oled.show()

def wifisetup():
    wifi_options = ["IOT-WU", "Testing", "3BB_5323_2.4GHz", "IoTC603","Back"]
    current_option = 0
    def showwifi():
        oled.fill(0)
        for x in range(0, 10, 5):
            for y in range(0, 10, 5):
                oled.fill_rect(x, y, 4, 4, fg)
        oled.text("WiFi Setup", 10, 1)
        oled.line(0, 10, 128, 10, 1)
        #oled.text("> " + menu_options[current_option], 0, 15)

        for i in range(len(wifi_options)):
            if i == current_option:
                a,b,c,d = 0,12+10*i,128,9
                oled.fill_rect(a, b, c, d, fg)
                oled.text("> " + wifi_options[i], 0, 13 + 10*i,bg)
            else:
                oled.text(wifi_options[i], 0, 13 + 10*i)
        oled.show()
    while True:
        showwifi()
        if select_button.value()==0:
            sound()
            current_option += 1
            if current_option >= len(wifi_options):
                current_option = 0
            utime.sleep(0.2)

        if confirm_button.value() == 0:
            sound()
            selected_option = wifi_options[current_option]
            oled.fill(0)

            if selected_option == "IOT-WU":
                G_System.selfconnect("IOT-WU", "iot123456")
            elif selected_option == "Testing":
                G_System.selfconnect("Testing", "00000000")
            elif selected_option == "3BB_5323_2.4GHz":
                G_System.selfconnect("3BB_5323_2.4GHz", '410093526')
            elif selected_option == "IoTC603":
                G_System.selfconnect("IoTC603","ccsadmin")
            elif selected_option == "Back":
                break
    
G_System.start_clock()    
while True:
    current_time = utime.localtime()
    timy = ("{:02d}:{:02d}".format(current_time[3], current_time[4]))
    show_options(timy)
    if select_button.value()==0:
        sound()
        current_option += 1
        if current_option >= len(menu_options):
            current_option = 0
        utime.sleep(0.2)

    if confirm_button.value() == 0:
        sound()
        selected_option = menu_options[current_option]
        oled.fill(0)

        if selected_option == "IoT-ESP32":
            print("Selected Option 1")
            program.P01_DHTtoTHINKSPEAKandLDR()
        elif selected_option == "Clock":
            program.P03_Clock()
        elif selected_option == "Power":
            power_options.show_power_options()
        elif selected_option == "WiFi Setup":
            wifisetup()
            
        utime.sleep(2)



