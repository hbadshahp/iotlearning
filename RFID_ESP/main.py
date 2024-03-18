# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from machine import Pin
from machine import SPI

def connect_and_subscribe():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server,1883,"npdAtom","npd@Atom")
  client.connect()
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
  
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
  
spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
# Using Hardware SPI pins:
#     sck=18   # yellow
#     mosi=23  # orange
#     miso=19  # blue
#     rst=4    # white
#     cs=5     # green, DS
# *************************
# To use SoftSPI,
# from machine import SOftSPI
# spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
print("Place card")
card_id_com = ""

while True:
  (stat, tag_type) = rdr.request(rdr.REQIDL)
  try:
    client.check_msg()
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]) + " "+client_id
            
            if card_id_com == "":
                client.publish(topic_pub,card_id)
                card_id_com = card_id;
                print(card_id)
            elif card_id_com == card_id:
                continue;
            else:
                client.publish(topic_pub,card_id)
                card_id_com = card_id;
                print(card_id)
                        
            #print(time.localtime(time.time() + int(UTC_OFFSET)))
            
  except OSError as e:
    restart_and_reconnect()
    