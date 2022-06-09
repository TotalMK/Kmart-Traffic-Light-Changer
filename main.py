import utime
from machine import Pin, Timer
from time import sleep_ms, sleep

#IR Sensor
ird = Pin(13,Pin.IN)       #IR Receiver Signal Pin
irdpower = Pin(14, Pin.OUT, Pin.PULL_UP) #Setting Pin 14 to Provide Power to IR Sensor
irdpower.value(1) #Telling Pin 14 to turn on

#Traffic Light Switch Pin
trafficswitch = Pin(16, Pin.OUT, Pin.PULL_UP) #Setting Output Pin to Switch
trafficswitch.value(1) #Pico Output Pin to Switch To Stay High (same as switch)

# Remote Button Array
# [¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯]
# [[ON]      [OFF]] ON / OFF
# [[MUP][SUP][BUP]] MODE UP / SPEED UP / BRIGHT UP
# [[MDW][SDW][BDW]] MODE DOWN / SPEED DOWN / BRIGHT DOWN
# [[R]   [G]   [B]] RED / GREEN / BLUE
# [[Y]   [C]   [P]] YELLOW / CYAN / PURPLE
# [     [RGB]     ] RGB
# [[AUT][PSE][RST]] AUTO / PAUSE / RESET
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

act = {
"B-ON": "LLLLLLLLHHHHHHHHHLHLLLHLLHLHHHLH",
"B-OFF": "LLLLLLLLHHHHHHHHHHHLLLHLLLLHHHLH",
"B-MODEUP": "LLLLLLLLHHHHHHHHLLHLLLHLHHLHHHLH",
"B-MODEDOWN": "LLLLLLLLHHHHHHHHHHHLLLLLLLLHHHHH",
"B-SPEEDUP": "LLLLLLLLHHHHHHHHLLLLLLHLHHHHHHLH",
"B-SPEEDDOWN": "LLLLLLLLHHHHHHHHHLHLHLLLLHLHLHHH",
"B-BRIGHTUP": "LLLLLLLLHHHHHHHHHHLLLLHLLLHHHHLH",
"B-BRIGHTDOWN": "LLLLLLLLHHHHHHHHHLLHLLLLLHHLHHHH",
"B-RED": "LLLLLLLLHHHHHHHHLHHLHLLLHLLHLHHH",
"B-GREEN": "LLLLLLLLHHHHHHHHHLLHHLLLLHHLLHHH",
"B-BLUE": "LLLLLLLLHHHHHHHHHLHHLLLLLHLLHHHH",
"B-YELLOW": "LLLLLLLLHHHHHHHHLLHHLLLLHHLLHHHH",
"B-CYAN": "LLLLLLLLHHHHHHHHLLLHHLLLHHHLLHHH",
"B-PURPLE": "LLLLLLLLHHHHHHHHLHHHHLHLHLLLLHLH",
"B-RGB": "LLLLLLLLHHHHHHHHLLHHHLLLHHLLLHHH",
"B-AUTO": "LLLLLLLLHHHHHHHHLHLLLLHLHLHHHHLH",
"B-PAUSE": "LLLLLLLLHHHHHHHHLHLLHLHLHLHHLHLH",
"B-RESET": "LLLLLLLLHHHHHHHHLHLHLLHLHLHLHHLH",
}

def read_ircode(ird):
    wait = 1
    complete = 0
    seq0 = []
    seq1 = []

    while wait == 1:
        if ird.value() == 0:
            wait = 0
    while wait == 0 and complete == 0:
        start = utime.ticks_us()
        while ird.value() == 0:
            ms1 = utime.ticks_us()
        diff = utime.ticks_diff(ms1,start)
        seq0.append(diff)
        while ird.value() == 1 and complete == 0:
            ms2 = utime.ticks_us()
            diff = utime.ticks_diff(ms2,ms1)
            if diff > 10000:
                complete = 1
        seq1.append(diff)

    code = ""
    for val in seq1:
        if val < 2000:
            if val < 700:
                code += "L"
            else:
                code += "H"
    # print(code)
    command = ""
    for k,v in act.items():
        if code == v:
            command = k
    if command == "":
        command = code
    return command


while True:
    command = read_ircode(ird)
#    print(command)
    utime.sleep(0.5)
    
    #RGB Button
    if command == "B-RGB":
        print('RGB PUSHED')
        print('Pressing Traffic Light Button')
        trafficswitch.value(0) #Switch Is Pulled Low
        sleep(1)
        trafficswitch.value(1) #Switch Is Reset To High
    
    #Reset Button            
    if command == "B-RESET":
        print('RESET PUSHED')
        machine.reset()