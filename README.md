# esphome-for-deye
Made for Deye SUN-12K-SG04LP3.
I guess it also works for SUN-5/6/8/10/-SG04LP3 as the modbus adresses is most likely the same.
For other models & sunsync. I cant support those as they use other addresses and the "modbus" interface in the inverter is different.

For use with ESP32 & TTL To RS485 Module with automatic flow control.
I powered the esp32 from CN2 pin 7&8 with 12V into a USB converter.

This include all addresses i could see relevant from the inverter. 
Including Changing time of use, Charge/discharge amps etc.

![esp32 rs485_bb](https://user-images.githubusercontent.com/22115157/211201233-f5fe9189-e6b3-4ee1-9baa-48068f078127.jpg)

![image](https://user-images.githubusercontent.com/22115157/211201343-1d54cada-4b2c-40b0-88c4-faf31e17fead.png)

