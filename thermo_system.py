#!/usr/bin/python
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import requests
import spidev
import time
import datetime
from firebase import firebase
from scipy.stats import mode

# initialize Firebase
firebase = firebase.FirebaseApplication('https://thermo-system.firebaseio.com', None)
    
# create SPI to check Moisture
spi = spidev.SpiDev()
spi.open(0,0)
    
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# init list with pin numbers int the 4 Channel Relay
light = 2
water = 3
fans  = 4
heat  = 17
pinList = [light,water,fans,heat]

def irrigation(water_time):
    
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)    
    for i in pinList: 
        GPIO.setup(i, GPIO.OUT) 
        GPIO.output(i, GPIO.HIGH)
    resultLight = firebase.post('/Data/2018/November/Light', False)
    resultWater = firebase.post('/Data/2018/November/Water', False)
    resultFans = firebase.post('/Data/2018/November/Fans', False)
    resultHeat = firebase.post('/Data/2018/November/Heat', False)
            
    # irrigation loop
    print '\n Date: '+str(now.month)+'/'+str(now.day)+'/'+str(now.year)
    print ' Time: '+str(now.hour)+':'+str(now.minute)
    print '\n Irrigation System ON for '+ str(water_time)+' seconds'
    endTime = time.time() + water_time
    
    while time.time() < endTime:
      try:
          GPIO.output(water, GPIO.LOW)          
          resultLight = firebase.post('/Data/2018/November/Light', False)
          resultWater = firebase.post('/Data/2018/November/Water', True)
          resultFans = firebase.post('/Data/2018/November/Fans', False)
          resultHeat = firebase.post('/Data/2018/November/Heat', False)
          
      # end program cleanly with keyboard
      except KeyboardInterrupt:
          print ' Quit\n'
    
    GPIO.output(water, GPIO.HIGH)
    print '\n Irrigation System OFF'
    resultLight = firebase.post('/Data/2018/November/Light', False)
    resultWater = firebase.post('/Data/2018/November/Water', False)
    resultFans = firebase.post('/Data/2018/November/Fans', False)
    resultHeat = firebase.post('/Data/2018/November/Heat', False)
    
def test_Relay():
    
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)    
    for i in pinList: 
        GPIO.setup(i, GPIO.OUT) 
        GPIO.output(i, GPIO.HIGH)
    resultLight = firebase.post('/Data/2018/November/Light', False)
    resultWater = firebase.post('/Data/2018/November/Water', False)
    resultFans = firebase.post('/Data/2018/November/Fans', False)
    resultHeat = firebase.post('/Data/2018/November/Heat', False)
        
    # time to sleep between operations in the test loop
    SleepTimeL = 10

    # test loop
    print '\n Date: '+str(now.month)+'/'+str(now.day)+'/'+str(now.year)
    print ' Time: '+str(now.hour)+':'+str(now.minute)
    print '\n Testing Relay: \n'
    endTime = time.time() + 30

    while time.time() < endTime:
      try:
          time.sleep(3);
          GPIO.output(light, GPIO.LOW)
          resultLight = firebase.post('/Data/2018/November/Light', True)
          print ' ONE - Lights ON'
          time.sleep(SleepTimeL)
          GPIO.output(light, GPIO.HIGH)
          resultLight = firebase.post('/Data/2018/November/Light', False)
      
          GPIO.output(water, GPIO.LOW)
          esultWater = firebase.post('/Data/2018/November/Water', True)
          print ' TWO - Water Pump ON'
          time.sleep(5) 
          GPIO.output(water, GPIO.HIGH)
          esultWater = firebase.post('/Data/2018/November/Water', False)
      
          GPIO.output(fans, GPIO.LOW)
          resultFans = firebase.post('/Data/2018/November/Fans', True)
          print ' THREE - Fans ON'
          time.sleep(SleepTimeL)
          GPIO.output(fans, GPIO.HIGH)
          resultFans = firebase.post('/Data/2018/November/Fans', False)
      
          GPIO.output(heat, GPIO.LOW)
          resultHeat = firebase.post('/Data/2018/November/Heat', True)
          print ' FOUR - Heater ON'
          time.sleep(SleepTimeL)
          GPIO.output(heat, GPIO.HIGH)
          resultHeat = firebase.post('/Data/2018/November/Heat', False)
          
      # end program cleanly with keyboard
      except KeyboardInterrupt:
          print ' Quit\n'
          
    GPIO.cleanup()
    print '\n Testing Relay Completed!'


