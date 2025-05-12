import numpy
import time
import pygame

# this is just a print method that makes it print in colour, you can ignore that
def printList(rules, constraints):
    newList = []
    empChar = ' '
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    for item in rules:
        new = item[:]
        newList +=[new]
    temp1 = [empChar for _ in range(len(rules[0]))]
    temp2 = temp1[:]
    i = 0
    for item in top:
        if item >= 0:
            temp1[i]=str(item)
        i+=1
    i=0
    for item in bottom:
        if item >= 0:
            temp2[i]=str(item)
        i+=1
    newList = [temp1] + newList + [temp2]

    i=-1
    for e in newList:
        r = empChar
        l = empChar
        if i != -1 and i != len(rules):
            if right[i]>=0:
                r = str(right[i])
            if left[i]>=0:
                l = str(left[i])
        i+=1
        newList[i] = [l] + e + [r]

    for i in range(len(newList)):
        for j in range(len(newList[i])):
            if newList[i][j] == 'x':
                newList[i][j] = "\033[32mx\033[0m"
            elif newList[i][j] == '+':
                newList[i][j] = "\033[31m+\033[0m"
            elif newList[i][j] == '-':
                newList[i][j] = "\033[34m-\033[0m"
    for item in newList:
        print(" ".join(item))
    print()

def canPutPatternHorizontally(rules, constraints, i, j, pat):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 

    """Checks if a horizontal magnet pattern can be placed at position (i, j)"""
    if pat[0] == '+':
        if top[j] == 0 or left[i] == 0 or bottom[j+1] == 0 or right[i] == 0:
            return False
    if pat[0] == '-':
        if top[j+1] == 0 or left[i] == 0 or bottom[j] == 0 or right[i] == 0:
            return False
    if i > 0:
        # checking above neighbours
        if rules[i-1][j] == pat[0] or rules[i-1][j+1] == pat[1]:
            return False
    if i < len(rules)-1:
        # checking below neighbours
        if rules[i+1][j] == pat[0] or rules[i+1][j+1] == pat[1]:
            return False
    if j-1 >= 0 and rules[i][j-1] == pat[0]:
        return False  # Left neighbor has the same polarity
    if j+2 < len(rules[0]) and rules[i][j+2] == pat[1]:
        return False  # Right neighbor two steps away has the same polarity
    return True

def canPutPatternVertically(rules, constraints, i, j, pat):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    """Checks if a vertical magnet pattern can be placed at position (i, j)"""
    if pat[0] == '+':
        if top[j] == 0 or left[i] == 0 or bottom[j] == 0 or right[i+1] == 0:
            return False
    if pat[0] == '-':
        if top[j] == 0 or left[i+1] == 0 or bottom[j] == 0 or right[i] == 0:
            return False
    if j > 0: 
        if rules[i][j-1] == pat[0] or rules[i+1][j-1] == pat[1]:
            return False  # Left neighbor has the same polarity
    if j < len(rules[0])-1:
        if rules[i][j+1] == pat[0] or rules[i+1][j+1] == pat[1]:
            return False  # Left neighbor has the same polarity
    if i > 0 and rules[i-1][j] == pat[0]:
        return False  # Top neighbor has the same polarity
    if i+2 < len(rules)-2 and rules[i+2][j] == pat[1]:
        return False  # check bottom neighbour
    return True

def isDone(constraints):
    """Checks if the board satisfies the constraints for '+' and '-' counts"""
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    for element in left:
        if element > 0:
            return False
    for element in right:
        if element > 0:
            return False
    for element in top:
        if element > 0:
            return False
    for element in bottom:
        if element > 0:
            return False
    
    return True

def revertRequirementsHorizontally(constraints, i, j, pat):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    first = pat[0]
    if first=='+':
        top[j] +=1
        left[i] +=1
        bottom[j+1] +=1
        right[i] +=1
    elif first=='-':
        top[j+1] +=1
        left[i] +=1
        bottom[j] +=1
        right[i] +=1

