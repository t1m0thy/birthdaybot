import serial, numpy, math, time
#from resui.plugin import SelectPlugin

class Pololu:
        def __init__(self, name="/dev/cu.SparkFun-BT-COM0-1"):
            self.ser = serial.Serial(name, 9600)
            
        def _send(self, command):
            list = [0x80, 0x01] + command
            print list
            for c in list:
                self.ser.write(chr(c))
                
        
        def setPosition(self, servo, pos):
            self._send([4,servo, pos >> 7, pos & 127])
            
class SSC:
        def __init__(self, name="/dev/cu.SparkFun-BT-COM0-1"):
            self.ser = serial.Serial(name, 9600)

        def send(self, servo, pos):
            pos = min(127, max(-127, int(pos)))
            print servo, pos
            self.ser.write(chr(255))
            time.sleep(0.02)
            self.ser.write(chr(int(servo)))
            time.sleep(0.02)
            self.ser.write(chr(pos+128))
            time.sleep(0.02)
            

class Mechanical:
    wheelbase = 11
    wheelradius = 1.75
    mmps = 10
    ymult = 1.0
    xmult = 1.0
    curpos = [0,0]
    speed = 20
    
class Holo:
    def __init__(self, driver, mech):
        """
        driver accepts send(servo, speed)
        """
        self.driver = driver
        self.mech = mech
        self.w = numpy.zeros(3)
        self.F = numpy.zeros((3,2))
        self.F[0] = [-1.0,0.0]
        self.F[1] = [1/2.0,-math.sqrt(3)/2.0]
        self.F[2] = [1/2.0, math.sqrt(3)/2.0]
        
        
    def go(self, velocity, angle):
        angle = math.radians(angle)
        v = numpy.array(velocity)
        v *= [self.mech.xmult, self.mech.ymult]
        a = angle
        b = self.mech.wheelbase
        r = self.mech.wheelradius
        for i in range(3):
            self.w[i] = (numpy.dot(v,self.F[i]) + b*angle)/r
        for i in range(3):
            self.driver.send(i, self.w[i])
            
            
            
            
    def goto(self, pos):
        self.go(pos - curpos )
        
    
h = Holo(SSC(), Mechanical())


s = 200   
t = 1
ymult = 1.0
yoff = 0
xoff = 1.0
a = 10

time.sleep(t)

def dsquare():
    print "maxy:"
    h.go([s+xoff,s*ymult+yoff],a)
    
    time.sleep(t)
    print "stop:"
    h.go([0,0],0)
    time.sleep(t)
    
    print "maxy:"
    h.go([s+xoff,-s*ymult +yoff],a)
    time.sleep(t)
    print "stop:"
    h.go([0,0],0)
    time.sleep(t)

    print "miny:"
    h.go([-s+xoff,-s*ymult+yoff],a)
    time.sleep(t)
    print "stop:"
    h.go([0,0],0)
    time.sleep(t)
    
    print "minx:"
    h.go([-s+xoff,s*ymult+yoff],a)
    time.sleep(t)
    print "stop:"
    h.go([0,0],0)
    
for i in range(3):
        dsquare()

"""
class PathMaker(SelectPlugin):
    def action(self, boundary):
        boundary.append(boundary[0])
        last = boundary[0]
        for p in boundary:
            h.go([0,0],0)
            h.go([(p[0] - last[0]), (p[1] - last[1])],0)
            last = p
            time.sleep(0.3)
        h.go([0,0],0)
"""
            
#path = PathMaker()

#wb.addPlugin(PathMaker)
            