def readadc(adcnum):
    
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def read_MOIST():
    
    # define Variables to check Moisture
    delay = 0.5
    value = 0
    moist0_List = []
    moist1_List = []
    moist2_List = []
    moist3_List = []
    moist4_List = []
    moist5_List = []
    moist6_List = []
    moist7_List = []
    moistCheck_List = []
    
    while value < 6: 
        
        # read data the MCP3008
        ldr_value0 = readadc(0)
        # print("LDR Value 0: %d" % ldr_value0)
        moist0_List.append(ldr_value0)
        
        ldr_value1 = readadc(1)
        # print("LDR Value 1: %d" % ldr_value1)
        moist1_List.append(ldr_value1)
        
        ldr_value2 = readadc(2)        
        # print("LDR Value 2: %d" % ldr_value2)
        moist2_List.append(ldr_value2)
        
        ldr_value3 = readadc(3)        
        # print("LDR Value 3: %d" % ldr_value3)
        moist3_List.append(ldr_value3)
        
        ldr_value4 = readadc(4)        
        # print("LDR Value 4: %d" % ldr_value4)
        moist4_List.append(ldr_value4)
        
        ldr_value5 = readadc(5)        
        # print("LDR Value 5: %d" % ldr_value5)
        moist5_List.append(ldr_value5)
        
        ldr_value6 = readadc(6)
        # print("LDR Value 6: %d" % ldr_value6)
        moist6_List.append(ldr_value6)
        
        ldr_value7 = readadc(7)
        # print("LDR Value 7: %d" % ldr_value7)
        moist7_List.append(ldr_value7)
        
        time.sleep(0.1)                
        value = value + 1
        # end while
    
    print "---------------------------------------"
    ldr_val0 = float(mode(moist0_List)[0])
    print("LDR Value 0: %d" % ldr_val0)
    moistCheck_List.append(ldr_val0)
    
    ldr_val1 = float(mode(moist1_List)[0])
    print("LDR Value 1: %d" % ldr_val1)
    moistCheck_List.append(ldr_val1)
    
    ldr_val2 = float(mode(moist2_List)[0])
    print("LDR Value 2: %d" % ldr_val2)
    moistCheck_List.append(ldr_val2)
    
    ldr_val3 = float(mode(moist3_List)[0])
    print("LDR Value 3: %d" % ldr_val3)
    moistCheck_List.append(ldr_val3)
    
    ldr_val4 = float(mode(moist4_List)[0])
    print("LDR Value 4: %d" % ldr_val4)
    moistCheck_List.append(ldr_val4)
    
    ldr_val5 = float(mode(moist5_List)[0])
    print("LDR Value 5: %d" % ldr_val5)
    moistCheck_List.append(ldr_val5)
    
    ldr_val6 = float(mode(moist6_List)[0])
    print("LDR Value 6: %d" % ldr_val6)
    moistCheck_List.append(ldr_val6)
    
    ldr_val7 = float(mode(moist7_List)[0])
    print("LDR Value 7: %d" % ldr_val7)
    moistCheck_List.append(ldr_val7)
    print "---------------------------------------"
    
    check_mode = float(mode(moistCheck_List)[0])
    check_max = max(moistCheck_List)
    
    need_water = False
    
    if check_mode < 100 and check_max < 800:
        need_water = True
        print " Our plants need more water"
        return (need_water)
    else:
        return(need_water)
    
