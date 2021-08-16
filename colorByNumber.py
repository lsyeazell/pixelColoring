import pygame
from PIL import Image
import time
import numpy
from k_means_image import K_Means

pygame.init()

BLACK = (0,0,0)
GREY = (190,190,190)
DARKGREY = (150,150,150)
WHITE = (255,255,255)
font1 = pygame.font.SysFont("couriernewttf",30)

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH+20,HEIGHT+130))

class button:
    def __init__(self,rect):
        self.rect = rect
    def isMouseOver(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0]>self.rect[0] and mousePos[0]<self.rect[0]+self.rect[2]:
            if mousePos[1]>self.rect[1] and mousePos[1]<self.rect[1]+self.rect[3]:
                return True
    def isClicked(self,mousePressed):
        return self.isMouseOver() and mousePressed
    def draw(self):
        pass

class controlButton(button):
    def __init__(self,rect,text):
        button.__init__(self,rect)
        self.text=text
    def draw(self):
        pygame.draw.rect(screen,GREY,self.rect,1)
        text = font1.render(self.text,True,DARKGREY)
        textX = self.rect[0]+self.rect[2]/2-(text.get_width())/2
        textY = self.rect[1]+self.rect[3]/2-(text.get_height())/2
        screen.blit(text,(textX,textY))

class zoomOutButton(button):
    def draw(self):
        pygame.draw.rect(screen,GREY,self.rect,1)
        text = font1.render("-",True,DARKGREY)
        textX = self.rect[0]+self.rect[2]/2-(text.get_width())/2
        textY = self.rect[1]+self.rect[3]/2-(text.get_height())/2
        screen.blit(text,(textX,textY))

class zoomInButton(button):
    def draw(self):
        pygame.draw.rect(screen,GREY,self.rect,1)
        text = font1.render("+",True,DARKGREY)
        textX = self.rect[0]+self.rect[2]/2-(text.get_width())/2
        textY = self.rect[1]+self.rect[3]/2-(text.get_height())/2
        screen.blit(text,(textX,textY))


class colorButton(button):
    def __init__(self,rect,color, colorNum):
        button.__init__(self,rect)
        self.color = color
        self.colorNum = colorNum
        avgColor = (self.color[0]+self.color[1]+self.color[2])/3
        self.isclicked = False
        self.x = rect[0]
        self.canBeClicked = True
        self.count = 0
        if avgColor<150:
            self.outline=WHITE
        else:
            self.outline=BLACK
    def draw(self):
        pygame.draw.rect(screen,self.color,(self.x,self.rect[1],self.rect[2],self.rect[3]))
        if self.count>0:
            text = font1.render(self.colorNum,True,self.outline)
            textX = self.x+self.rect[2]/2-(text.get_width())/2
            textY = self.rect[1]+self.rect[3]/2-(text.get_height())/2
            screen.blit(text,(textX,textY))
        if self.isclicked:
            pygame.draw.rect(screen,self.outline,(self.x,self.rect[1],self.rect[2],self.rect[3]),3)
    def isMouseOver(self):
        if self.count==0:
            return False
        mousePos = pygame.mouse.get_pos()
        if mousePos[0]>self.x and mousePos[0]<self.x+self.rect[2]:
            if mousePos[1]>self.rect[1] and mousePos[1]<self.rect[1]+self.rect[3]:
                return True

class scrollBarX(button):
    def __init__(self, rect):
        self.shiftX = 0
        self.zoom = 1
        self.rect = rect
        self.buttonWidth = self.rect[2]/self.zoom
    def draw(self):
        pygame.draw.line(screen,GREY,(self.rect[0],self.rect[1]),(self.rect[0]+self.rect[2],self.rect[1]),1)
        pygame.draw.line(screen,GREY,(self.rect[0],self.rect[1]+self.rect[3]),(self.rect[0]+self.rect[2],self.rect[1]+self.rect[3]),1)
        self.buttonWidth = self.rect[2]/self.zoom
        if self.zoom>=.9:
            pygame.draw.rect(screen, DARKGREY, (self.rect[0]+self.shiftX+1,self.rect[1]+2.5,self.buttonWidth-2,self.rect[3]-5))

class scrollBarY(button):
    def __init__(self, rect):
        self.shiftY = 0
        self.zoom = 1
        self.rect = rect
        self.buttonHeight = self.rect[3]/self.zoom
    def draw(self):
        pygame.draw.line(screen,GREY,(self.rect[0],self.rect[1]),(self.rect[0],self.rect[1]+self.rect[3]),1)
        pygame.draw.line(screen,GREY,(self.rect[0]+self.rect[2],self.rect[1]),(self.rect[0]+self.rect[2],self.rect[1]+self.rect[3]),1)
        self.buttonHeight = self.rect[3]/self.zoom
        if self.zoom>=.9:
            pygame.draw.rect(screen, DARKGREY, (self.rect[0]+2.5,self.rect[1]+self.shiftY+1,self.rect[2]-5,self.buttonHeight-2))
    

