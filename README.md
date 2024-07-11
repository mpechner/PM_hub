# PM_hub
parachutemobile-aprs-hub

Task1 - learn how to control bluetooth from cli on Rapsberry Pi
# bluetoothctl
## turn bluetooth on and off
power [on|off]
## search for devices to pair with
scan on/off/bredr/le

* onfor all
* off
* le ble dewvices
* bredr old devices

When tsetting scan off you get the follwing
```
mpechner@pi5:~ $ bluetoothctl scan off
Failed to stop discovery: org.bluez.Error.Failed
```
to fix, reset the device

`sudo systemctl restart bluetooth`