def read_DHT():

    value = 0
    temp1_List = []
    temp2_List = []
    temp3_List = []
    tempIn_List = []
    humi1_List = []
    humi2_List = []
    humi3_List = []
    humiIn_List = []
    print '\n Reading DHT - Temperature and Humidity: '

    while value < 6: # 6 = 1 minute, 30 = 5 mintutes
                
        # read data from pins: 25,23,24
        humi1, temp1 = Adafruit_DHT.read_retry(11,25) #temp sensor 1 out 
        humi2, temp2 = Adafruit_DHT.read_retry(11,23) #temp sensor 2 in top
        humi3, temp3 = Adafruit_DHT.read_retry(11,24) #temp sensor 3 in bottom     
                
        # Get average inside Temperature and Huminity
        tempIn = (temp2 + temp3)/2
        humiIn = (humi2 + humi3)/2
                
        #print ('The' + str(value) + 'reading is:')
        print ' Temperature Outside: {0:0.1f}C   Temperature Inside: {1:0.1f}C  ({2:0.1f}C - {3:0.1f}C) '.format(temp1,tempIn,temp2,temp3)
        print ' Humidity Outside:    {0:0.1f}%   Humidity Inside:    {1:0.1f}%  ({2:0.1f}% - {3:0.1f}%) \n'.format(humi1,humiIn,humi2,humi3)
                
        time.sleep(10)
        temp1_List.append(temp1)
        temp2_List.append(temp2)
        temp3_List.append(temp3)
        tempIn_List.append(tempIn)
        humi1_List.append(humi1)
        humi2_List.append(humi2)
        humi3_List.append(humi3)
        humiIn_List.append(humiIn)
                
        value = value + 1
    
    temp_1  = float(mode(temp1_List)[0])
    temp_2  = float(mode(temp2_List)[0])
    temp_3  = float(mode(temp3_List)[0])
    temp_In = float(mode(tempIn_List)[0])
    humi_1  = float(mode(humi1_List)[0])
    humi_2  = float(mode(humi2_List)[0])
    humi_3  = float(mode(humi3_List)[0])
    humi_In = float(mode(humiIn_List)[0])
                
    return (temp_1,temp_In,temp_2,temp_3,humi_1,humi_In,humi_2,humi_3)          


now = datetime.datetime.now()
print '\n Date: '+str(now.month)+'/'+str(now.day)+'/'+str(now.year)
print ' Time: '+str(now.hour)+':'+str(now.minute)

startDate = now.day
startMonth = now.month

# print Welcome
print ('\n Welcome to the Sustainable Thermo-System !!!\n')

# code asks for user input
x = raw_input('Would you like to execute the system?\n')

if x == 'y' or x == 'Y' or x == 'yes' or x == 'Yes' or 'YES':
    systemOn = True
else:
    systemOn = False
    
    
