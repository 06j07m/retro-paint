#ICS3U Paint Project
#Mona Liu
#Due April 25, 2022

'''
Extra features:
- Undo & redo
- Clear canvas (fill canvas with background colour or backdrop)
- Separate foreground/background colour (click to select to change)
- Spray paint
- Rectangular brush
- Bucket (fill with colour or backdrop)
- Colour dropper
- Polygon shape (click for points and press space to draw)
- Stamps scrolling
- Backdrops scrolling
- Music start/stop
- Music next/previous
- Mute and sound slider
- Show which tool is selected and hint
- Show position of mouse on canvas
'''

#imports and initializing
from pygame import *

from tkinter import *
from tkinter import filedialog

from random import *

from math import *

font.init()
mixer.init()

root = Tk()


#set pygame screen
width,height = 1200,760
screen = display.set_mode((width,height))


#fixed colours
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKGREY = (73, 71, 77)
LIGHTGREY = (134, 131, 138)
LIGHTPURPLE = (192, 180, 195)
DARKPURPLE = (25, 12, 40)
HIGHLIGHT = (225, 216, 227)
SHADOW = (117, 106, 119)


#import font
textFont = font.Font("paintResources/VCR_OSD_MONO_1.001.ttf",15)
subtextFont = font.Font("paintResources/VCR_OSD_MONO_1.001.ttf",10)


#load and draw background
background = image.load("paintResources/background.jpg")
screen.blit(background,(0,0))

#load and draw palette
palette = Rect(40,520,155,170)
palette_img = image.load("paintResources/palette.jpg")
screen.blit(palette_img,(palette.x,palette.y))


#draw canvas
canvas = Rect(235,40,690,650)
draw.rect(screen,WHITE,canvas)


#size slider area and border
size = Rect(60,350,130,40)
draw.rect(screen,HIGHLIGHT,(58,348,134,44),2)

#foreground and background selectors
bg = Rect(80,465,45,45)
fg = Rect(50,445,45,45)

#unfill button
fill_false = image.load("paintResources/fill_false.jpg")


#music play icon
pause_true = image.load("paintResources/play.jpg")

#sound mute icon
sound_off = image.load("paintResources/sound_mute.jpg")

#sound slider area
sound = Rect(1120,660,50,10)


#list of main buttons
#(save, load, undo, redo, clear, prev stamp, next stamp, prev backdrop,
# next backdrop, pause, prev song, next song, sound, fill)
mainButtons = [Rect(40,197,50,50),
               Rect(40,247,50,50),
               Rect(90,197,50,50),
               Rect(90,247,50,50),
               Rect(140,197,50,50),
               Rect(1000,280,20,20),
               Rect(1120,280,20,20),
               Rect(1000,390,20,20),
               Rect(1120,390,20,20),
               Rect(1020,650,25,25),
               Rect(985,650,25,25),
               Rect(1055,650,25,25),
               Rect(1090,650,25,25),
               Rect(140,450,45,45)]

#list of main button icon files
mainFiles = ["paintResources/save.jpg",
             "paintResources/load.jpg",
             "paintResources/undo.jpg",
             "paintResources/redo.jpg",
             "paintResources/clear.jpg",
             "paintResources/up.jpg",
             "paintResources/down.jpg",
             "paintResources/up.jpg",
             "paintResources/down.jpg",
             "paintResources/pause.jpg",
             "paintResources/prev.jpg",
             "paintResources/next.jpg",
             "paintResources/sound.jpg",
             "paintResources/fill_true.jpg"]

#list of main button icons
mainIcons = []

#load each icon and add it to list
for file in mainFiles:
    icon = image.load(file)
    mainIcons.append(icon)


#list of tool buttons
toolButtons = [Rect(970,45,50,50),
               Rect(1020,45,50,50),
               Rect(1070,45,50,50),
               Rect(1120,45,50,50),
               Rect(970,95,50,50),
               Rect(1020,95,50,50),
               Rect(1070,95,50,50),
               Rect(1120,95,50,50),
               Rect(970,145,50,50),
               Rect(1020,145,50,50),
               Rect(1070,145,50,50)]

