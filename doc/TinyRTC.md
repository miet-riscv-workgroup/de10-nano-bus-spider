# TinyRTC I2C module

* http://www.dx.com/en/p/i2c-rtc-ds1307-24c32-real-time-clock-module-for-arduino-blue-149493
* https://electronics.stackexchange.com/questions/242159/what-are-all-these-pins-on-the-ds1307-rtc-for
* http://we.easyelectronics.ru/Shematech/platka-rasshireniya-tiny-rtc-i2c-modules.html

```
HiZ> S

     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:       -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: 50 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- -- 

### 24C32N
HiZ> [ 0xa0 0 0 [ 0xa1 r r r r ]
I2C START BIT
WRITE: 0xa0 ACK
WRITE: 0x00 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xa1 ACK
READ: 0xff ACK
READ: 0xff ACK
READ: 0xff ACK
READ: 0xff NACK
I2C STOP BIT
HiZ> [ 0xa0 0 0 0x12 0x34 0x45 0x67 ]
I2C START BIT
WRITE: 0xa0 ACK
WRITE: 0x00 ACK
WRITE: 0x00 ACK
WRITE: 0x12 ACK
WRITE: 0x34 ACK
WRITE: 0x45 ACK
WRITE: 0x67 ACK
I2C STOP BIT
HiZ> [ 0xa0 0 0 [ 0xa1 r r r r ]
I2C START BIT
WRITE: 0xa0 ACK
WRITE: 0x00 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xa1 ACK
READ: 0x12 ACK
READ: 0x34 ACK
READ: 0x45 ACK
READ: 0x67 NACK
I2C STOP BIT
HiZ>

# DS1307
HiZ> [ 0xd0 0x00 0x50 0x59 0x02 ]
I2C START BIT
WRITE: 0xd0 ACK
WRITE: 0x00 ACK
WRITE: 0x50 ACK
WRITE: 0x59 ACK
WRITE: 0x02 ACK
I2C STOP BIT
HiZ> [ 0xd0 0x00 [ 0xd1 r r r ]
I2C START BIT
WRITE: 0xd0 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xd1 ACK
READ: 0x56 ACK
READ: 0x59 ACK
READ: 0x02 NACK
I2C STOP BIT
HiZ> [ 0xd0 0x00 [ 0xd1 r r r ]
I2C START BIT
WRITE: 0xd0 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xd1 ACK
READ: 0x57 ACK
READ: 0x59 ACK
READ: 0x02 NACK
I2C STOP BIT
HiZ> [ 0xd0 0x00 [ 0xd1 r r r ]
I2C START BIT
WRITE: 0xd0 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xd1 ACK
READ: 0x59 ACK
READ: 0x59 ACK
READ: 0x02 NACK
I2C STOP BIT
HiZ> [ 0xd0 0x00 [ 0xd1 r r r ]
I2C START BIT
WRITE: 0xd0 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xd1 ACK
READ: 0x01 ACK
READ: 0x00 ACK
READ: 0x03 NACK
I2C STOP BIT
HiZ> [ 0xd0 0x00 [ 0xd1 r r r ]
I2C START BIT
WRITE: 0xd0 ACK
WRITE: 0x00 ACK
I2C START BIT
WRITE: 0xd1 ACK
READ: 0x03 ACK
READ: 0x00 ACK
READ: 0x03 NACK
I2C STOP BIT
HiZ> 
```
