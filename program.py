from machine import Pin, SoftI2C
from time import sleep, time
import ssd1306
import dht
import urequests
import network
import machine
import utime
import ntptime
import G_System

# Initialize peripherals
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
sensor_dht = dht.DHT22(Pin(18))
ldr = Pin(19, Pin.IN)
led = Pin(2, Pin.OUT)
buzzer = Pin(5, Pin.OUT)
back_button = Pin(4, Pin.IN, Pin.PULL_UP)
# Set foreground and background colors
fg = 1
bg = 0
API_KEY = "ZC7O9CCTOD0XEY2S" # ThingSpeak API key

def P01_DHTtoTHINKSPEAKandLDR():
    print("---Program 1---")
    print("Checking WiFi connection")
    print("Checking DHT22 measurement")
    
    def get_req():
        sta_if = network.WLAN(network.STA_IF)
        if sta_if.isconnected():
            try:
                sensor_dht.measure()
                return True
            except OSError:
                print("DHT22 not found!")
                G_System.msgbox("Sensor Error","Not found!",128)
                return False
        else:
            print("No WiFi plase use program 2")
            G_System.msgbox("Error No WiFi","Program2 Active",128)
            P02_DHTandLDR()
            return False
    
    def check_req():
        if get_req():
            return True
        else:
            return False
        
    def send_data(): #Send to ThinkSpeak
        temp, hum = get_data()
        if temp is not None and hum is not None:
            try:
                print('Sending data to ThingSpeak')
                led.value(0)
                utime.sleep(0.1)
                led.value(1)
                response = urequests.get(
                    f'https://api.thingspeak.com/update?api_key={API_KEY}&field1={temp}&field2={hum}&field3={ldr.value()}')
                response.close()
                print(f'Sent data to ThingSpeak at timestamp:{last_update_time}')
                utime.sleep(0.1)
                led.value(0)
            except Exception as e:
                print("Error sending data to ThingSpeak:", e)
                
    def get_data(): #Ger from DHT22
        try:
            sensor_dht.measure()
            temp = sensor_dht.temperature()
            hum = sensor_dht.humidity()
            if temp is not None or hum is not None:
                return temp, hum
            else:
                raise ValueError("DHT22 sensor returned invalid data")
            
        except Exception as e:
            print("Error reading DHT22 sensor:", e)
            pass
    def show_data(clock):
        try:
            temp, hum = get_data()
        except:
            pass
        
        print(get_data())
        oled.fill(bg)
        #oled.text(f"{APP_NAME} v{APP_VER}", 0, 2,fg)
        oled.text(f'IoT-ESP32  {clock}',0,2,fg)
        oled.text('_' * 128, 2, 5,fg)
        oled.text("  Temp | Humid  ", 2, 19, fg)
        oled.text("-------|--------", 2, 30, fg)
        oled.text(f"{'  {:.1f}'.format(temp)} | {'{:.1f}'.format(hum)}  ", 2, 40, fg)
        oled.text("    C  |   %    ", 2, 50, fg)
        oled.text("   .            ", 2, 45, fg)
        oled.show()
        utime.sleep(0.5)
    
    last_update_time = time()
    gmp7 = [07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00,01,02,03,04,05,06]
    
    while check_req():
        if back_button.value() == 0:
            break
        current_time = utime.localtime()
        sec_time = current_time[5]
        clock = ("{:02d}:{:02d}".format(current_time[3], current_time[4]))
        led.value(0)
        if ldr.value() == 1:
            utime.sleep(0.1)
            led.value(1)
            print("Detected")
            show_data(clock)
        else:
            utime.sleep(0.1)
            led.value(0)
            oled.fill(0)
            oled.show()
       # Print the current time
        last_sync = time() - last_update_time
        print("Sync:", last_sync ,"s ago")
        if last_sync >= 30: #avg30
            send_data()
            last_update_time = time()
        utime.sleep(0.75)
        
def P02_DHTandLDR():
    print("---Program 2---")
    print("Checking DHT22 measurement")
    
    def get_req():
        try:
            sensor_dht.measure()
            return True
        except OSError:
            print("DHT22 not found!")
            G_System.msgbox("Sensor Error","Not found!",128)
            return False
    
    def check_req():
        if get_req():
            return True
        else:
            return False
                
    def get_data(): #Ger from DHT22
        try:
            sensor_dht.measure()
            temp = sensor_dht.temperature()
            hum = sensor_dht.humidity()
            if temp is not None or hum is not None:
                return temp, hum
            else:
                raise ValueError("DHT22 sensor returned invalid data")
        except Exception as e:
            print("Error reading DHT22 sensor:", e)
            pass
    def show_data(clock):
        try:
            temp, hum = get_data()
        except:
            pass
        
        print(get_data())
        oled.fill(bg)
        oled.text(f'No WiFi  {clock}',0,2,fg)
        oled.text('_' * 128, 2, 5,fg)
        oled.text("  Temp | Humid  ", 2, 19, fg)
        oled.text("-------|--------", 2, 30, fg)
        oled.text(f"{'  {:.1f}'.format(temp)} | {'{:.1f}'.format(hum)}  ", 2, 40, fg)
        oled.text("    C  |   %    ", 2, 50, fg)
        oled.text("   .            ", 2, 45, fg)
        oled.show()
        utime.sleep(0.5)
    
    last_update_time = time()
    gmp7 = [07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00,01,02,03,04,05,06]
    
    while check_req():
        if back_button.value() == 0:
            break
        current_time = utime.localtime()
        clock = ("{:02d}:{:02d}".format(gmp7[current_time[3]], current_time[4]))
        led.value(0)
        if ldr.value() == 1:
            utime.sleep(0.1)
            led.value(1)
            print("Detected")
            show_data(clock)
        else:
            utime.sleep(0.1)
            led.value(0)
            oled.fill(0)
            oled.show()
        utime.sleep(0.75)
  
def P03_Clock():
    try:
        ntptime.settime()
    except:
        pass
    gmp7 = [07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,00,01,02,03,04,05,06]
    while True:
        if back_button.value() == 0:
            break
        current_time = utime.localtime()
        clock = ("{:02d}:{:02d}:{:02d}".format(gmp7[current_time[3]], current_time[4], current_time[5]))
        print(clock)
        G_System.msgbox("Clock",clock,100)
        utime.sleep(0.5)