#list of tools
tools = ["pencil","eraser","brush","calligraphy","spray","bucket","dropper","rectangle","circle","line","polygon"]

#list of tool "hints"
toolHints = ["PENCIL: CLICK AND DRAG TO DRAW",
             "ERASER: CLICK AND DRAG TO ERASE",
             "ROUND BRUSH: CLICK AND DRAG TO DRAW",
             "SQUARE BRUSH: CLICK AND DRAG TO DRAW (CALLIGRAPHY EFFECT)",
             "SPRAY PAINT: CLICK AND DRAG TO DRAW (SPRAY PAINT EFFECT)",
             "BUCKET: CLICK TO FILL CANVAS - FILLS WITH PICTURE IF BACKDROP IS SELECTED",
             "DROPPER: CLICK ON CANVAS TO PICK COLOUR",
             "RECTANGLE: CLICK AND DRAG - RELEASE TO DRAW",
             "CIRCLE: CLICK AND DRAG - RELEASE TO DRAW",
             "LINE: CLICK AND DRAG - RELEASE TO DRAW",
             "POLYGON: CLICK FOR POINTS (NEEDS 3+) - PRESS SPACE TO DRAW"]

#list of tool icon files
toolFiles = ["paintResources/pencil.jpg",
            "paintResources/eraser.jpg",
            "paintResources/brush.jpg",
            "paintResources/calligraphy.jpg",
            "paintResources/spray.jpg",
            "paintResources/bucket.jpg",
            "paintResources/dropper.jpg",
            "paintResources/rectangle.jpg",
            "paintResources/circle.jpg",
            "paintResources/line.jpg",
            "paintResources/polygon.jpg"]

#list of tool icons
toolIcons = []

#load each tool icon and add it to list
for file in toolFiles:
    icon = image.load(file)
    toolIcons.append(icon)


#area for stamp and background preview
stamp = Rect(1030,250,80,80)
backdrop = Rect(1030,360,80,80)
    

#list of stamp files
stampFiles = ["paintResources/stamp1.png",
             "paintResources/stamp2.png",
             "paintResources/stamp3.png",
             "paintResources/stamp4.png",
             "paintResources/stamp5.png",
             "paintResources/stamp6.png"]

#list of stamps
stamps = []

#load each stamp file and add it to list of stamps
for file in stampFiles:
    st = image.load(file)
    stamps.append(st)


#list of backdrop files
backdropFiles = ["paintResources/backdrop1.jpg",
                "paintResources/backdrop2.jpg",
                "paintResources/backdrop3.jpg",
                "paintResources/backdrop4.jpg",
                "paintResources/backdrop5.jpg",
                "paintResources/backdrop6.jpg"]

#list of backdrops
backdrops = []

#load each backdrop file and add it to list
for file in backdropFiles:
    bd = image.load(file)
    backdrops.append(bd)


#list of song files
songFiles = ["paintResources/sideeffects.ogg",
             "paintResources/godsmenu.ogg",
             "paintResources/thunderous.ogg",
             "paintResources/wolfgang.ogg",
             "paintResources/maniac.ogg"]

#list of song names and artists
songNames = ["SIDE EFFECTS (8 BIT)",
             "GOD'S MENU (8 BIT)",
             "THUNDEROUS (8 BIT)",
             "WOLFGANG (8 BIT)",
             "MANIAC (8 BIT)"]

songArtists = ["ELZISH TWO (orig. by STRAY KIDS)",
               "ELZISH TWO (orig. by STRAY KIDS)",
               "ELZISH TWO (orig. by STRAY KIDS)",
               "8-BIT ARCADE (orig. by STRAY KIDS)",
               "ELZISH TWO (orig. by STRAY KIDS)"]

#list of album art files
songImgFiles = ["paintResources/cle2.jpg",
                "paintResources/golive.jpg",
                "paintResources/noeasy.jpg",
                "paintResources/noeasy.jpg",
                "paintResources/oddinary.jpg"]