class square:
    def __init__(self,color,colorNum,loc,size):
        self.color = color
        self.colorNum = colorNum
        self.loc = loc
        self.size = size
        self.shiftX=0
        self.shiftY=0
        self.zoom = 1
        self.colored = False
        self.selected = False
        avg = (color[0]+color[1]+color[2])/3
        self.grey = (avg,avg,avg)
    def draw(self,text = None,stretch = 1):
        x = (self.loc[0]*self.size+self.shiftX)*self.zoom
        y = (self.loc[1]*self.size+self.shiftY)*self.zoom

            
        if self.colored:
            pygame.draw.rect(screen,self.color,(x,y,self.size*self.zoom*stretch ,self.size*self.zoom*stretch ))#added the +self.size*.1
        else:
            if self.selected and self.zoom>1:
                pygame.draw.rect(screen,GREY,(x,y,self.size*self.zoom*stretch ,self.size*self.zoom*stretch ))
            elif self.selected:
                pygame.draw.rect(screen,DARKGREY,(x,y,self.size*self.zoom*stretch ,self.size*self.zoom*stretch ))
            elif self.zoom<=1:
                pygame.draw.rect(screen,self.grey,(x,y,self.size*self.zoom*stretch ,self.size*self.zoom*stretch ))
            else:
                pygame.draw.rect(screen,WHITE,(x,y,self.size*self.zoom*stretch ,self.size*self.zoom*stretch ))
            
            textY = y+self.size*self.zoom/2-(text.get_height())/2
            textX = x+self.size*self.zoom/2-(text.get_width())/2
            screen.blit(text,(textX,textY))
    def isMouseOver(self, mousePos):
        
        x = (self.loc[0]*self.size+self.shiftX)*self.zoom
        y = (self.loc[1]*self.size+self.shiftY)*self.zoom
        if mousePos[0]>=x and mousePos[0]<x+self.size*self.zoom:
            if mousePos[1]>=y and mousePos[1]<y+self.size*self.zoom:
                return True
    def isClicked(self,mousePressed,mousePos):
        return self.isMouseOver(mousePos) and mousePressed
    def setZoom(self,zoom=1):
        self.zoom = zoom
    def setShiftX(self,shift=0):
        self.shiftX = shift
    def setShiftY(self,shift=0):
        self.shiftY = shift


                    


def colorMatch(color1, color2):
    tol = 20
    if abs(color1[0]-color2[0])<=tol and abs(color1[1]-color2[1])<=tol and abs(color1[1]-color2[1])<=tol:
        return True
    return False
    
def getAvg(pix, shift):
    rAvg = 0
    bAvg = 0
    gAvg = 0
    for x in range(5):
        for y in range(5):
            rAvg+= pix[x+shift[0],y+shift[1]][0]
            gAvg+= pix[x+shift[0],y+shift[1]][1]
            bAvg+= pix[x+shift[0],y+shift[1]][2]
    return (rAvg/25,gAvg/25,bAvg/25)


