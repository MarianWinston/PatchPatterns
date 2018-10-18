#831162.py

from graphics import *

def makeWindow(size):
    return GraphWin("Collection of patches", size*100, size*100)

def main():
    size, myColours = getInputs()
    win = makeWindow(size)
    displayAndMovePatches(win, size, myColours)

# triangle function for penultimate patch
def triangle(win ,p1, p2, p3, colour, colourLine):
    tri = Polygon(p1, p2, p3)
    tri.setFill(colour)
    tri.setOutline(colourLine)
    tri.draw(win)
    
    return tri

# penultimate patch    
def drawPatchP(win ,x , y, colour):
    patternList = []
# assign a type so i can make decisions on the positions/colours later
    TypeP = "P" 
    for i in range(0, 100, 20):
        # making the half triangles on second and fourth rows
        if i == 20 or i == 60: 
            for j in range(0, 110, 20):
                if j == 0:
                    
                    shape = triangle(win, Point(j + x, i + y ), 
                            Point(j + x + 10, i + y), Point(j + x, i + 20 + y), 
                            colour, colour)
                    
                elif j - 10 == 90:
                    shape = triangle(win, Point(j + x - 10, i + y), 
                            Point(j + x, i + y), Point(j + x, i + 20 + y), 
                            colour, colour)
                else:
                    shape = triangle(win, Point(j + x - 10, i + y), 
                            Point(j + x + 10, i + y), Point(j + x, i + 20 + y), 
                            colour, colour)
                patternList.append(shape)
        # making first, third and fifth rows
        else: 
            for k in range(0, 100, 20):
                shape = triangle(win, Point(k + x, i + y), 
                        Point(k + x + 20, i + y), Point(k + x + 10, i + 20 + y),
                        colour, colour)
                # appending all my shapes in a list so i can use them later        
                patternList.append(shape)  
    return patternList, colour, TypeP

# line function for the final patch
def drawLine(win, p1, p2, colour):
    line = Line(p1, p2)
    line.setFill(colour)
    line.draw(win)
    return line

# final patch    
def drawPatchF(win, x, y, colour):
# assign a type so i can make decisions on the positions/colours later
    TypeF = "F"  
    patternList = []
    
    for i in range(0, 110, 10):
        line = drawLine(win, Point(x + i, y + 0), Point(x + 100 - i, y + 100), 
               colour)
        patternList.append(line)
        
    for j in range(10, 100, 10):
        line = drawLine(win, Point(100 + x, j + y), Point(0 + x, 100 - j + y), 
               colour)
# appending all my shapes in a list so i can use them later
        patternList.append(line) 
    return patternList, colour, TypeF
        
def displayAndMovePatches(win, size, myColours):
    patchworks = []
# displaying all the patches in the antepenultimate disposition
    for i in range(size):
        for j in range(size):
            colour = myColours[0]
            myColours.remove(colour)
            myColours.append(colour)
            
            if i < j:
                patchworks.append(drawPatchP(win, j*100, i*100, colour))
            else:
                patchworks.append(drawPatchF(win, j* 100, i*100, colour))
# making a while true loop to make the user swap as many patches as he wishes
    while True:
        mouse = win.getMouse()
        mouse2 = win.getMouse()
# changing the x and y coordinates of the clicks so I can use them as indexes for my lists 
        mouseCoords = Point(int(mouse.getX()/100), int(mouse.getY()/100))
        mouseCoords2 = Point(int(mouse2.getX()/100), int(mouse2.getY()/100))
        #first click index
        patternIndex = mouseCoords.getY() * size + mouseCoords.getX() 
        # second click index
        patternIndex2 = mouseCoords2.getY() * size + mouseCoords2.getX() 
        
        # extract patch, colour and type values from the list at index mouse click
        pattern, colour, Type1 = patchworks[int(patternIndex)] # first
        pattern2, colour2, Type2 = patchworks[int(patternIndex2)] # second
        
        patterns = pattern + pattern2 
        
        for shape in patterns: # undraw the patches from the click positions
            shape.undraw()
            
        
        # swapping patches from same position
        if patternIndex == patternIndex2: # if the clicks are in the same 
                                          # 100*100 square
            if Type1 == "P": # if the click is on a penultimate patch make it 
                             # final and keep the colour
                patchwork1 = drawPatchF(win, mouseCoords.getX()* 100, 
                             mouseCoords.getY()*100, colour2)
            else:  # else if the click is on a final patch make it penultimate 
                   # and keep the colour
                patchwork1 = drawPatchP(win, mouseCoords2.getX()* 100, 
                             mouseCoords2.getY()*100, colour2)
        
            # Update patternList with patchwork swap
            patchworks[int(patternIndex)] = patchwork1 # insert this patch at first index
# if the clicked patches are in different positions swap them and keep their original colour
        else: 
            if Type2 == "P":
                patchwork1 = drawPatchP(win, mouseCoords.getX()* 100, 
                             mouseCoords.getY()*100, colour2)
            else:
                patchwork1 = drawPatchF(win, mouseCoords.getX()* 100, 
                             mouseCoords.getY()*100, colour2)

            if Type1 == "P":
                patchwork2 = drawPatchP(win, mouseCoords2.getX()* 100, 
                             mouseCoords2.getY()*100, colour)
            else:
                patchwork2 = drawPatchF(win, mouseCoords2.getX()* 100, 
                             mouseCoords2.getY()*100, colour)
        
            # Update patternList with both patchwork changes
            patchworks[int(patternIndex)] = patchwork1
            patchworks[int(patternIndex2)] = patchwork2

def getInputs():
    validSizes = [5, 7, 9, 11] # make the user use these values only
    
    while True: # for as long as the user inserts invalid sizes
        size = str(input("Enter the size of the patch, the valid sizes are 5, 7, 9, 11: "))
        if not size.isnumeric(): # if the input is not a number
            print("Please enter a whole number.")
            continue #  it returns the control to the beginning of the while loop
            
# so that we don't get an error when the user enter any other type of value
        size = int(size) 
        if size not in validSizes:
            print("Non valid size.")
        else:
            size = int(size)
            break # if size is in the validSizes list terminate the loop
            
    validColours = ["red", "green", "blue", "magenta", "cyan", "orange", "brown",
                    "pink"] # make only these colours available for the patches
    myColours = []
    colourCount = 0
    
    # making the user choose 3 colours only
    while colourCount != 3:
        coloursString = ", ".join(validColours)
        colour = input("Enter the colours of the patch, valid colours are {0}: ".
                 format(coloursString))
    # remove chosen colour from the available colours and add it to the 
    # colour list i use to draw my patches
        if colour in validColours and colour not in myColours:
            myColours.append(colour)
            validColours.remove(colour)
            colourCount += 1
    
    return size, myColours
    
