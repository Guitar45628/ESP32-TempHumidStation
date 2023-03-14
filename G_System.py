from machine import Pin, SoftI2C
import utime
import ssd1306
import network
import time

#ประกาศตัวแปรสำหรับ led
led = Pin(2, Pin.OUT)
###Screen###
#ประกาศตัวแปรสำหรับสีบนหน้าจอ ssd1306
fg = 1 #fg = สีพื้นหน้า
bg = 0 #bg = สีพื้นหลัง
SCREEN_WIDTH = 128 #กำหนดความกว้างของจอ
SCREEN_HEIGHT = 64 #กำหนดความยาวของจอ
# Set up the I2C connection and SSD1306 display
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

###Boot Screen###
def bootscreen():
    # Set start time
    start_time = utime.ticks_ms()

    # Set up I2C interface for OLED
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    # Function to draw progress bar
    def draw_progress_bar(x, y, width, height, progress):
        oled.rect(x, y, width, height, fg)
        oled.fill_rect(x, y, int(width*progress), height, fg)
        oled_show()

    # Function to show OLED display
    def oled_show():
        oled.show()

    # Clear display and draw "Kartie OS" text in center
    oled.fill(bg)
    oled.text("KARTIE OS", int(oled_width/2)-int(len("KARTIE OS")*8/2), int(oled_height/2)-16, fg)
    oled_show()
    # Draw progress bar for 2 seconds
    while utime.ticks_ms() - start_time < 500:
        for i in range(20,108,2):
            draw_progress_bar(i, 50, 2, 2, (i-20)/88)
            utime.sleep_ms(5)

    # Clear display
    oled.fill(bg)
    oled_show()

###LED Blink###
def led_blink(time):
    led.value(0)
    for i in range(time):
        led.value(0)
        utime.sleep(0.2)
        led.value(1)
        utime.sleep(0.2)
    led.value(0)
    
##MSG BOX###
def msgbox(title,msg,c):
    oled.fill(bg)
    d = 35
    b = int(((64-d)/2)-5)
    a = int((128-c)/2)
    #oled.rect(20, 12, 88, 30, fg)
    oled.fill_rect(a, b, c, d, fg)
    for i in range(3):
        oled.pixel(a+i,b,bg)
        oled.pixel(a,b+i,bg)
    for i in range(3):
        oled.pixel((a+c-1)-i,b,bg)
        oled.pixel((a+c-1),b+i,bg)
    for i in range(3):
        oled.pixel((a+c-1),(b+d-1)-i,bg)
        oled.pixel((a+c-1)-i,(b+d-1),bg)
    for i in range(3):
        oled.pixel(a,(b+d-1)-i,bg)
        oled.pixel(a+i,(b+d-1),bg)
    oled.text(title, int(128/2)-int(len(title)*8/2), int(64/2)-20, bg)
    oled.line(a,b+12,a+c,b+12,bg)
    oled.text(msg, int(128/2)-int(len(msg)*8/2), int(64/2)-4, bg)
    oled.show()
    utime.sleep(0.5)
    
###WIFI CONNECTION###
wifi_credentials = [
    ("IOT-WU", "iot123456"),
    ("Testing", "00000000"),
    ("3BB_5323_2.4GHz", '410093526'),
    ("IoTC603","ccsadmin")
]

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        for ssid, password in wifi_credentials:
            print("Trying to connect to", ssid)
            msgbox(ssid,"Connecting..",120)
            try:
                sta_if.connect(ssid, password)
                utime.sleep(3)
            except:
                print('Error connecting to network:', ssid)
                msgbox(ssid,"WiFi Error!",120)
                continue
    if sta_if.isconnected():
        print(f'WiFi connected:{sta_if.config('essid')},', sta_if.ifconfig()[0])
        #show_on_screen("WiFi Connected", sta_if.config('essid'),sta_if.ifconfig()[0],"")
        msgbox(sta_if.config('essid'),"Connected!",120)
        led_blink(2)
        #bootscreen() 
        
def selfconnect(ssid,password):
    try:
        print("Connecting..")
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(ssid, password)
        while not wifi.isconnected():
            utime.sleep(1)
        msgbox(wifi.config('essid'),"Connected!",120)
    except:
        print("WiFi Lost")
        print('Error connecting to network:', ssid)
    
def start_clock():
    def getntp():
        try:
            print("Getting ntptime")
            ntptime.settime()
            pass
        except:
            msgbox("Time Config","Getting ntp",105)
            utime.sleep(5)
            getntp()
    
    current_time = utime.localtime()
    timy = ("{:02d}:{:02d}".format(current_time[3], current_time[4]))
    print(f'Clock: {timy}')
    