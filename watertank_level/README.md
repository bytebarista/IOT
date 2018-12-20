# How to monitor water lever state with ESP32 and send SMS using Telerivet 

> **Disclaimer**: The scripts in this repo are copied from [Water level demo](https://github.com/SebastianRoll/micropython-libs/tree/master/micropython_libs/demos/watertank_level), that @SebastianRoll and I pair-programmed. However, some modifications has been made in the repo.

### Background
Use an IoT device to monitor a water level(empty & full state) in a water tank with heigh around 3-5ft and about 10,000L. The device must be able to sends an SMS to a phone number when the state changed. 

The device also should be portable, cheep, easy to use and runs on low energy, preferably battery or some solar power system.  In addition , the SMS must be configured to work in Sierra Leone, West Africa.

### Prototype solution
Use a **MicroPython** powered *ESP32 MicroController* (**MCU**) along with a *Vertical Float switch sensor*(**Floater**) and  *Telerivet Text Message Service*(**SMS Gateway**) .

### Why the ESP32 MicroController
[ESP32 MicroControllers](https://en.wikipedia.org/wiki/ESP32) are very portable, [cheap](https://www.amazon.com/Espressif-ESP32-ESP32-DEVKITC-ESP-WROOM-32-soldered/dp/B01N0SB08Q) microcontrollers that runs on very [low power](https://www.espressif.com/en/products/hardware/esp32/overview)  compare to [Raspberry Pi](https://www.raspberrypi.org/) or [Arduino](https://store.arduino.cc/) devices. They also have an integrated WiFi(2.4 GHz band) and dual-mode Bluetooth along with dual high performance cores and with lots of RAM (520 kB).

### Why MicroPython
> MicroPython is a lean and efficient implementation of the Python 3
> programming language that includes a small subset of the Python
> standard library and is optimised to run on microcontrollers and in
> constrained environments.   [- micropython.org](https://micropython.org/)


MicroPython is fully supported on **MCUs** and makes it an excellent choice for such quickly prototyping such project. Implementing Deep-sleep on **MCU** using [LoBo MicroPython for ESP32](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/rtc) is very simple, meaning, no need to implement some advanced deep-sleep. This is also a cool feature that preserves energy consumption. 


*This guide assumes that [MicroPython for ESP32 with psRAM support](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki) is already installed on the **MCU**, **Python 3** installed on your Personal Computer(**PC**) and  you have a valid [Telerivet](https://telerivet.com/product/messaging) account with an active Service Plan for Text Messaging.*
*If not, please check out [Flashing MicroPython on microcontroller](#flashing-mp-on-mc) below.*

Also, if you don't have **Python 3** installed, please install it from [python.org](https://www.python.org/downloads/) or Homebrew.
*If you are installing on **Windows**, make sure the **Add Python <x.x> to PATH** checkbox is selected.*

The official MicroPython [documentation](http://docs.micropython.org/en/latest/) is well documented. However, I find this [MicroPython Programming Basics with ESP32 and ESP8266](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/) tutorial very useful and highly recommended for IoT newbies like me.

### Why Telerivet
Telerivet was chosen because it simply works in [Sierra Leone](https://telerivet.com/product/messaging/country/SL) and has a very simple API. Twilio was the first candidate but doesn't have an SMS service for Sierra Leone.

##### Required Materials
- PC
- MCU
- Floater
- Micro-USB cable
- Access to the Internet
- Battery (Optional)

MCU Hardware Overview

![](https://github.com/LilyGO/ESP32-MINI-32-V2.0/blob/master/ZZ_Images/image1.jpg?raw=true)

Floater

Overview             |  Specifications
:-------------------------:|:-------------------------:
![](https://images-na.ssl-images-amazon.com/images/I/61Gz83YilTL._SL1500_.jpg?size=61644&height=400&width=400)  |  ![](https://ae01.alicdn.com/kf/HTB14FA2hlUSMeJjy1zjq6A0dXXaO.jpg?size=61644&height=642&width=665&hash=98a27caeff86c70e76ec888760011e54)




### Establish Serial Connection with MCU
Connect the **MCU** to you **PC** and run the following command to check if the serial drive is already installed.

**Microsoft Windows**
You may have to also [Enable OpenSSH](https://www.howtogeek.com/336775/how-to-enable-and-use-windows-10s-built-in-ssh-commands/) if your are running **Windows 10** and haven't already done that.

    PowerShell> [System.IO.Ports.SerialPort]::getportnames()

*Tested to work on Windows 10 with PowerShell*

If your output looks like **`COMX`** where **`X`** is the serial port number, then you are good to go, otherwise you have to download  and install [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) from Silabs or [FDTI Chip drive](https://www.ftdichip.com/Drivers/VCP.htm). Make sure you follow the instructions in the FDTI Chip comments area.

Also download and  install [PuTTY SSH Client](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) for debugging and monitoring the serial port.


**Mac OSX and Linux** 
If you’re on Linux, run verify your serial connection
```$ ls -l /dev/ttyUSB0:```

or on Mac OSX
```$ ls -l /dev/tty.SLAB_USBtoUART``` 

Your output should display something like `/dev/ttyUSB` on Linux and `/dev/tty.SLAB_USBtoUART` on Mac OSX, otherwise you have to download and install [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) from Silicon Labs.


### Loading and reading files on the MUC
Install **ESPTool** and **Adafruit-ampy** if you are running Mac OSX or Linux on your PC.
These are  Python based utility libraries used for communication and interacting with the  **MUC** over a serial connection.

Run ```$ pip install esptool adafruit-ampy``` to install them.
If you don't have `pip` installed, run  ```$ sudo easy_install pip``` to install

To load a file from the **MCU**, run the following command:
```$ ampy --port <SERIAL-PORT> put <FILE_PATH>```

To read a file from the **MCU**, run the following command:
```$ ampy --port <SERIAL-PORT> get <FILE_PATH>```

### Functional setup and testing
**Scripts files**
Download or clone this repo and unzip if chose to download.
Open *Command line or Power Shell* on your **PC** and `$ cd` to **`watertank_level`**
- **/boot.py** - This file will MicroPython run first when the **MCU** is boots or reset.
  *This file don't need to be modify, unless modifying MicroPython itself.*

- **/main.py** - This file runs right after **`/boot.py`** and contains the main script or logic.

- **/settings.py** - This file contains all the variable needed to successfully run the program.
  *This should be the ONLY file that need modification*

Open and modify  **`settings.py`**  with missing variables and save.

Copy these three files to the **MCU**   using  **`ampy`**  **put** command.
i.e on Mac OSX

```$ ampy --port /dev/tty.SLAB_USBtoUART put settings.py``` 

```$ ampy --port /dev/tty.SLAB_USBtoUART put main.py``` 

```$ ampy --port /dev/tty.SLAB_USBtoUART put boot.py``` 

To verify the copied files on the **MCU**, run **`ampy`** **get** command to read the files.
i.e on Mac OSX

```$ ampy --port /dev/tty.SLAB_USBtoUART **get** boot.py``` 

- Connect the **Vertical Float Switch** sensor to **Pin4** and **GND** on the **MCU**
- Open your Serial Monitor and reset the **MCU** or unplug it and plug it back in the PC.

#### Testing
*The **MCU** should go to deep-sleep mode when the **Floater/Ring Magnet** is at the top of the ***Internal Magnetic Reed Switch*** and wakes from deep sleep and sends SMS when at the bottom.*
![](https://ae01.alicdn.com/kf/HTB14FA2hlUSMeJjy1zjq6A0dXXaO.jpg?size=61644&height=642&width=665&hash=98a27caeff86c70e76ec888760011e54)

Placing the **Floater**  into a tank or container filled with water shouldn't send an SMS text message, but will print `$ Water Level Ok!` in the Serial Monitor.
***Ring Magnet should move to the top of the Internal Magnetic Reed Switch***

However, with less water in the tank or container an SMS should be send to the phone number given in **/settings.py** if the **MCU** is connected to the internet, Telerivet setup correctly.
***Ring Magnet should move to the bottom of the Internal Magnetic Reed Switch***

The Serial Monitor will show all log events if the **MCU** is connected to your **PC**.

> Note: SMS is send ONLY once in a single boot as of the current
> implementation, but will be improved when I have time.  Reset the
> **MCU** or unplug it and plug it back in the **PC** to retest resending the SMS.
> I apologize for that!

 
#### TODOs
- Improved SMS Sending to send 
- Send SMS on battery low
- Add GMS support

### Debugging
#### Debugging Windows
Connect the **MCU** to you **PC**
- Open PUTTY, select `Serial` and select the serial port `COMX`.
- Change the Baud Rate to `115200

Logs from the **MCU** should appear on *PUTTY* or *Serial Monitor*. 
Try soft resetting/reboot  by tapping to the reset button on the **MCU**


#### Debugging Linux and Mac OSX
TBA

### Troubleshooting:
<a name="flashing-mp-on-mc"><h4>Flashing MicroPython on MCU</a></h4>

Download and install [MicroPython_LoBo_esp32](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/raw/master/MicroPython_BUILD/firmware/MicroPython_LoBo_esp32.zip)
Connect the **MCU** to your **PC** via USB, and erase the entire flash using **Esptool**.

`$ esptool.py --chip esp32 erase_flash`

Then flash the downloaded firmware using the command below
`$ esptool.py --chip esp32 --port <SERIAL-PORT> write_flash -z 0x1000 esp32-xxxx-vx.xx.bin`

#### Micro-USB cable
Make sure you have a working Micro-USB before connecting the MCU to your PC.
This will save you a lot of time as I experienced when connecting MCUs, so I advice your to have more that *ONE* Micro-USB cables. 
