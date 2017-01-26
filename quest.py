doserial=False
cave=[]
import csv
with open('cavedata3.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        rowstr = ""
        try:

            for i in range(180):
                if (i < int(row[2])):
                    rowstr += "T"
                if (i > int(row[1])):
                    rowstr +="B"
                if not((i < int(row[2])) or (i > int(row[1]))):
                    rowstr+=" "

            print(rowstr)
            #print (', '.join(row))
            cave.append((row[0],row[1],row[2],row[3],row[4]))
        except:
            pass
    print(len(cave))

# START THREAD FOR COM PORT
import threading
import serial

connected = False
reading=""
temp=25
toohot=False
port = 'COM6'
baud = 9600


if doserial==True:
    serial_port = serial.Serial(port, baud, timeout=10)
    print(serial_port.is_open)

def handle_data(data):
    print(data)

def read_from_port(ser):
    global connected,reading,toohot,temp
    while not connected:
        #serin = ser.read()
        connected = True

        while True:
           reading = ser.readline().decode().strip()
           if (reading in ["32","31","30","29","28","27","26","25","24"]):
               temp=int(reading)
           handle_data(reading)
if doserial==True:
    thread = threading.Thread(target=read_from_port, args=(serial_port,))
    thread.start()




import sys, pygame
pygame.init()
import time
size = width, height = 750,1000
sf=5 #vertical scale factor
speed = [1, 1]
black = 0, 0, 0
red = 255, 0, 0
orange = 255, 127, 0
green = 128, 255, 128
blue = 0,0,255
white=200,200,200
yellow=255,255,0


screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
caveb = pygame.image.load("cave.bmp")
rocket=pygame.image.load("rocket.png")
satellite=[]
for i in range(1,39):
    if i>=10:
        satellite.append(pygame.image.load("c:\\tmp\\00%s.png" %i))
    else:
        satellite.append(pygame.image.load("c:\\tmp\\000%s.png"%i))
ballrect = ball.get_rect()
ii=0
while 1:
    ii=ii+0.1
    if ii>len(cave):
        ii=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()



    if temp in [25,26,27,]:
        screen.fill(green)
    if temp in [28,29]:
        screen.fill(orange)
    if temp in [30,31,32]:
        screen.fill(red)
    if not temp in[25,26,27,28,29,30,31,32]:
        screen.fill(black)


    n=0
    oo=ii
    row= cave[int(oo)]
    bspp = [(n - oo % 1) * ballrect.width, sf * int(row[4])]
    tspp = [(n - oo % 1) * ballrect.width, sf * int(row[2])]
    ballrect = ballrect.move(speed)
    for row in cave[int(oo):int(oo+(size[0]+50)/ballrect.width)]:
        #Set speed based on temperature
        targets=temp-23
        if targets<=0:
            targets=0
        if speed[0]>=0:
            speed[0]=targets
        else:
            speed[0]=-targets
        if speed[1]>=0:
            speed[1]=targets
        else:
            speed[1]=-targets

        #bottom
        caverect=ball.get_rect()
        bsp=[(n-oo%1)*ballrect.width,sf*int(row[4])]
        #blit horizontal rect
        screen.fill(white, rect=pygame.Rect(bsp[0],bsp[1],ballrect.width,size[1]-bsp[1]))
        screen.fill(black, rect=pygame.Rect(bsp[0], bsp[1], ballrect.width, 4))

        #blit vertical rect
        if bsp[1]>bspp[1]:
            screen.fill(black,rect=pygame.Rect(bsp[0],bspp[1],4,bsp[1]-bspp[1]))
        if bsp[1]<bspp[1]:
            screen.fill(black,rect=pygame.Rect(bsp[0],bsp[1],4,bspp[1]-bsp[1]+4))
        bspp=bsp
        #if ball is in this part of the cave check if we are hitting the top or bottom
        if ballrect.left>bsp[0] and ballrect.left<(bsp[0]+ballrect.width):
            if ballrect.bottom > bsp[1]:  # or ballrect.top < tsp[1]:
                speed[1] = -abs(speed[1])
        #draw a rocket if there is one
        if int(row[3]) == 2:
            rrect = pygame.Rect(bsp[0], bsp[1] - 124,32, 128)
            screen.blit(rocket, rrect)

        # draw a satellite tower if there is one
        if int(row[3])==1:
            #screen.fill(blue, rect=pygame.Rect(bsp[0], bsp[1]-32, ballrect.width, 32))
            srect=pygame.Rect(bsp[0], bsp[1]-58, 64, 64)
            screen.blit(satellite[int(ii+int(row[0])) % 38], srect)
        #top
        tsp=[(n-oo%1)*ballrect.width,sf*int(row[2])]
        #blit horizontal rect
        screen.fill(white, rect=pygame.Rect(tsp[0],0,ballrect.width,tsp[1]))
        screen.fill(black, rect=pygame.Rect(tsp[0],tsp[1],ballrect.width,4))

        #blit vertical rect
        if tsp[1]>tspp[1]:
            screen.fill(black,rect=pygame.Rect(tsp[0],tspp[1],4,tsp[1]-tspp[1]))
        if tsp[1]<tspp[1]:
            screen.fill(black,rect=pygame.Rect(tsp[0],tsp[1],4,tspp[1]-tsp[1]+4))
        tspp=tsp
        #if ball is in this part of the cave check if we are hitting the top or bottom
        if ballrect.left>bsp[0] and ballrect.left<(bsp[0]+ballrect.width):
            if ballrect.top < tsp[1]:  # or ballrect.top < tsp[1]:
                speed[1] = abs(speed[1])
        
        n=n+1


    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]


    screen.blit(ball, ballrect)
    pygame.display.flip()

    #if toohot==True:
    #    ballrect = ball.get_rect()
    time.sleep(0.0015*(1+abs(5-targets)))




