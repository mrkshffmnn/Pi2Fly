from OpenGL.GL import glVertex2f, glColor3f, glBegin, glEnd, GL_QUADS, GL_TRIANGLES, glTexCoord2f, glBindTexture, GL_TEXTURE_2D, glEnable, glDisable, GL_BLEND, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glColor4f
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from time import sleep, perf_counter, time
from math import tan, radians
import pygame

window_width = 800
window_height = 480

pygame.font.init()
font1 = pygame.font.Font (None, 40)
font3 = pygame.font.Font (None, 25)
font4 = pygame.font.Font (None, 45)
    
class Data:
    roll = 0
    pitch = 0
    airspeed = 160
    heading = 0
    
    altitude = 4500
    
    altitude_last = 0
    altitude_now = 0
    altitude_delta = 0
    altitude_delta_table = 30 * [0]
    time_last = 0
    time_now = 0
    
    c1 = True
    c2 = True
    c3 = 0
    
class FPS:   
    c = 0
    fps = 0

def fps():

    FPS.c += 1
    try: FPS.last_clock = FPS.this_clock
    except:FPS.last_clock = perf_counter()
    FPS.this_clock = perf_counter()
    if round(FPS.this_clock) > round(FPS.last_clock):
        #print(FPS.fps)
        FPS.fps = FPS.c
        FPS.c = 0

    color = (255,198,0, 255)
    drawText(5, 9, str(FPS.fps), color, font1)
    drawTexture(70, 10, fpstexture, 1, 198/255, 0, 1)


def get_data():
    #dummy data for artifical horizon
    
    #pitch
    if Data.pitch < 20 and Data.c1: Data.pitch += 0.01
    if Data.pitch >= 20 and Data.c1: Data.c1 = False
    if Data.pitch < 21 and not Data.c1: Data.pitch = Data.pitch - 0.01
    if Data.pitch < -20: Data.c1 = True

    #roll
    if Data.roll < 20 and Data.c2: Data.roll += 0.005
    if Data.roll >= 20 and Data.c2: Data.c2 = False
    if Data.roll < 21 and not Data.c2: Data.roll = Data.roll - 0.005
    if Data.roll < -20: Data.c2 = True
    
    #airspeed
    if Data.pitch > 0: Data.airspeed = Data.airspeed - 0.002 * Data.pitch
    elif Data.pitch < 0: Data.airspeed = Data.airspeed + 0.002 * abs(Data.pitch)
    
    #altitude
    if Data.pitch > 0: Data.altitude = Data.altitude + 0.005 * Data.pitch
    elif Data.pitch < 0: Data.altitude = Data.altitude - 0.005 * abs(Data.pitch)
    
    #altitude_delta
    Data.time_now = perf_counter()
    if Data.time_now >= Data.time_last + 0.01:
        if Data.c3 == 30: Data.c3 = 0
        Data.time_last = Data.time_now        
        Data.altitude_last = Data.altitude_now
        Data.altitude_now = Data.altitude        
        Data.altitude_delta_table[Data.c3] = Data.altitude_now - Data.altitude_last
        Data.c3 +=1 
    Data.altitude_delta = (sum(Data.altitude_delta_table)/len(Data.altitude_delta_table))
    
    if Data.heading < 360 and Data.c1: Data.heading += 0.05
    if Data.heading >= 360 and Data.c1: Data.heading = 0
       
def frame():
       
    drawTexture(0, 0, frametexture, 1, 1, 1, 1)