def revertRequirementsVertically(constraints, i, j, pat):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    first = pat[0]
    if first=='+':
        top[j] +=1
        left[i] +=1
        bottom[j] +=1
        right[i+1] +=1
    elif first=='-':
        top[j] +=1
        left[i+1] +=1
        bottom[j] +=1
        right[i] +=1

def adjustRequirementsHorizontally(constraints, i, j, pat):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    first = pat[0]
    if first=='+':
        top[j] -=1
        left[i] -=1
        bottom[j+1] -=1
        right[i] -=1
    elif first=='-':
        top[j+1] -=1
        left[i] -=1
        bottom[j] -=1
        right[i] -=1

def adjustRequirementsVertically(constraints, i, j, pat):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    first = pat[0]
    if first=='+':
        top[j] -=1
        left[i] -=1
        bottom[j] -=1
        right[i+1] -=1
    elif first=='-':
        top[j] -=1
        left[i+1] -=1
        bottom[j] -=1
        right[i] -=1

def updateWithXs(rules):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    changes = [[0 for _ in range(len(rules[0]))] for _ in range(len(rules))]
    for i in range(len(left)):
        for j in range(len(rules[0])):
            if left[i] == 0 and right[i] == 0:
                char = rules[i][j]
                if  char in 'TBLR':
                    rules[i][j] = 'x'
                    changes[i][j] = char
                    if char == 'T':
                        rules[i+1][j] = 'x'
                        changes[i+1][j] = 'B'
                    elif char == 'B':
                        rules[i-1][j] = 'x'
                        changes[i-1][j] = 'T'
            elif left[i] == 0 or right[i] == 0:
                if rules[i][j] == 'R':
                    rules[i][j] = 'x'
                    changes[i][j] = 'R'
                elif rules[i][j] == 'L':
                    rules[i][j] = 'x'
                    changes[i][j] = 'L'
            if i<len(left)-1:
                if (left[i]==0 and left[i+1] == 0) or (right[i]==0 and right[i+1]==0):
                    if rules[i][j] == 'T':
                        rules[i][j] = 'x'
                        rules[i+1][j] = 'x'
                        changes[i][j] = 'T'
                        changes[i+1][j] = 'B'
            if top[j] == 0 and bottom[j] == 0:
                char = rules[i][j]
                if  char in 'TBLR':
                    rules[i][j] = 'x'
                    changes[i][j] = char
                    if char == 'L':
                        rules[i][j+1] = 'x'
                        changes[i][j+1] = 'R'
                    elif char == 'R':
                        rules[i][j-1] = 'x'
                        changes[i][j-1] = 'L'
            elif top[j] == 0 or bottom[j] == 0:
                if rules[i][j] == 'B':
                    rules[i][j] = 'x'
                    changes[i][j] = 'B'
                elif rules[i][j] == 'T':
                    rules[i][j] = 'x'
                    changes[i][j] = 'T'
                if j<len(top)-1:
                    if (top[j]==0 and top[j+1] == 0) or (bottom[j]==0 and bottom[j+1]==0):
                        if rules[i][j] == 'L':
                            rules[i][j] = 'x'
                            rules[i][j+1] = 'x'
                            changes[i][j] = 'L'
                            changes[i][j+1] = 'R'

    return changes

def revertUpdates(rules, changes):
    for i in range(len(changes)):
        for j in range(len(changes[0])):
            if changes[i][j] != 0:
                rules[i][j] = changes[i][j]

def fillEmptyCells(rules):
    for i in range(len(rules)):
        for j in range(len(rules[0])):
            if rules[i][j] in "TBLR":
                rules[i][j] = 'x'

def isSolvable(rules):
    right, left, top, bottom = constraints['right'], constraints['left'], constraints['top'], constraints['bottom'] 
    score = 0
    pOffset = 0
    nOffset = 0
    i = 0
    j=0
    for item in left:
        for cell in rules[i]:
            if cell in 'RL':
                score+=0.5
                if cell == 'L':
                    if (not canPutPatternHorizontally(rules, constraints, i, j, "+-")) and (not canPutPatternHorizontally(rules, constraints, i, j, "-+")):
                        pOffset+=1
                        nOffset+=1
            elif cell in 'TB':
                score+=1
                if cell == 'T':
                    if (not canPutPatternVertically(rules, constraints, i, j, "+-")):
                        pOffset+=1
                    if (not canPutPatternVertically(rules, constraints, i, j, "-+")):
                        nOffset+=1
                elif cell == 'B':
                    if (not canPutPatternVertically(rules, constraints, i-1, j, "+-")):
                        nOffset+=1
                    if (not canPutPatternVertically(rules, constraints, i-1, j, "-+")):
                        pOffset+=1
            j+=1
        score = int(round(score))
        # print(score, ', ', pOffset, ', ', nOffset)
        # print()
        if (item >= 0 and (score-pOffset) < item) or (right[i] >= 0 and (score-nOffset) < right[i]):
            return False
        score = 0
        nOffset=0
        pOffset=0
        j=0
        i+=1

    score = 0
    pOffset = 0
    nOffset = 0
    j = 0
    i=0
    for item in top:
        for row in rules:
            cell = row[j]
            if cell in 'TB':
                score+=0.5
                if cell == 'T':
                    if (not canPutPatternVertically(rules, constraints, i, j, "+-")) and (not canPutPatternVertically(rules, constraints, i, j, "-+")):
                        pOffset+=1
                        nOffset+=1
            elif cell in 'LR':
                score+=1
                if cell == 'L':
                    if (not canPutPatternHorizontally(rules, constraints, i, j, "+-")):
                        pOffset+=1
                    if (not canPutPatternHorizontally(rules, constraints, i, j, "-+")):
                        nOffset+=1
                elif cell == 'R':
                    if (not canPutPatternHorizontally(rules, constraints, i, j-1, "+-")):
                        nOffset+=1
                    if (not canPutPatternHorizontally(rules, constraints, i, j-1, "-+")):
                        pOffset+=1
            i+=1
        score = int(round(score))
        # print(score, ', ', pOffset, ', ', nOffset)
        # print()
        if (item >= 0 and (score-pOffset) < item) or (bottom[j] >= 0 and (score-nOffset) < bottom[j]):
            return False        
        score= 0
        nOffset=0
        pOffset=0
        j+=1
        i=0
    return True


def solveMagnets(rules, constraints, i, j):
    """Recursive backtracking function to solve the magnet puzzle"""
    global e, delay
    draw_board()
    pygame.display.flip()
    time.sleep(delay)
    e+=1
    #print('checking here')
    #print(isSolvable(rules))
    print(e)

    # printList(rules, constraints)
    if not isSolvable(rules):
        return None
    if isDone(constraints):
        fillEmptyCells(rules)
        return rules
    
    if j >= len(rules[0]):
        # Move to next row when reaching the end of a row
        return solveMagnets(rules, constraints, i+1, 0)
    else:
        # check what the next empty slot is
        while(rules[i][j] not in 'TLBR'):
            j+=1
            if j == len(rules[0]):
                j=0
                i+=1
            if i == len(rules):
                if isDone(constraints):
                    updateWithXs(rules)
                    return rules
                else:
                    return None
        # Try placing horizontal magnet
        if rules[i][j] == "L":
            if canPutPatternHorizontally(rules, constraints, i, j, "+-"):
                adjustRequirementsHorizontally(constraints, i, j, '+-')
                rules[i][j], rules[i][j+1] = "+", "-"
                changes = updateWithXs(rules)
                sol = solveMagnets(rules, constraints, i, j+2)
                if (sol != None):
                    return sol
                revertUpdates(rules,changes)
                revertRequirementsHorizontally(constraints, i, j, '+-')
                rules[i][j], rules[i][j+1] = "L", "R"
            if canPutPatternHorizontally(rules, constraints, i, j, "-+"):
                adjustRequirementsHorizontally(constraints, i, j, '-+')
                rules[i][j], rules[i][j+1] = "-", "+"
                changes = updateWithXs(rules)
                sol = solveMagnets(rules, constraints, i, j+2)
                if (sol != None):
                    return sol
                revertUpdates(rules,changes)
                revertRequirementsHorizontally(constraints, i, j, '-+')
                rules[i][j], rules[i][j+1] = "L", "R"
            rules[i][j], rules[i][j+1] = "x", "x"
            sol = solveMagnets(rules, constraints, i, j+2)
            if (sol):
                    return sol
            rules[i][j], rules[i][j+1] = "L", "R"
            return None

        # Try placing vertical magnet
        elif rules[i][j] == "T":
            if canPutPatternVertically(rules, constraints, i, j, "+-"):
                adjustRequirementsVertically(constraints, i, j, '+-')
                rules[i][j], rules[i+1][j] = "+", "-"
                changes = updateWithXs(rules)
                sol = solveMagnets(rules, constraints, i, j+1)
                if (sol != None):
                    return sol
                revertUpdates(rules, changes)
                revertRequirementsVertically(constraints, i, j, '+-')
                rules[i][j], rules[i+1][j] = "T", "B"
            if canPutPatternVertically(rules, constraints, i, j, "-+"):
                adjustRequirementsVertically(constraints, i, j, '-+')
                rules[i][j], rules[i+1][j] = "-", "+"
                changes = updateWithXs(rules)
                sol = solveMagnets(rules, constraints, i, j+1)
                if (sol != None):
                    return sol
                revertUpdates(rules,changes)
                revertRequirementsVertically(constraints, i, j, '-+')
                rules[i][j], rules[i+1][j] = "T", "B"
            rules[i][j], rules[i+1][j] = "x", "x"
            sol = solveMagnets(rules, constraints, i, j+1)
            if (sol):
                    return sol
            rules[i][j], rules[i+1][j] = "T", "B"
            return None
        else:
            # Move to the next cell
            return None




