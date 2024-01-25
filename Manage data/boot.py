# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
import time
#import ntptime
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

#ntptime.settime() # this queris the time from an NTP server
#UTC_OFFSET = 5.5*60*60

ssid = 'raspi-iiot'
password = 'hussain2024'
mqtt_server = '10.3.141.1'
client_id = ubinascii.hexlify(machine.unique_id())

#topic_sub = b'notification'
topic_pub = b'RFID ON ESP3'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
#ntptime.settime()

webrepl.start()
