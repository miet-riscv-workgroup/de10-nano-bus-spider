# демонстрация LCD1X9

See https://www.youtube.com/watch?v=xk4pjrGDSXQ#t=4m15s

```
[ 0x70 0xc8 0xf0 0xe0 0x08 0xd0 0xd4 ] -> 9
[ 0x70 0xc8 0xf0 0xe0 0x0c 0xd0 0xd4 ] -> 9
[ 0x70 0xc8 0xf0 0xe0 0x10 0x90 0x96 ] -> 0
[ 0x70 0xc8 0xf0 0xe0 0x14 0x91 0x07 ] -> M
[ 0x70 0xc8 0xf0 0xe0 0x18 0x40 0xd6 ] -> E
[ 0x70 0xc8 0xf0 0xe0 0x1c 0x00 0x00 ]
[ 0x70 0xc8 0xf0 0xe0 0x20 0x00 0x00 ]
[ 0x70 0xc8 0xf0 0xe0 0x00 0x00 0x00 ]
```

Put letter E into position 3:
```
 HiZ>[ 0x70 0xc8 0xf0 0xe0 0x18 0x40 0xd6 ]
 I2C START BIT
 WRITE: 0x70 ACK
 WRITE: 0xc8 ACK
 WRITE: 0xf0 ACK
 WRITE: 0xe0 ACK
 WRITE: 0x18 ACK
 WRITE: 0x40 ACK
 WRITE: 0xd6 ACK
 I2C STOP BIT
 I2C>
```

```diff
- тут фото
```
 
* https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/open-source-hardware
* https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/resources/MOD-LCD-1x9-schematic.pdf
* https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/resources/LCD1X9.pdf
* https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/resources/MOD-LCD-1x9_support-files-v1.00(MOD-ZIGBEE).zip
 
* http://dangerousprototypes.com/docs/Practical_guide_to_Bus_Pirate_pull-up_resistors

```
 I2C>W
 Power supplies ON
 I2C>P
 Pull-up resistors ON

 I2C>[ 0x70 0xc8 0xf0 0xe0 0x0 0xff 0xff 0xff 0xff 0xff 0xff 0xf0 0xf0 ]
 I2C START BIT
 WRITE: 0x70 ACK 
 WRITE: 0xC8 ACK 
 WRITE: 0xF0 ACK 
 WRITE: 0xE0 ACK 
 WRITE: 0x00 ACK 
 WRITE: 0xFF ACK 
 WRITE: 0xFF ACK 
 WRITE: 0xFF ACK 
 WRITE: 0xFF ACK 
 WRITE: 0xFF ACK 
 WRITE: 0xFF ACK 
 WRITE: 0xF0 ACK 
 WRITE: 0xF0 ACK 
 I2C STOP BIT
 I2C>
```


```
 result |= local_I2C_WriteByte(LCD1x9_SLAVE_ADDR | 0x00);^M
 result |= local_I2C_WriteByte(0b11001000); // mode register
 result |= local_I2C_WriteByte(0b11110000); // blink register
 result |= local_I2C_WriteByte(0b11100000); // device select register
 result |= local_I2C_WriteByte(0b00000000); // pointer register

 // light up all the segments, initialize the local display buffer as well
 for(i = 0; i < 20; i++)
 {
    result |= local_I2C_WriteByte(0xFF);
    lcdBitmap[i] = 0xFF;
 }
```