while systemOn is True:
  try:  
    # call test relay function
    # b = test_Relay()
    
    resultError = firebase.post('/Data/2018/November/Errors', "No Errors")
    
    appDaysOn = firebase.get('/Data/2018/November/DaysOn', None)
    daysOn = int(appDaysOn)
    endTime = time.time() + 60*60*24*daysOn # 60sec*60min*24hr*30days
    #while time.time() < endTime:
    
    # retrieve SystemOn from Firebase
    appSystemOn = firebase.get('/Data/2018/November/SystemOn', None)

    while appSystemOn is True and time.time() < endTime:
      try:  
        # call read DHT function
        DHT = read_DHT()
               
        # set temperatures
        TempOut = DHT[0]
        TempIn  = DHT[1]
        
        # set max humidity
        HumiOut = DHT[4]
        HumiIn  = DHT[5]
        maxHumi = 82
        
        # post data to Firebase
        new_temp = str(TempIn)
        new_humi = str(HumiIn)
        resultTemp = firebase.post('/Data/2018/November/Temperature', new_temp)
        resultHumi = firebase.post('/Data/2018/November/Humidity', new_humi)
        
        # retrieve data from Firebase
        # appMaxTemp = firebase.get('/Data/2018/November/AppMaxTemperature', None)
        # appMinTemp = firebase.get('/Data/2018/November/AppMinTemperature', None)
        # maxTemp = int(appMaxTemp)
        # minTemp = int(appMinTemp)
                
        timeRema = endTime - time.time()
        if (timeRema > 48):
            print '\n Remaining time: '+str(int(timeRema/(3600*24)))+' days ('+str(int(timeRema/(3600)))+' hrs)'
        elif (24 < timeRema and timeRema < 48):
            print '\n Remaining time: 1 day and '+str(int(timeRema/(3600)-24))+' hrs'
        else:
            print '\n Remaining time: '+str(int(timeRema/(3600)))+' hrs'
        
        remaDays = str(int(timeRema/(3600*24)))
        resultRemaDays = firebase.post('/Data/2018/November/RemaDays', remaDays)
        
        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for i in pinList: 
            GPIO.setup(i, GPIO.OUT) 
            GPIO.output(i, GPIO.HIGH)
        resultLight = firebase.post('/Data/2018/November/Light', False)
        resultWater = firebase.post('/Data/2018/November/Water', False)
        resultFans = firebase.post('/Data/2018/November/Fans', False)
        resultHeat = firebase.post('/Data/2018/November/Heat', False)
            
        # set daytime
        now = datetime.datetime.now()
        if (5 < now.hour and now.hour < 22):
            print ' Date: '+str(now.month)+'/'+str(now.day)+'/'+str(now.year)
            print ' Time: '+str(now.hour)+':'+str(now.minute)
            minTemp = 25
            resultMinTemp = firebase.post('/Data/2018/November/MinTemperature', str(minTemp))
            maxTemp = 30
            resultMaxTemp = firebase.post('/Data/2018/November/MaxTemperature', str(maxTemp))
            dayTime = 1
            GPIO.output(light, GPIO.LOW)
            resultLight = firebase.post('/Data/2018/November/Light', True)
            resultWater = firebase.post('/Data/2018/November/Water', False)
            resultFans = firebase.post('/Data/2018/November/Fans', False)
            resultHeat = firebase.post('/Data/2018/November/Heat', False)
            print " Day Time - Lights ON\n"
            
        else:
            print ' Date: '+str(now.month)+'/'+str(now.day)+'/'+str(now.year)
            print ' Time: '+str(now.hour)+':'+str(now.minute)
            minTemp = 25
            resultMinTemp = firebase.post('/Data/2018/November/MinTemperature', str(minTemp))
            maxTemp = 30
            resultMaxTemp = firebase.post('/Data/2018/November/MaxTemperature', str(maxTemp))
            
            GPIO.output(light, GPIO.HIGH)
            resultLight = firebase.post('/Data/2018/November/Light', False)
            print " Night Time - Lights OFF\n"
            if (startDate < (now.day) or startMonth < (now.month)):
                # call test relay function
                # test_Relay()
                startDate = now.day
                startMonth = now.month
                moist = read_MOIST()
                
                if moist == True:
                    print " The plants need more water"
                    irrigation(6)    
                else:
                    print " The plants are good in water"
                
        time.sleep(10)
        
        # setmode GPIO
        GPIO.setmode(GPIO.BCM)
        
        if (TempIn < minTemp):
            print ' The temperature outside is '+str(TempOut)+'C'
            print ' The temperature inside is '+str(TempIn)+'C lower than expected'
            GPIO.output(light, GPIO.HIGH)
            #print " Turn Lights OFF"
            GPIO.output(water, GPIO.HIGH)
            #print ' Turn Water OFF'
            GPIO.output(fans, GPIO.HIGH)
            #print " Turn Fans OFF"
            GPIO.output(heat, GPIO.LOW)
            print " Turn Heater ON"
            resultLight = firebase.post('/Data/2018/November/Light', False)
            resultWater = firebase.post('/Data/2018/November/Water', False)
            resultFans = firebase.post('/Data/2018/November/Fans', False)
            resultHeat = firebase.post('/Data/2018/November/Heat', True)
            time.sleep(120)
            
        elif (TempIn > maxTemp):
            print ' The temperature outside is '+str(TempOut)+'C'
            print ' The temperature inside is '+str(TempIn)+'C higher than expected'
            GPIO.output(light, GPIO.HIGH)
            #print " Turn Lights OFF"
            GPIO.output(water, GPIO.HIGH)
            #print ' Turn Water OFF'
            GPIO.output(fans, GPIO.LOW)
            print " Turn Fans ON"
            GPIO.output(heat, GPIO.HIGH)
            #print " Turn Heater OFF"
            resultLight = firebase.post('/Data/2018/November/Light', False)
            resultWater = firebase.post('/Data/2018/November/Water', False)
            resultFans = firebase.post('/Data/2018/November/Fans', True)
            resultHeat = firebase.post('/Data/2018/November/Heat', False)
            time.sleep(60)
        else:
            print ' The temperature outside is '+str(TempOut)+'C'
            print ' The temperature inside is '+str(TempIn)+'C as expected'
            
        time.sleep(10)
        
        if (HumiIn > maxHumi):
            print ' The humidity outside is '+str(HumiOut)+'%'
            print ' The humidity inside is '+str(HumiIn)+'% higher than expected'
            GPIO.output(light, GPIO.HIGH)
            #print " Turn Lights OFF"
            GPIO.output(water, GPIO.HIGH)
            #print ' Turn Water OFF'
            GPIO.output(fans, GPIO.HIGH)
            #print " Turn Fans OFF"
            GPIO.output(heat, GPIO.LOW)
            print " Turn Heater ON"
            resultLight = firebase.post('/Data/2018/November/Light', False)
            resultWater = firebase.post('/Data/2018/November/Water', False)
            resultFans = firebase.post('/Data/2018/November/Fans', False)
            resultHeat = firebase.post('/Data/2018/November/Heat', True)
            time.sleep(120)
        else:
            print ' The humidity outside is '+str(HumiOut)+'%'
            print ' The humidity inside is '+str(HumiIn)+'% as expected'
            
        # update SystemOn from Firebase
        appSystemOn = firebase.get('/Data/2018/November/SystemOn', None)
        
        # end while loop
      except requests.exceptions.HTTPError:
        resultError = firebase.post('/Data/2018/November/Errors', "HTTP error")
      except requests.exceptions.SSLError:
        resultError = firebase.post('/Data/2018/November/Errors', "SSL error")
      except requests.exceptions.ReadTimeout:
        resultError = firebase.post('/Data/2018/November/Errors', "Read Timeout error")
      time.sleep(10)
      #except KeyboardInterrupt:
        #resultError = firebase.post('/Data/2018/November/Errors', "Interrupt error")
        #print ' Quit\n'
        
    # After while loop turn OFF everything
    
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in pinList: 
        GPIO.setup(i, GPIO.OUT) 
        GPIO.output(i, GPIO.HIGH)
    resultLight = firebase.post('/Data/2018/November/Light', False)
    resultWater = firebase.post('/Data/2018/November/Water', False)
    resultFans = firebase.post('/Data/2018/November/Fans', False)
    resultHeat = firebase.post('/Data/2018/November/Heat', False)
    print ' System is OFF'
    resultError = firebase.post('/Data/2018/November/Errors', "Thermo-System is OFF")
    time.sleep(10)
    # end while loop
    
  except requests.exceptions.HTTPError:
    resultError = firebase.post('/Data/2018/November/Errors', "HTTP error")
  except requests.exceptions.SSLError:
    resultError = firebase.post('/Data/2018/November/Errors', "SSL error")
  except requests.exceptions.ReadTimeout:
        resultError = firebase.post('/Data/2018/November/Errors', "Read Timeout error")
  time.sleep(10)
  #except KeyboardInterrupt:
    #resultError = firebase.post('/Data/2018/November/Errors', "Interrupt error")
    #print ' Quit\n' 
            
else:
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in pinList: 
        GPIO.setup(i, GPIO.OUT) 
        GPIO.output(i, GPIO.HIGH)
    resultLight = firebase.post('/Data/2018/November/Light', False)
    resultWater = firebase.post('/Data/2018/November/Water', False)
    resultFans = firebase.post('/Data/2018/November/Fans', False)
    resultHeat = firebase.post('/Data/2018/November/Heat', False)
    quit()
    sys.exit()
    GPIO.cleanup()

