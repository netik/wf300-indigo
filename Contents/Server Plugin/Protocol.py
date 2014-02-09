class Protocol:
  # this is the color list inside of the WF300
  COLORLIST = ( "RED", "GREEN", "BLUE", "YELLOW", "PURPLE", "CYAN", "WHITE", "RED-HR-FD", "RED-HR-BD", "GREEN-HR-FD", "GREEN-HR-BD", "BLUE-HR-FD", "BLUE-HR-BD", "RED-HR-LC", "GREEN-HR-DC", "3B-HR-BF", "3M-HR-BB", "3B-HR-BDC", "3M-HR-BLC", "7-HR-BF", "7-HR-BBD", "7-HR-BDC", "7-HR-BLC", "3B-BF", "3B-BB", "3M-BF", "3M-BB", "7-BF", "7-BD", "3B-BDC", "3B-BLC", "7-BDC", "7-BLC", "3B-F", "7-F", "3B-GC", "3M-GC", "7-JC", "GBY-FD", "BYC-BD", "3M-FD", "3M-FD", "BYC-F", "GB_DC", "BY_LC", "7W-FD", "7W-BD", "BT-BD", "RT-FD", "RT-BD", "GT-FD", "GT_BD", "BT-FD", "YT-FD", "CT-FD", "PT-BD", "WT-FD", "WT-BD", "7T-BD", "7T-FD", "YRY-CF", "PRP-CF", "PRP-CB", "YGY-CF", "YGY-CB", "CGC-CF", "CGC-CB", "PBP-CF", "PBP-CB", "CBC-CF", "CBC-CB", "WRW-CF", "WRW-CB", "GRG-CF", "BRB-CB", "YRY-CF", "YRY-CB", "RYR", "RPR", "GCG", "GYG", "BPB", "AUTO8-82" ) 

  # SPI byte ordering
  SPI = ( "RGB", "RBG", "GRB", "GBR", "BRG", "BGR" ) 

  # supported LED controllor chips
  CHIPS = ( "LDP6803", "TM1803", "UCS1903", "WS2811", "TM1812", "TM1809", "WS2801", "TLS3001", "TLS3008", "P9813" ) 

  # add more modes here as we find them. 
  MODE_PAUSE=6
  MODE_OFF=2
  MODE_ON=3
  MODE_SPEED=4 

  all = [0] *10
  checkValue = '\0'
  colorRGB = [ 0, 0, 0 ]
  SPIICtype = 1
  SPIsequence = 4
       # SPISequence - this is how color is sent based on this table: 
                          # RBG = 1
                          # GRB = 2
                          # GBR = 3
                          # BRG = 4
                          # BGR = 5 
 
  # was -86,85. Unsure why ? 
  # the boot sector of drives is 0x55, 0xaa. What if this is reversed?
  # 0xaa = 1010 1010, 0x55 = 0101 0101 ! 
  frameHead = []
  frameHead.append( 0xAA )
  frameHead.append( 0x55 )

  keyNum = 0
  keyNumber = 0
  keyValue = 0
  mode = 0
  serverPort = '\0'
  setupspieditvalue = 150

  bar_no = 0 # wtf is this? 

  def exchangeInt(self, paramArrayOfInt ):
    i = paramArrayOfInt[0]
    j = paramArrayOfInt[1]
    k = i & 0xF0;
    m = (i & 0xF) << 4;
    n = j & 0xF0;
    i1 = j & 0xF;
    i2 = k + (n >> 4);
    i3 = m + i1;

    paramArrayOfInt[0] = i2
    paramArrayOfInt[1] = i3

  def exchangeBytes(self, paramArrayOfByte):
    if len(paramArrayOfByte) != 10:
      return

    arrayOfInt = [0]*10

    i = 0 
    while i < 5:
      arrayOfInt[0] = paramArrayOfByte[i]
      arrayOfInt[1] = paramArrayOfByte[(9 - i)]
      self.exchangeInt(arrayOfInt)

      paramArrayOfByte[i] = arrayOfInt[0]
      paramArrayOfByte[(9 - i)] = arrayOfInt[1]

      i = i + 1

  def getAll(self):
    # this works for static strips that have one color. 
    self.all[0] = self.frameHead[0]
    self.all[1] = self.frameHead[1]
    self.all[2] = 0
    self.all[3] = self.mode
    self.all[4] = self.keyNum
    self.all[5] = self.bar_no
    self.all[6] = self.colorRGB[0]
    self.all[7] = self.colorRGB[1]
    self.all[8] = self.colorRGB[2]
    self.all[9] = self.getCurCheckValue(self.bar_no, self.colorRGB[0], self.colorRGB[1], self.colorRGB[2], self.keyNum)
    return self.all

  def spi_getAll(self):
    # in this mode, the controller does all the work. I do not think
    # you can send brightness or color here. 
    self.all[0] = self.frameHead[0]
    self.all[1] = self.frameHead[1]
    self.all[2] = 0x81 # -127 
    self.all[3] = self.SPIICtype              # set based on the chip
    self.all[4] = self.setupspieditvalue >> 8 # SPIEdit Value (MSB?), the number of pixels in the string)
    self.all[5] = self.setupspieditvalue      # SPIEdit Value (LSB?)
    self.all[6] = self.keyNum    # this does something, not sure? 
    self.all[7] = self.keyValue  # THIS IS THE PROGRAM. CONFIRMED.  aka, bar_no? 
    self.all[8] = self.SPIsequence
    self.all[9] = 0
    # as it turns out this check digit is meaningless on SPI. 
#    self.all[9] = self.getCurCheckValue(50, self.colorRGB[0], self.colorRGB[1], self.colorRGB[2], 0)
    self.exchangeBytes(self.all)
    return self.all

  def getCurCheckValue(self,paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):
    i = paramInt5 + (paramInt4 + (paramInt3 + (paramInt2 + (paramInt1 + 255))) + self.mode);

    # this logic seems bad. 
    if (i == 0):
      return 0xff & i

    j = i % 255

    if (j == 0):
      j = 255;

    # perhaps no need to cast to byte here, as we're already modulo 255.
    self.checkValue = j  
    return self.checkValue;

  def findProgram(self,name):
    i=0
    for c in self.COLORLIST:
      if self.COLORLIST[i] == name.upper():
        return i+1
      i=i+1

    return None

  def setColorRGB(self, paramInt1, paramInt2, paramInt3):
    self.colorRGB[0] = 0xff & paramInt1
    self.colorRGB[1] = 0xff & paramInt2
    self.colorRGB[2] = 0xff & paramInt3

  def setKeyNumber(self, paramInt):
    if (paramInt > 5) or (paramInt < 1):
      return

    self.keyNumber = 0xff & paramInt

  def setKeyValue(self,paramInt):
    self.keyValue = 0xff & paramInt

  def setMode(self,paramInt):
    if (paramInt > 3) or (paramInt < 1):
      return

    self._mode = 0xff & paramInt

  def turnOff(self):
    self.keyNum=2
    self.keyValue=10

if __name__ == "__main__":
	p = Protocol()
	for val in  p.spi_getAll():
	   print "%0x " % val
	
	