#list of album art images
songImgs = []

#load each album art image and add it to list
for file in songImgFiles:
    songImg = image.load(file)
    songImgs.append(songImg)


#"hint" for tools (starts as no tool)
hint = textFont.render("SELECT A TOOL TO START",False,DARKPURPLE)

#size of tools (starts at 10)
sizeHint = textFont.render("10",False,DARKPURPLE)


running = True


#selected tool
tool = ""

#drawing (foreground) and erasing (background) colour
toolFg = BLACK  
toolBg = WHITE

#tool size
toolR = 10

#shape border size
shapeR = 0

#boolean for selecting fore/backround colours
fgSelected = True

#polygon coordinates
coord = []

#make "screenshot" and lists of "screenshot"s for undo and redo
undoList = []
redoList = []
screenCap = screen.subsurface(canvas).copy()
undoList.append(screenCap)

#position of stamp, backdrop, and music lists
stampPos = 0
backdropPos = 0
musicPos = 0

#backdrop preview surface
previewRect = Rect(80,80,80,80)
previewPic = backdrops[backdropPos].subsurface(previewRect).copy()

#boolean for selecting backdrop
bdSelected = False

#volume
vol = 1


#load and play first song
mixer.music.load(songFiles[musicPos])
mixer.music.play()

#get song name and artist
songName = textFont.render(songNames[musicPos],False,DARKPURPLE)
songArtist = subtextFont.render(songArtists[musicPos],False,DARKPURPLE)


