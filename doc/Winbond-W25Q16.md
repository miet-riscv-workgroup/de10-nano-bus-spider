# Winbond W25Q16 16M-bit Serial Flash Memory

See JEDEC ID (9Fh) command response (chapter 10.2.27 from [Winbond-w25q32.pdf](https://elinux.org/images/f/f5/Winbond-w25q32.pdf) ):

```
0xEF --- Winbond
0x40 0x15 --- W25Q16
```

Bus Spider log:

```
HiZ> m
 1. HiZ
 2. I2C
 3. SPI
>>> 3
  SPI mode selected

SPI> [ 0x9f r r r ]
/CS ENABLED
WRITE: 0x9f
READ: 0xef
READ: 0x40
READ: 0x15
/CS DISABLED
SPI>
```


See also

* [ILS - CJMCU-2516 Memory Module W25Q16BVSIG Serial SPI Flash 16M-BIT](https://www.amazon.com/ILS-CJMCU-2516-Memory-W25Q16BVSIG-16M-BIT/dp/B0768D2H2N)
