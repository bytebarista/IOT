
### Introduction / Background:
Use an IoT device to monitor a water level(empty state) in a water tank with heigh around 3-5ft. The device must be able to sends an SMS to a central(phone number) when a trash hold is reached. 

The device should be portable, cheep, easy to use and runs on low energy, preferably,  battery or some solar power system.  Also, the SMS must be configured to work in Sierra Leone, West Africa.

### Why the ESP32:
[ESP32](https://en.wikipedia.org/wiki/ESP32) are very portable [cheap](https://www.amazon.com/Espressif-ESP32-ESP32-DEVKITC-ESP-WROOM-32-soldered/dp/B01N0SB08Q) microcontrollers that runs on very [low-power](https://www.espressif.com/en/products/hardware/esp32/overview) compare to [Raspberry Pi](https://www.raspberrypi.org/) or [Arduino](https://store.arduino.cc/). It has an integrated WiFi(2.4 GHz band) and dual-mode Bluetooth along with dual high performance cores and with lots of RAM (520 kB).

### Why MicroPython
> MicroPython is a lean and efficient implementation of the Python 3
> programming language that includes a small subset of the Python
> standard library and is optimised to run on microcontrollers and in
> constrained environments

MicroPython is fully supported on ESP32 microcontrollers and makes it an excellent choice for this project. Implementing Deep-sleep on Esp32 using MicroPython is very simple, meaning, no need to implement some advanced deep-sleep. This is an excellent feature for for  is vital when building such device. 


*This guide assumes that MicroPython is already installed on the microcontroller.
If not, please check out [Flashing MicroPython on microcontroller](#flashing-mp-on-mc) below.*


The official MicroPython [documentation](http://docs.micropython.org/en/latest/) is well documented but i find this [MicroPython Programming Basics with ESP32 and ESP8266](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/) very useful and highly recommended for newbies MicroPython.

##### Required Materials
- ESP32 microcontroller
- Water level Floater sensor[Link]
- Micro-USB cable
- Access to the Internet
- Battery (Optional)

ESP32 Hardware overview
[Image of floater]


#Required Software
This guide assume that Python 3 is installed on your computer. 
If you don't have Python 3 installed, please install it from python.org[https://www.python.org/downloads/] or Homebrew.

If you are installing on Windows, make sure the “Add Python <x.x> to PATH” checkbox is selected.

 #### Install esptool and adafruit-ampy
Install ESPTool and Adafruit-ampy if you are on a Mac or Linux
ESPTool is a Python based utility tool used for communication with the ESP32 micro controller while Adafruit-ampy is a utility library to interact with a MicroPython board over a serial connection.

`$ pip install esptool adafruit-ampy`

If you don't have `pip` installed, run the command below
  `$ sudo easy_install pip`


### Establish Serial Connection with ESP32
See  https://docs.espressif.com/projects/esp-idf/en/latest/get-started/establish-serial-connection.html#establish-serial-connection-with-esp32

I recommend installing CP210x:  [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) 
[Enable OpenSSH Server](https://www.howtogeek.com/336775/how-to-enable-and-use-windows-10s-built-in-ssh-commands/) 

Virtual COM Port (VCP) Drive 
Verify that the driver is working by plugging your microcontroller into your computer. 
If you’re on Linux, check for /dev/ttyUSB0:
Or /dev/tty.SLAB_USBtoUART on macOS:
Windows: [System.IO.Ports.SerialPort]::getportnames() // tested on Windows 10 with  PowerShell

If not result, download the drive Virtual COM Port (VCP) Drive [https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers]



### Load MicroPython on the ESP32 microcontroller

    sudo pip install adafruit-ampy --upgrade

    ampy --port /dev/ttyUSB0 put blink.py
… reconnect to the serial console, and verify the file is there:

    >>> import os
    >>> os.listdir()
    ['boot.py', 'blink.py']

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


