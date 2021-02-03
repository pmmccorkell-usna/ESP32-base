Boot and Main run every time the ESP32 is started.
Their code is "blocking".
Boot runs first and errors can brick the device. Avoid putting code in boot.
Avoid putting blocking code in main until complete project. I like to put a library im working on at the end of main.py… such as:
import mylibrary
a = mylibrary
Saves lots of typing. Then I can immediately skip to a.mytestfunction(). 
Main runs after boot, and can prevent you from getting the command line. If you're having trouble accessing the serial command line, it's probably because something in Main is causing a delay and not permitting access yet.
There’s a number of helper functions in main, particularly “reload(hello_world)”. If you edit a python script, "reload(scriptname)” lets you reimport that library without having to restart the device.
Always double check and verify I2C pins in main vs the specific device and flavor you're using.

- ssid.py is where you can enter WiFi information. Needs to be updated with your network.
The actual connection is made in Main, which imports the lists in ssid.py
Due to the aforementioned timing issues, connecting to wifi is best done manually.
There's a function in main called "wifi()" ... enter that if you don't have a connection. It will do a wifi scan, and connect to the first match against the list in ssid.py
The scan, however, takes time.... and that can block people out. So I had to stop using it automatically.
On the plus side, the ESP32 will auto reconnect when you do a reset with CTRL+D. So you should only have to run this command again after a hard disconnect (loss of power or physically removed cord).
If you always want to connect to the first network in ssid.py, you can add the following line to main:  "connect_wifi(0)"

- webrepl_cfg.py enables the webpage connection.
Once the device is on a wifi network, write the IP address down (and save it, b/c usually it doesn’t change and it’s so nice to not need cords or upycraft). 
Go to https://micropython.org/webrepl/, and change ‘192.168.4.1’ to the device IP. Leave ‘ws’ (web browser protocol) and ‘8266’ (port number).
(advanced: you can also download that webpage, ctrl+f and change every instance of the IP in the html (use notepad++ or vsc), then double click the html into chrome and save it as a bookmark.)
Click ‘connect’ and the password is blank, just press Enter. You can change password in webrepl_cfg.
Use “send a file” and “get a file” on the right.
Send automatically overwrites.
( os.listdir() will list the files on device. )


- stats.py has some basic math stuff… mean, standard deviation, twos compliment. 

- umqttsimple.py for sending mqtt messages over wifi. MQTT is a small packet of data. Say a thermometer is attached to the device as a sensor. The ESP32 reads the sensor, but you want to wirelessly send that data every second to the Air Conditioner… MQTT is the way to do that. This is the building block of IOT / smarthome stuff.

- The bluetooth folder. This is code I got from micropython examples. Works w/ Bluefruit Connect app on phone.
A google search will probably reveal more interesting things for ESP32 & bluetooth, because that just gets you the same commandline as upycraft and webrepl.

General notes…
[TAB] will reveal available objects (functions and variables).
You can go down the levels in a library, ie mylibrary.[TAB] will reveal the objects under ‘mylibrary’
If you instantiated mylibrary, ie “a=mylibrary” … a.[TAB] will do the same.
This lets you see variables within the library’s scope, ie a.variable … or call functions like a.myfunction(var1,var2,var3,…)
Make liberal use of print() to identify why something isn’t working the way you expected it to.
Ctrl+D to soft restart.
Ctrl+C to cancel out of blocking code.
There’s a lot of python libraries built in that are not imported by default. Particularly ‘machine.Pin’, ‘machine.I2C’, etc.