while running:

    #variables for left mouse button press/release and space key (for polygon)
    clickLeft = False
    unclickLeft = False
    spaceKey = False
    
    for evt in event.get():

        if evt.type == QUIT:
            #close tkinter and paint program
            root.destroy()
            running = False
            
        if evt.type == KEYDOWN:
            if evt.key == K_SPACE:
                #press space to finish polygon
                spaceKey = True
                
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                #get when mouse is clicked (to use in loops)
                clickLeft = True
                #get location of original click
                sx,sy = evt.pos
                
        if evt.type == MOUSEBUTTONUP:
            if evt.button == 1:
                #get when mouse is released (to use in loops)
                unclickLeft = True

                
    #get mouse position and press
    curx,cury = mouse.get_pos()
    pressLeft = mouse.get_pressed()[0]


    #draw all buttons
    for i in range(len(mainButtons)):
        screen.blit(mainIcons[i],(mainButtons[i]))
    for i in range(len(toolButtons)):
        screen.blit(toolIcons[i],(toolButtons[i]))

    
    #outline when mouse hover on main buttons, stamp, or backdrop
    for btn in mainButtons + [stamp,backdrop]:
        if btn.collidepoint(curx,cury):
            draw.rect(screen,LIGHTGREY,btn,2)
            

    #draw rects to show fore/back ground colours
    #show whichever is selected in front of the other
    if fgSelected:
        draw.rect(screen,toolBg,bg)
        draw.rect(screen,toolFg,fg)
    else:
        draw.rect(screen,toolFg,fg)
        draw.rect(screen,toolBg,bg)

    #select fore/back ground colour when user clicks on it (to change it)
    if fg.collidepoint(curx,cury) and clickLeft:
        fgSelected = True
    if bg.collidepoint(curx,cury) and clickLeft:
        fgSelected = False


    #get colour from palette or canvas (only if eyedropper tool is selected)
    if (palette.collidepoint(curx,cury) or (tool == "dropper" and canvas.collidepoint(curx,cury))) and pressLeft:
        #change fore/back ground colour depending on which is selected
        #and draw new rectangle showing current colour
        if fgSelected:
            toolFg = screen.get_at((curx,cury))
            draw.rect(screen,toolFg,fg)
        else:
            toolBg = screen.get_at((curx,cury))
            draw.rect(screen,toolBg,bg)


    #change button to show whether shapes are filled or not (0 means filled)
    if shapeR == 0:
        screen.blit(mainIcons[13],mainButtons[13])
    else:
        screen.blit(fill_false,mainButtons[13])

    #toggle fill/unfill for shapes
    if mainButtons[13].collidepoint(curx,cury):
        if clickLeft:
            if shapeR == 0:
                #if shape is filled, change it to unfilled (border size same as tool size)
                shapeR = toolR
            else:
                #if shape is not filled, change it to filled
                shapeR = 0


    #draw slider for brush size
    draw.rect(screen,LIGHTPURPLE,(size))
    #x, y, and height are the same as the slider
    #width is proportional to brush size (width / slider width = size / 50)
    draw.rect(screen,DARKPURPLE,(size.x,size.y,toolR / 50 * size.w, size.h))

    #show brush size in numbers beside slider
    draw.rect(screen,LIGHTPURPLE,(size.x - 25,size.y + 10,20,20))
    screen.blit(sizeHint,(size.x - 25,size.y + 10))

    #change size
    if size.collidepoint(curx,cury) and pressLeft:
        #use mouse position to determine size of tool (left = 1, right = 50)
        toolR = int((curx - size.x) / size.w * 51)
        #change size of shape border to match (if unfill is selected)
        if shapeR != 0:
            shapeR = toolR
        #update number next to slider
        sizeHint = textFont.render(str(toolR),False,DARKPURPLE)


    #change button to show whether music is playing
    if mixer.music.get_busy():
        screen.blit(mainIcons[9],mainButtons[9])
    else:
        screen.blit(pause_true,mainButtons[9])

    #start/stop music (needs pygame 2.0.1 and above)
    if mainButtons[9].collidepoint(curx,cury) and clickLeft:
        if mixer.music.get_busy():
            #if pause button is clicked and it's playing, pause it
            mixer.music.pause()
        else:
            #if it's not playing, unpause it
            mixer.music.unpause()


    #change button to show whether music is muted
    if mixer.music.get_volume() == 0:
        screen.blit(sound_off,mainButtons[12])
    else:
        screen.blit(mainIcons[12],mainButtons[12])

    #mute/unmute music
    if mainButtons[12].collidepoint(curx,cury) and clickLeft:
        if mixer.music.get_volume() == 0:
            #if mute button is clicked and volume is 0 (it's muted), unmute it
            #by setting the volume to what it was before
            mixer.music.set_volume(vol)
        else:
            #if volume isn't 0 (it's not muted), mute it by setting volume to 0
            mixer.music.set_volume(0)


    #show song name
    draw.rect(screen,LIGHTPURPLE,(960,610,210,30))
    screen.blit(songName,(965,615))
    screen.blit(songArtist,(965,630))

    #show album art
    screen.blit(songImgs[musicPos],(1010,505))

    #change music (similar to stamps/backdrops)
    if (mainButtons[10].collidepoint(curx,cury) or mainButtons[11].collidepoint(curx,cury)) and clickLeft:
        if mainButtons[10].collidepoint(curx,cury):
            musicPos = (musicPos + 1) % len(songFiles)
        else:
            musicPos = (musicPos - 1 + len(songFiles)) % len(songFiles)
        #unload current song and load new one
        mixer.music.unload()
        mixer.music.load(songFiles[musicPos])
        #start new song
        mixer.music.play()
        #set song name and artist
        songName = textFont.render(songNames[musicPos],False,DARKPURPLE)
        songArtist = subtextFont.render(songArtists[musicPos],False,DARKPURPLE)
        

    #show sound slider
    draw.rect(screen,HIGHLIGHT,sound)
    draw.rect(screen,DARKPURPLE,(sound.x,sound.y,vol * sound.w,sound.h))

    #change volume
    if sound.collidepoint(curx,cury) and pressLeft:
        #use mouse position to determine volume (left = 0.1, right = 1)
        vol = (curx - sound.x) / sound.w
        #set the volume
        mixer.music.set_volume(vol)


    #show tool "hint" at bottom of screen
    draw.rect(screen,LIGHTPURPLE,(35,715,1140,30))
    screen.blit(hint,(40,722))

    #if mouse is on canvas, show mouse x and y position
    if canvas.collidepoint(curx,cury):
        mousePos = textFont.render(str((curx - canvas.x,cury - canvas.y)),False,DARKPURPLE)
        screen.blit(mousePos,(1070,722))
        

    #save
    if mainButtons[0].collidepoint(curx,cury):
        if clickLeft:
            #show save dialog using tkinter and get file name to save
            fileName = filedialog.asksaveasfilename(defaultextension = ".png")
            if fileName:
                #if user enters a name/path, save the current canvas
                image.save(screen.subsurface(canvas),fileName)

            
    #load
    if mainButtons[1].collidepoint(curx,cury):
        if clickLeft:
            #show open dialog and get path of image to load
            fileName = filedialog.askopenfilename(filetypes = [("Image",(".png",".jpg",".jpeg"))])
            if fileName:
                #if user selects a file, load it and get height and width
                fileImg = image.load(fileName)
                fileH = fileImg.get_height()
                fileW = fileImg.get_width()
                if fileH > canvas.h or fileW > canvas.w:
                    #if loaded file is wider or taller than canvas, resize it
                    if fileH >= fileW:
                        #if file is portrait, resize height to fit canvas
                        #use aspect ratio to resize width
                        fileImg = transform.scale(fileImg,(canvas.h * fileW / fileH,canvas.h))
                    elif fileW > fileH:
                        #if file is landscape, resize width to fit canvas
                        #use aspect ratio to resize height
                        fileImg = transform.scale(fileImg,(canvas.w,canvas.h * fileH / fileW))
                #show loaded image on canvas
                screen.blit(fileImg,canvas)


    #undo
    if mainButtons[2].collidepoint(curx,cury):
        if clickLeft and len(undoList) > 1:
            #if undo has more than 1 "screenshot", remove the last one and add it to redo list
            redoList.append(undoList.pop())
            #show the last "screenshot" in the undo list
            screen.blit(undoList[-1],canvas)
            

    #redo
    if mainButtons[3].collidepoint(curx,cury):
        if clickLeft and len(redoList) > 0:
            #if redo has at 1 or more "screenshot"s, remove the last one and add it to undo list
            undoList.append(redoList.pop())
            #show the last "screenshot" in the undo list
            screen.blit(undoList[-1],canvas)

                    
    #clear
    if mainButtons[4].collidepoint(curx,cury):
        if clickLeft:
            if bdSelected:
                #if backdrop is selected, draw it on canvas
                screen.blit(backdrops[backdropPos],canvas)
            else:
                #if backdrop isn't selected, fill canvas with foreground colour
                screen.subsurface(canvas).fill(toolBg)
        if unclickLeft:
            #take "screenshot" after clearing
            screenCap = screen.subsurface(canvas).copy()
            #add it to undo list
            undoList.append(screenCap)
            redoList = []


    #select/deselect tools
    for ind in range(len(toolButtons)):
        if tools[ind] == tool:
            #if tool is selected, draw outline around icon and change hint to match selected tool
            draw.rect(screen,DARKGREY,toolButtons[ind],2)
            hint = textFont.render(toolHints[ind],False,DARKPURPLE)
        if toolButtons[ind].collidepoint(curx,cury):
            #outline when mouse hovers on button
            draw.rect(screen,LIGHTGREY,toolButtons[ind],2)
            if clickLeft:
                #if user click on button
                if tools[ind] == tool:
                    #if tool is selected, deselect it and change hint back to no tool
                    tool = ""
                    hint = textFont.render("Select a tool to start",False,DARKPURPLE)
                else:
                    #if tool isn't selected, select it
                    tool = tools[ind]


    #show stamp preview (with white background)
    draw.rect(screen,HIGHLIGHT,stamp)
    screen.blit(stamps[stampPos],stamp)

    #if stamp is selected, draw outline around icon and show hint
    if tool in stamps:
        draw.rect(screen,DARKGREY,stamp,2)
        hint = textFont.render("STAMP: CLICK ON SCREEN - UP/DOWN BUTTON FOR MORE",False,DARKPURPLE)

    #select/deselect stamps
    if stamp.collidepoint(curx,cury):
        if clickLeft:
            if tool in stamps:
                tool = ""
            else:
                tool = stamps[stampPos]

    #if "previous" or "next" button is clicked, scroll through and update stamps
    if (mainButtons[5].collidepoint(curx,cury) or mainButtons[6].collidepoint(curx,cury)) and clickLeft:
        if mainButtons[5].collidepoint(curx,cury):
            #if "previous" is clicked, move position in list backward
            stampPos = (stampPos + 1) % len(stamps)
        else:
            #if "next" is clicked, move position in list forward (add length of list to keep it above 0)
            stampPos = (stampPos - 1 + len(stamps)) % len(stamps)
        #if a stamp is selected, update the stamp
        if tool in stamps:
            tool = stamps[stampPos]


    #show backdrop preview
    screen.blit(previewPic,backdrop)

    #if backdrop is selected, draw outline around icon
    if bdSelected:
        draw.rect(screen,DARKGREY,backdrop,2)

    #select/deselect backdrop
    if backdrop.collidepoint(curx,cury):
        if clickLeft:
            if not bdSelected:
                bdSelected = True
            else:
                bdSelected = False

    #scroll through and update backdrops (similar to stamps)
    if (mainButtons[7].collidepoint(curx,cury) or mainButtons[8].collidepoint(curx,cury)) and clickLeft:
        if mainButtons[7].collidepoint(curx,cury):
            backdropPos = (backdropPos + 1) % len(backdrops)
        else:
            backdropPos = (backdropPos - 1 + len(backdrops)) % len(backdrops)
        #update preview picture
        previewPic = backdrops[backdropPos].subsurface(previewRect).copy()


    #use tools on canvas
    if canvas.collidepoint(curx,cury):
        
        #only draw on canvas
        screen.set_clip(canvas)


        if tool == "pencil":
            if pressLeft:
                #hold down mouse to draw 1 px line
                draw.line(screen,toolFg,(oldcurx,oldcury),(curx,cury))

        elif tool == "brush":
            if pressLeft:
                #hold down mouse to draw circles
                draw.circle(screen,toolFg,(curx,cury),toolR)
                #calculate distance between current and previous mouse position
                dx = curx - oldcurx
                dy = cury - oldcury
                dt = sqrt((dx ** 2) + (dy ** 2))
                #connect distance by drawing circles at intervals
                for d in range(1,int(dt),int(toolR / 4)):
                    dotX = d * dx / dt + oldcurx
                    dotY = d * dy / dt + oldcury
                    draw.circle(screen,toolFg,(int(dotX),int(dotY)),toolR)

        elif tool == "eraser":
            if pressLeft:
                if bdSelected:
                    #if backdrop is selected, erase by drawing backdrop at mouse position
                    eraserPic = backdrops[backdropPos].subsurface((curx - canvas.x,cury - canvas.y,toolR * 2,toolR * 2))
                    screen.blit(eraserPic,(curx,cury))
                else:
                    #if backdrop isn't selected, draw circles like for brush but with background colour
                    draw.circle(screen,toolBg,(curx,cury),toolR)
                    dx = curx - oldcurx
                    dy = cury - oldcury
                    dt = sqrt((dx ** 2) + (dy ** 2))
                    for d in range(1,int(dt),int(toolR / 4)):
                        dotX = d * dx / dt + oldcurx
                        dotY = d * dy / dt + oldcury
                        draw.circle(screen,toolBg,(int(dotX),int(dotY)),toolR)
        
        elif tool == "calligraphy":
            if pressLeft:
                #same as brush but drawing a rectangle
                draw.rect(screen,toolFg,(curx,cury,toolR*2,toolR))
                dx = curx - oldcurx
                dy = cury - oldcury
                dt = sqrt((dx ** 2) + (dy ** 2))
                for d in range(1,int(dt),int(toolR / 4)):
                    dotX = d * dx / dt + oldcurx
                    dotY = d * dy / dt + oldcury
                    draw.rect(screen,toolFg,(dotX,dotY,toolR*2,toolR))

        elif tool == "spray":
            if pressLeft:
                #hold down mouse to draw random dots within size of spray brush
                for i in range(toolR):
                    #random x and y location within tool size
                    randX = randint(-toolR,toolR)
                    randY = randint(-toolR,toolR)
                    #if the x and y are within the brush circle, draw a 1px dot
                    if (randX ** 2 + randY ** 2) <= toolR ** 2:
                       draw.circle(screen,toolFg,(curx + randX,cury + randY),1)

        elif tool == "bucket":
            if clickLeft:
                if bdSelected:
                    #if backdrop is selected, fill canvas with current backdrop
                    screen.blit(backdrops[backdropPos],canvas)
                else:
                    #if backdrop is not selected, fill canvas with foreground colour
                    screen.subsurface(canvas).fill(toolFg)

        elif tool in stamps:
            #get centre x and y of stamp
            mx = tool.get_width() // 2
            my = tool.get_height() // 2
            #draw over previous canvas
            screen.blit(undoList[-1],canvas)
            #preview of the stamp
            screen.blit(tool,(curx - mx,cury - my))
            if unclickLeft:
                #draw over previous canvas
                screen.blit(undoList[-1],canvas)
                #draw stamp at mouse position
                screen.blit(tool,(curx - mx,cury - my))

        elif tool == "line":
            #draw over previous canvas
            screen.blit(undoList[-1],canvas)
            if pressLeft:
                #preview of the line
                draw.line(screen,toolFg,(sx,sy),(curx,cury),toolR)
            if unclickLeft:
                #draw over previous canvas
                screen.blit(undoList[-1],canvas)
                #draw line from click location to mouse position
                draw.line(screen,toolFg,(sx,sy),(curx,cury),toolR)
                
        elif tool == "rectangle":
            #draw over previous canvas
            screen.blit(undoList[-1],canvas)
            if pressLeft:
                #make temporary rectangle from click location to mouse position
                rectTemp = Rect(sx,sy,curx - sx,cury - sy)
                #normalize rectangle so negative width/height doesn't cause error
                rectTemp.normalize()
                #preview of the rectangle
                draw.rect(screen,toolFg,(rectTemp),shapeR)
            if unclickLeft:
                #draw over previous canvas
                screen.blit(undoList[-1],canvas)
                #draw rectangle
                draw.rect(screen,toolFg,(rectTemp),shapeR)
                

        elif tool == "circle":
            #same as rectangle but drawing and ellipse instead
            screen.blit(undoList[-1],canvas)
            if pressLeft:
                rectTemp = Rect(sx,sy,curx - sx,cury - sy)
                rectTemp.normalize()
                draw.ellipse(screen,toolFg,(rectTemp),shapeR)
            if unclickLeft:
                screen.blit(undoList[-1],canvas)
                draw.ellipse(screen,toolFg,(rectTemp),shapeR)
    
        elif tool == "polygon":
            if clickLeft:
                #get mouse click positions and add them to list of coordinates
                coord.append((curx,cury))
            if spaceKey and len(coord) >= 3:
                #if space bar is pressed and there are at least 3 coordinates,
                #draw the polygon and clear list
                draw.polygon(screen,toolFg,(coord),shapeR)
                coord = []
                

        if (tool != "" and tool != "polygon" and unclickLeft) or spaceKey:
            #take "screenshot" after drawing anything
            #(drawing using any tool that's not polygon and drawing polygon)
            screenCap = screen.subsurface(canvas).copy()
            #add it to undo list and clear redo list
            undoList.append(screenCap)
            redoList = []


        #can draw on other parts of the screen
        screen.set_clip(None)
        
    else:
        #if mouse leaves canvas, draw over screen (to get rid of stamp preview)
        if tool in stamps:
            screen.blit(undoList[-1],canvas)

    #save previous mouse position
    oldcurx,oldcury = curx,cury
    
    display.flip()
            
quit()