def horizon():

    pivot_x = (900 + (-100)) / 2
    pivot_y = (-1200+ 1680) / 2
    glPushMatrix()
    
    # rotate around pivot (roll)
    glTranslatef(pivot_x, pivot_y, 0)
    glRotatef(-Data.roll, 0, 0, 1)
    glTranslatef(-pivot_x, -pivot_y, 0)

    # apply pitch
    glTranslatef(0, (-Data.pitch*8), 0)
    
    glBindTexture(GL_TEXTURE_2D, horizontexture[0])

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glColor4f(1, 1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(-100, -1200)
    glTexCoord2f(1, 1); glVertex2f(900, -1200)
    glTexCoord2f(1, 0); glVertex2f(900, 1680)
    glTexCoord2f(0, 0); glVertex2f(-100, 1680)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
     
    color = (255,  255, 255, 0)
    drawText(110, 10, str("roll: "+str(round(Data.roll))), color, font3)
    drawText(620, 10, str("pitch: "+str(round(Data.pitch))), color, font3)

def rollindicator():

    '''indicator markins are 10, 20, 30, 45, 60 degree'''
    glPushMatrix()
    
    # rotate around pivot (roll)
    glTranslatef(400, 240, 0)
    glRotatef(-Data.roll, 0, 0, 1)
    glTranslatef(-400, -240, 0)
    
    glBindTexture(GL_TEXTURE_2D, rollindtexture[0])

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glColor4f(1, 1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(266, 240)
    glTexCoord2f(1, 1); glVertex2f(266+rollindtexture[1], 240)
    glTexCoord2f(1, 0); glVertex2f(266+rollindtexture[1], 240+rollindtexture[2])
    glTexCoord2f(0, 0); glVertex2f(266, 240+rollindtexture[2])
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    
    #roll indicator stationary triangle 
    drawTexture(392, 365, rollindtritexture, 1, 1, 1, 1)    

def compass():
    
    glPushMatrix()
    
    # rotate around pivot (roll)
    glTranslatef(400, 0, 0)
    glRotatef(Data.heading, 0, 0, 1)
    glTranslatef(-400, -0, 0)
    
    glBindTexture(GL_TEXTURE_2D, compasstexture[0])

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glColor4f(1, 1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(305, -95)
    glTexCoord2f(1, 1); glVertex2f(305+compasstexture[1], -95)
    glTexCoord2f(1, 0); glVertex2f(305+compasstexture[1], -95+compasstexture[2])
    glTexCoord2f(0, 0); glVertex2f(305, -95+compasstexture[2])
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    
    drawTexture(393, 94, compassindtexture, 1, 1, 1, 1)
    
    
def crosshair():
    #crosshair
    #indicator triangle shadow
    glColor3f(187/255, 107/255, 1/255)
    glBegin(GL_QUADS)
    glVertex2f(400, 230)
    glVertex2f(365, 215)
    glVertex2f(400, 227)
    glVertex2f(435, 215)
    glEnd()
    # indicator triangle
    glColor3f(255/255, 198/255, 0/255)
    glBegin(GL_QUADS)
    glVertex2f(400, 240)
    glVertex2f(365, 215)
    glVertex2f(400, 230)
    glVertex2f(435, 215)
    glEnd()
    #yellow indicator line
    glColor3f(255/255, 198/255, 0/255)
    glBegin(GL_QUADS)
    glVertex2f(320, 241)
    glVertex2f(320, 239)
    glVertex2f(350, 239)
    glVertex2f(350, 241)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(450, 241)
    glVertex2f(450, 239)
    glVertex2f(480, 239)
    glVertex2f(480, 241)
    glEnd()
    
def speedometer():
    
    ypos = 63 + round(Data.airspeed) * 1.35    
    glColor3f(0/255, 241/255, 250/255)
    glBegin(GL_QUADS)
    glVertex2f(40, ypos)
    glVertex2f(40+59, ypos)
    glVertex2f(40+59, ypos+3)
    glVertex2f(40, ypos+3)
    glEnd()
    
    color = (0,  241, 250, 255)
    drawText(5, 435, str(round(Data.airspeed)), color, font4)
    
    #knots 
    drawTexture(60, 440, knotstexture, 0, 241/255, 250/255, 1)
    
def altimeter():
    
    color = (0,  241, 250, 255)
    drawText(705, 435, str(round(Data.altitude)), color, font4)
    
    # m unit
    drawTexture(784, 440, mtexture, 0, 241/255, 250/255, 1)

def variometer():
    color = (0,  241, 250, 255)
    drawText(710, 10, str(round((abs(Data.altitude_delta*10)), 1)), color, font4)
    
    # m/s unit
    drawTexture(769, 10, mstexture, 0, 241/255, 250/255, 1)
    
    if Data.altitude_delta*10 > 0:
        glBegin(GL_TRIANGLES)
        glVertex2f(768, 30)
        glVertex2f(794, 30)
        glVertex2f(781, 44)
        glEnd()
        
    if Data.altitude_delta*10 < 0:
        glBegin(GL_TRIANGLES)
        glVertex2f(768, 44)
        glVertex2f(794, 44)
        glVertex2f(781, 30)
        glEnd()
            
def drawText(xpos, ypos, textString, color, font):

    textSurface = font.render(textString, True, color, (0,0,0,1))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos2d(xpos,ypos)
    #glDrawPixels is the slowest
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def drawTexture(xpos, ypos, texturename, r, g, b, a):
    
    glBindTexture(GL_TEXTURE_2D, texturename[0])

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glColor4f(r, g, b, a)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(xpos, ypos)
    glTexCoord2f(1, 1); glVertex2f(xpos+texturename[1], ypos)
    glTexCoord2f(1, 0); glVertex2f(xpos+texturename[1], ypos+texturename[2])
    glTexCoord2f(0, 0); glVertex2f(xpos, ypos+texturename[2])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def loadtexture(filename):
    
    image = pygame.image.load(filename)
    datas = pygame.image.tostring(image, 'RGBA')
    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, datas)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    return [texID, image.get_width(), image.get_height()]
       
def draw():
    
    horizon()
    rollindicator()
    compass()
    frame()
    speedometer()
    altimeter()
    variometer()
    crosshair()
    
    
def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    #glutFullScreen()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  
    iterate()
    
    try:get_data()
    except Exception as e:print("get_data:\t", e)
    try:draw()
    except Exception as e:print("draw:\t", e)
    try:fps()
    except Exception as e:print("fps:\t", e)
    
    glutSwapBuffers()
    
if __name__ == "__main__":
    
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow(b"Pi2Fly")
    
    frametexture = loadtexture(r"resources/frame.png")
    horizontexture = loadtexture(r"resources/horizon.png")
    rollindtexture = loadtexture(r"resources/rollind.png")
    rollindtritexture = loadtexture(r"resources/rollindtri.png")
    knotstexture = loadtexture(r"resources/kn.png")
    fpstexture = loadtexture(r"resources/fps.png")
    mtexture = loadtexture(r"resources/m.png")
    mstexture = loadtexture(r"resources/ms.png")
    varioindtexture = loadtexture(r"resources/varioind.png")
    compasstexture = loadtexture(r"resources/compass.png")
    compassindtexture = loadtexture(r"resources/compassind.png")
    
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutMainLoop()