# Project Status and Milestones
## Augist 17, 2024
The Pi has the baseline configuration.  It comes up as a AP  serving 192.168.10.1/24 on wifi.  It is running mosquitto MQTT. 

The  Adafruit QT board runs a sample that just sends base packet.  I tested that I can hold the board at variouos location on my body and the packets are received. Code is cliewnts/testclient/code.py.
### next
* Do a from screatch of the raspberry pi. I've tweaked and reran the setup script numerous times.
* Write a client using PAHO that runs on the raspberry pi and logs the messages is a consumable format.
