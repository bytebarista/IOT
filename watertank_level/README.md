
### Background
Use an IoT device to monitor a water level(empty & full state) in a water tank with heigh around 3-5ft and about 10,000L. The device must be able to sends an SMS to a central(phone number) when the state changed. 

The device should be portable, cheep, easy to use and runs on low energy, preferably battery or some solar power system.  Also, the SMS must be configured to work in Sierra Leone, West Africa.

### Why the ESP32
[ESP32](https://en.wikipedia.org/wiki/ESP32) are very portable [cheap](https://www.amazon.com/Espressif-ESP32-ESP32-DEVKITC-ESP-WROOM-32-soldered/dp/B01N0SB08Q) microcontrollers that runs on very [low-power](https://www.espressif.com/en/products/hardware/esp32/overview) compare to [Raspberry Pi](https://www.raspberrypi.org/) or [Arduino](https://store.arduino.cc/) devices. ESP32 also has an integrated WiFi(2.4 GHz band) and dual-mode Bluetooth along with dual high performance cores and with lots of RAM (520 kB).

### Why MicroPython
> MicroPython is a lean and efficient implementation of the Python 3
> programming language that includes a small subset of the Python
> standard library and is optimised to run on microcontrollers and in
> constrained environments

MicroPython is fully supported on ESP32 microcontrollers and makes it an excellent choice for such project. Implementing Deep-sleep on Esp32 using MicroPython is very simple, meaning no need to implement some advanced deep-sleep. This is also a cool feature for power consumption. 


*This guide assumes that MicroPython is already installed on the microcontroller.
If not, please check out [Flashing MicroPython on microcontroller](#flashing-mp-on-mc) below.*


The official MicroPython [documentation](http://docs.micropython.org/en/latest/) is well documented but i find this [MicroPython Programming Basics with ESP32 and ESP8266](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/) very useful and highly recommended for newbies MicroPython.

##### Required Materials
- ESP32 microcontroller
- Water level Floater sensor
- Micro-USB cable
- Access to the Internet
- Battery (Optional)

ESP32 microcontroller
![](https://github.com/LilyGO/ESP32-MINI-32-V2.0/blob/master/ZZ_Images/image1.jpg?raw=true)

Water level Float Switch
![](https://images-na.ssl-images-amazon.com/images/I/61Gz83YilTL._SL1500_.jpg)


### Establish Serial Connection with ESP32
This guide assume that Python 3 is installed on your computer. If you don't have Python 3 installed, please install it from [python.org](https://www.python.org/downloads/) or Homebrew.

*If you are installing on Windows, make sure the “Add Python <x.x> to PATH” checkbox is selected.*


Connect the microcontroller to you computer and run the following command to check if you already have a serial drive install.

#### Windows users
You may have to also [Enable OpenSSH](https://www.howtogeek.com/336775/how-to-enable-and-use-windows-10s-built-in-ssh-commands/) if your are running Windows 10 and haven't already done that.

Connect your 

`PS> [System.IO.Ports.SerialPort]::getportnames()` 

*Tested on Windows 10 with  PowerShell*

If your output looks like `COMX` where `X` is the port number, then you are good to go. Skip to the next step.

Download and install [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) from Silabs or [FDTI Chip drive](https://www.ftdichip.com/Drivers/VCP.htm). 
Make sure you follow the instructions in the FDTI Chip comments area.

I also recommend installing [Arduino IDE] (https://www.arduino.cc/en/main/software) for debugging on Windows.



#### Mac OSX and Linux 
If you’re on Linux, check for `$ ls -l /dev/ttyUSB0:` or `$ ls -l /dev/tty.SLAB_USBtoUART` on Mac OSX.

Your output should display something like `/dev/tty**`, otherwise you have to download and install [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) from Silicon Labs.


### Loading and reading files on the microcontroller
Install ESPTool and Adafruit-ampy if you are running Mac OSX or Linux on your computer.
ESPTool is a Python based utility tool used for communication with the ESP32 microcontrollers, while Adafruit-ampy is a utility library, with tools for interacting with a microcontrollers over a serial connection.

`$ pip install esptool adafruit-ampy`

If you don't have `pip` installed, run the command below  `$ sudo easy_install pip`


To load a file from the microcontroller, run the following command:

`$ ampy --port <SERIAL_PORT> put <FILE_PATH>`


To read a file from the microcontroller, run the following command:
`$ ampy --port <SERIAL_PORT> get <FILE_PATH>`


### Debugging

#### Windows
Connect the microcontroller to you computer
- Open Arduino IDE, navigate to `Tools -> Port` and select the serial port `COMX`.
- Next navigate again to `Tools -> Serial Monitor`
- Change the Baud Rate to `115200

Logs from the microcontroller should apear now. Try soft resetting the microcontrollers by tapping to the reset button.


#### Linux and Mac OSX

`$ picocom -b115200 <SERIAL_PORT_PATH>`
TBA

### Troubleshooting:

<a name="flashing-mp-on-mc"><h4>Flashing MicroPython on microcontroller</a></h4>

Download the latest firmware for [ESP32 boards](http://micropython.org/download#esp32)

Connect the microcontroller to your computer via USB, and erase the entire flash using Esptool.

`$ esptool.py --chip esp32 erase_flash`

Then flash the downloaded firmware using the command below
`$ esptool.py --chip esp32 --port <PORT-PATH> write_flash -z 0x1000 esp32-xxxxxxx-vx.xx.bin`

#### Micro-USB cable
Make sure you have a working Micro-USB before connecting the microcontroller to your computer.
This will save you a lot of time as I experenced when connecting microcontrollers, so I advice your to have more that *ONE* Micro-USB cables. 