# Function to draw board
def draw_board():
    global GRID_COLS, GRID_ROWS, CELL_SIZE, MARGIN, EMPTY_COLOR, POS_COLOR, NEG_COLOR, NEUTRAL_COLOR
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CELL_SIZE + MARGIN) + MARGIN
            y = row * (CELL_SIZE + MARGIN) + MARGIN
            color = EMPTY_COLOR
            if rules[row][col] == '+':
                color = POS_COLOR
            elif rules[row][col] == '-':
                color = NEG_COLOR
            elif rules[row][col] == 'x':
                color = NEUTRAL_COLOR
            
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LINE_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 2)

            # Draw the letter with outline - thicker outline
            letter = rules[row][col]
            text = font.render(letter, True, (255,255,255))  # White text
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))

            outline_color = (0, 0, 0)  # Black outline
            outline_thickness = 2  # Adjust this value for thickness

            for i in range(outline_thickness):
                for dx in [-i, 0, i]:
                    for dy in [-i, 0, i]:
                        if dx != 0 or dy != 0:
                            text_outline = font.render(letter, True, outline_color)
                            text_rect_outline = text_outline.get_rect(center=(x + CELL_SIZE // 2 + dx, y + CELL_SIZE // 2 + dy))
                            screen.blit(text_outline, text_rect_outline)

            screen.blit(text, text_rect)  # Draw the main text on top

if __name__ == '__main__':
    constraints56 = {'left':[2, 3, -1, -1, -1] ,'right':[-1, -1, -1 , 1, -1],'top':[1, -1, -1, 2, 1, -1],'bottom':[2, -1, -1, 2, -1, 3]}
    constraints8_1 = { "left" : [-1, -1, 2, 2, 4, -1, 3, 2],"right":[-1, 1, -1, 3, 3, -1, -1, 4],"top":[0, 4, 3, 3, -1, 3, -1, 1],"bottom": [2, 2, 3, 3, 2, -1, 1, 3]}
    constraints8_2 = {'left':[-1, 2, 2, 2, 2, 2, 2, 0],'right':[1, 1, 1, -1, 3, 3, -1, -1], 'top':[1, 0, 2, 3, 2, -1, 2, 2], 'bottom':[0, 2, 1, 3, 2, 2, 1, -1]}
    constraints16 = {'left':[-1, -1, -1, 2, 1, 4, 1, 2, 0, 2, -1, 3, 2, -1, -1, 1],'right':[0, 0, 3, 2, 1, 2, 3, 2, 0, 1, -1, -1, 2, 1, 1, 1],'top': [1, 0, 0, 1, -1, 3, 2, 2, 1, -1, 3, 1, 2, -1, 2, -1], 'bottom':[1, -1, -1, 1, 3, 1, 3, 1, 0, 2, -1, 3, 2, 3, 2, 0]}
    constraints4 = {'left':[0, 1, 2, -1],'right':[0, -1, 1, 2],'top': [1, 1, -1, 1],'bottom':[1, 1, 0, 2]}

    rules56 = [[ "L","R","L", "R", "T", "T" ],[ "L","R","L", "R", "B", "B" ],[ "T","T","T", "T", "L", "R" ],[ "B","B","B", "B", "T", "T" ],[ "L","R","L", "R", "B", "B" ]]
    rules8_1 =[list("LRTTLRTT"),list("LRBBLRBB"),list("TTLRTTLR"),list("BBLRBBLR"),list("LRTTLRTT"),list("LRBBLRBB"),list("TTLRTTLR"),list("BBLRBBLR")]
    rules8_2 = [list('LRLRLRLR'),list('LRLRTLRT'),list('TTTTBTTB'),list('BBBBTBBT'),list('LRLRBTTB'),list('TLRTTBBT'),list('BLRBBLRB'),list('LRLRLRLR')]
    rules16 = [list("LRLRTTTTTTTTLRLR"),list("LRLRBBBBBBBBLRLR"),list("LRTTTTLRTTLRLRTT"),list("LRBBBBLRBBLRLRBB"),list("LRLRLRLRLRLRLRLR"),list("TLRTTLRTTLRTTLRT"),list("BLRBBLRBBLRBBLRB"),list("TTLRLRLRTTLRTTLR"),list("BBLRLRLRBBLRBBLR"),list("TTLRTLRTLRTTTTLR"),list("BBLRBLRBLRBBBBLR"),list("LRLRLRLRLRLRLRLR"),list("LRLRTTLRLRLRTTTT"),list("LRLRBBLRLRLRBBBB"),list("TLRTTTTTTLRTTTTT"),list("BLRBBBBBBLRBBBBB")]
    rules4 = [list('TTLR'),list('BBLR'),list('LRTT'),list('LRBB')]

    game4= (rules4, constraints4)
    game56= (rules56, constraints56)
    game8_1= (rules8_1, constraints8_1)
    game8_2= (rules8_2, constraints8_2)
    game16= (rules16, constraints16)

    rules, constraints = game56

    # Initialize pygame
    pygame.init()

    # Define constants
    
    WIDTH, HEIGHT = 800, 800
    GRID_ROWS, GRID_COLS = len(rules), len(rules[0])
    MARGIN = 5
    CELL_SIZE = min((WIDTH - (GRID_COLS + 1) * MARGIN) // GRID_COLS, (HEIGHT - (GRID_ROWS + 1) * MARGIN) // GRID_ROWS)
    BG_COLOR = (30, 30, 30)
    LINE_COLOR = (200, 200, 200)
    NEW_HEIGHT = CELL_SIZE*GRID_ROWS+MARGIN*(GRID_ROWS+2)

    # Colors for magnets
    BRIGHTNESS = 180
    POS_COLOR = (BRIGHTNESS, 0, 0)
    NEG_COLOR = (0, 0, BRIGHTNESS)
    EMPTY_COLOR = (50, 50, 50)
    NEUTRAL_COLOR = (0, BRIGHTNESS, 0)

    # Define board state
    board = numpy.full((GRID_ROWS, GRID_COLS), " ")
    
    # Font for the letters
    font = pygame.font.Font(None, int(CELL_SIZE * 0.6))  # Adjust font size as needed
    
    # Create the screen
    screen = pygame.display.set_mode((WIDTH, NEW_HEIGHT))
    pygame.display.set_caption("Polarity Game")


    start = time.time()

    e = 0
    delay = 0.1

    updateWithXs(rules)
    printList(solveMagnets(rules, constraints, 0, 0), constraints)
    draw_board()
    pygame.display.flip()
    print(e)
    end = time.time()
    print(end-start)
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()