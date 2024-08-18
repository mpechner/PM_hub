# just a collection of commands

# list for mqtt messages
mosquitto_sub -h localhost -u parachutemobile -P parachutemobile  -v -t timer

# setup initial mqtt password
sudo mosquitto_passwd  -b /etc/mosquitto/passwd parachutemobile parachutemobile