def imgConverter(img):
    im = Image.open(img)
    pixels  = im.load()
    x,y = im.size
    colors = {}
    colorNum = 1
    newPix = []
    squares =[]
    size = WIDTH/(x//5)
    for y1 in range(y//5):
        squares.append([])
        for x1 in range(x//5):
            avg = getAvg(pixels, (x1*5,y1*5))
            matchFound = False
            for n in colors:
                if colorMatch(colors[n],avg):
                    matchFound = True
                    squares[y1].append(square(colors[n],n,(x1,y1),size))
                    break
            if not matchFound:
                colors[str(colorNum)] = avg
                squares[y1].append(square(avg,str(colorNum),(x1,y1),size))
                colorNum+=1
    return squares, colors

def mlimgConverter(img):
    im = Image.open(img)
    pixels  = im.load()
    x,y = im.size
    siz = WIDTH/(x//5)
    pixReduced =[]
    squares = []
    for y1 in range(y//5):
        pixReduced.append([])
        squares.append([])
        for x1 in range(x//5):
            avg = getAvg(pixels, (x1*5,y1*5))
            pixReduced[y1].append(avg)
            squares[y1].append(None)
    pixFlattened = flatten(pixReduced)
    groups, centroids = K_Means(pixFlattened, x//15)
    colors = {}
    w = (len(squares[0]))
    w = (len(squares))
    for cluster in groups:
        for point in groups[cluster]:
            squares[point[0]//w][point[0]%w] = square(tuple(centroids[cluster-1]),str(cluster),(point[0]%w,point[0]//w),siz)
            
        colors[str(cluster)] = tuple(centroids[cluster-1])
            
    return squares, colors

def flatten(pixels):
    flat = []
    for j in range(len(pixels)):
        for i in range(len(pixels[j])):
            flat.append(pixels[j][i])
        
    return flat


def drawSquares(sqrs):
    for sqrRow in sqrs:
        for sqr in sqrRow:
            sqr.draw()

def colorAll(sqrs):
    for sqrRow in sqrs:
        for sqr in sqrRow:
            sqr.colored = True
            sqr.draw()
    
def main(img):
    squares,colors = mlimgConverter(img)
    mousePressed = False
    rightPressed = False
    leftPressed = False
    upPressed= False
    downPressed = False
    scrollingX = False
    scrollingY = False
    colorButtons = {}
    for num in colors:
        colorButtons[num] =colorButton((20+620*((int(num)-1)//20)+((int(num)-1)%10)*55,HEIGHT+20+(((int(num)-1)//10)%2)*55,55,55), colors[num],num)
    firstColorButton = 1
    running = True
    numSelected = "1"
    colorButtons["1"].isclicked = True
    screen.fill(WHITE)
    font = pygame.font.SysFont("couriernewttf",int(squares[0][0].size)-2)
    for sqrRow in squares:
        for sqr in sqrRow:
            #sqr.draw(font)
            colorButtons[sqr.colorNum].count+=1
    zoomIn = controlButton((590,600,30,65),"+")
    zoomOut = controlButton((590,665,30,65),"-")
    colorLeft = controlButton((0,HEIGHT+20,20,110),"<")
    colorRight = controlButton((570,HEIGHT+20,20,110),">")
    leftShown = False
    rightShown = False
    scrollX = scrollBarX((0,600,590,20))
    scrollY = scrollBarY((600,0,20,600))
    texts = {}
    for num in colorButtons:
        texts[num] = font.render(num,True,BLACK)
    screen.fill(WHITE)
    for sqrRow in squares:
        for sqr in sqrRow:
            if sqr.colorNum ==numSelected:
                sqr.selected = True
            sqr.draw(texts[sqr.colorNum])
    
    while running:
        needToDraw = False
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
                if pygame.mouse.get_pos()[1]>=620 and pygame.mouse.get_pos()[0]>=20 and pygame.mouse.get_pos()[0]<=570:
                    for colorB in colorButtons:
                        colorButtons[colorB].isclicked = colorButtons[colorB].isClicked(mousePressed)
                        if colorButtons[colorB].isclicked:
                            numSelected = colorB
                            needToDraw = True
                if zoomIn.isClicked(mousePressed):
                    needToDraw = True
                    for sqrRow in squares:
                        for sqr in sqrRow:
                            sqr.zoom+=.25
                    font = pygame.font.SysFont("couriernewttf",int(squares[0][0].size*squares[0][0].zoom-2))
                    for num in colorButtons:
                        texts[num] = font.render(num,True,BLACK)
                    scrollX.zoom+=.25
                    scrollY.zoom+=.25
                    if scrollX.zoom<=1:
                        scrollX.shiftX=0
                        scrollY.shiftY = 0
                elif zoomOut.isClicked(mousePressed):
                    if scrollX.zoom>=0.5:
                        needToDraw = True
                        for sqrRow in squares:
                            for sqr in sqrRow:
                                sqr.zoom-=.25
                        font = pygame.font.SysFont("couriernewttf",int(squares[0][0].size*squares[0][0].zoom-2))
                        for num in colorButtons:
                            texts[num] = font.render(num,True,BLACK)
                        scrollX.zoom-=.25
                        scrollY.zoom-=.25
                        scrollX.buttonWidth = scrollX.rect[2]/scrollX.zoom
                        if scrollX.shiftX>=scrollX.rect[2]-scrollX.buttonWidth:
                            scrollX.shiftX = scrollX.rect[2]-scrollX.buttonWidth
                        scrollY.buttonHeight = scrollY.rect[3]/scrollY.zoom
                        if scrollY.shiftY>=scrollY.rect[3]-scrollY.buttonHeight:
                            scrollY.shiftY = scrollY.rect[3]-scrollY.buttonHeight
                        if scrollX.zoom<=1:
                            scrollX.shiftX=0
                            scrollY.shiftY = 0
                elif colorLeft.isClicked(mousePressed) and leftShown:
                    for colorB in colorButtons:
                        colorButtons[colorB].x+=620
                    firstColorButton-=20
                elif colorRight.isClicked(mousePressed) and rightShown:
                    for colorB in colorButtons:
                        colorButtons[colorB].x-=620
                    firstColorButton+=20
                elif scrollX.isClicked(mousePressed):
                    scrollingX = True
                elif scrollY.isClicked(mousePressed):
                    scrollingY = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
                scrollingX = False
                scrollingY = False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    leftPressed = True
                elif event.key==pygame.K_RIGHT:
                    rightPressed = True
                elif event.key==pygame.K_UP:
                    upPressed = True
                elif event.key==pygame.K_DOWN:
                    downPressed = True
            elif event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    leftPressed = False
                elif event.key==pygame.K_RIGHT:
                    rightPressed = False
                elif event.key==pygame.K_UP:
                    upPressed = False
                elif event.key==pygame.K_DOWN:
                    downPressed = False
        mousePos = pygame.mouse.get_pos()
        mouseX = mousePos[0]
        mouseY = mousePos[1]
        if rightPressed:
            if scrollX.shiftX<scrollX.rect[2]-scrollX.buttonWidth:
                scrollX.shiftX +=2
            else:
                scrollX.shiftX = scrollX.rect[2]-scrollX.buttonWidth
            needToDraw = True
        if leftPressed:
            if scrollX.shiftX>0:
                scrollX.shiftX -=2
            else:
                scrollX.shiftX = 0
            needToDraw = True
        if downPressed:
            if scrollY.shiftY<scrollY.rect[3]-scrollY.buttonHeight:
                scrollY.shiftY +=2
            else:
                scrollY.shiftY = scrollY.rect[3]-scrollY.buttonHeight
            needToDraw = True
        if upPressed:
            if scrollY.shiftY>0:
                scrollY.shiftY -=2
            else:
                scrollY.shiftY = 0
            needToDraw = True
        if scrollingX:
            if mouseX-scrollX.buttonWidth/2>=scrollX.rect[2]-scrollX.buttonWidth:
                scrollX.shiftX = scrollX.rect[2]-scrollX.buttonWidth
            elif mouseX-scrollX.buttonWidth/2<=0:
                scrollX.shiftX =0
            else:
                scrollX.shiftX = mouseX-scrollX.buttonWidth/2
            needToDraw = True
        if scrollingY:
            if mouseY-scrollY.buttonHeight/2>=scrollY.rect[3]-scrollY.buttonHeight:
                scrollY.shiftY = scrollY.rect[3]-scrollY.buttonHeight
            elif mouseY-scrollY.buttonHeight/2<=0:
                scrollY.shiftY =0
            else:
                scrollY.shiftY = mouseY-scrollY.buttonHeight/2
            needToDraw = True

        if firstColorButton>1:
            leftShown = True
        else:
            leftShown = False
        if firstColorButton+19<len(colorButtons):
            rightShown = True
        else:
            rightShown = False

        
        if mouseX<600 and mouseY<600 and mouseX<600*squares[0][0].zoom and mouseY<600*squares[0][0].zoom and mousePressed:
            mouseOverX = int((mouseX/squares[0][0].zoom-squares[0][0].shiftX)//squares[0][0].size)
            mouseOverY = int((mouseY/squares[0][0].zoom-squares[0][0].shiftY)//squares[0][0].size)
            sq = squares[mouseOverY][mouseOverX]
            if not sq.colored and numSelected==sq.colorNum:
                sq.colored = True
                colorButtons[numSelected].count-=1
                sq.draw(texts[sq.colorNum])


        if needToDraw:
            screen.fill(WHITE)
            for sqrRow in squares:
                for sqr in sqrRow:
                    sqr.selected= (numSelected==sqr.colorNum)
                    if sqr.zoom>=1:
                        sqr.shiftX = -scrollX.shiftX*WIDTH/(scrollX.rect[2])
                        sqr.shiftY = -scrollY.shiftY*HEIGHT/(scrollY.rect[3])
                    else:
                        sqr.shiftX = 0
                        sqr.shiftY = 0
                    sqr.draw(texts[sqr.colorNum],1.1)
                
        pygame.draw.rect(screen,WHITE,(0,600,620,130))
        pygame.draw.rect(screen,WHITE,(600,0,20,5900))
        zoomIn.draw()
        zoomOut.draw()
        scrollX.draw()
        scrollY.draw()
        if rightShown:
            colorRight.draw()
        if leftShown:
            colorLeft.draw()
        for colorB in colorButtons:
            colorButtons[colorB].draw()

        pygame.display.update()
        
img = "catTestImage.jpg"

main(img)
pygame.quit()

    
                    
                
    
    
