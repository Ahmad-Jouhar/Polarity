import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 800
GRID_ROWS, GRID_COLS = 5, 6
MARGIN = 5
CELL_SIZE = min((WIDTH - (GRID_COLS + 1) * MARGIN) // GRID_COLS, (HEIGHT - (GRID_ROWS + 1) * MARGIN) // GRID_ROWS)
BG_COLOR = (30, 30, 30)
LINE_COLOR = (200, 200, 200)
NEW_HEIGHT = CELL_SIZE*GRID_ROWS+MARGIN*(GRID_ROWS+2)

# Colors for magnets
POS_COLOR = (255, 0, 0)
NEG_COLOR = (0, 0, 255)
EMPTY_COLOR = (50, 50, 50)
NEUTRAL_COLOR = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, NEW_HEIGHT))
pygame.display.set_caption("Polarity Game")

# Define board state
board = np.full((GRID_ROWS, GRID_COLS), " ")

# Rules for the board
rules = [[ "L","R","L", "R", "T", "T" ],
         [ "L","R","L", "R", "B", "B" ],
         [ "T","T","T", "T", "L", "R" ],
         [ "B","B","B", "B", "T", "T" ],
         [ "L","R","L", "R", "B", "B" ]]

# Font for the letters
font = pygame.font.Font(None, int(CELL_SIZE * 0.6))  # Adjust font size as needed

# Function to draw board
def draw_board():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CELL_SIZE + MARGIN) + MARGIN
            y = row * (CELL_SIZE + MARGIN) + MARGIN
            color = EMPTY_COLOR
            if board[row, col] == '+':
                color = POS_COLOR
            elif board[row, col] == '-':
                color = NEG_COLOR
            elif board[row, col] == 'N':
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


# Game loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - MARGIN) // (CELL_SIZE + MARGIN)
            row = (y - MARGIN) // (CELL_SIZE + MARGIN)
            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                if board[row, col] == ' ':
                    if rules[row][col] == 'T' and row + 1 < GRID_ROWS:
                        board[row, col] = '+'
                        board[row + 1, col] = '-'
                    elif rules[row][col] == 'B' and row - 1 >= 0:
                        board[row, col] = '-'
                        board[row - 1, col] = '+'
                    elif rules[row][col] == 'L' and col + 1 < GRID_COLS:
                        board[row, col] = '+'
                        board[row, col + 1] = '-'
                    elif rules[row][col] == 'R' and col - 1 >= 0:
                        board[row, col] = '-'
                        board[row, col - 1] = '+'
                elif board[row, col] == '+':
                    board[row, col] = '-'
                    if rules[row][col] == 'T' and row + 1 < GRID_ROWS:
                        board[row + 1, col] = '+'
                    elif rules[row][col] == 'B' and row - 1 >= 0:
                        board[row - 1, col] = '+'
                    elif rules[row][col] == 'L' and col + 1 < GRID_COLS:
                        board[row, col + 1] = '+'
                    elif rules[row][col] == 'R' and col - 1 >= 0:
                        board[row, col - 1] = '+'
                elif board[row, col] == '-':
                    board[row, col] = 'N'
                    if rules[row][col] == 'T' and row + 1 < GRID_ROWS:
                        board[row + 1, col] = 'N'
                    elif rules[row][col] == 'B' and row - 1 >= 0:
                        board[row - 1, col] = 'N'
                    elif rules[row][col] == 'L' and col + 1 < GRID_COLS:
                        board[row, col + 1] = 'N'
                    elif rules[row][col] == 'R' and col - 1 >= 0:
                        board[row, col - 1] = 'N'
                elif board[row, col] == 'N':
                    board[row, col] = ' '
                    if rules[row][col] == 'T' and row + 1 < GRID_ROWS:
                        board[row + 1, col] = ' '
                    elif rules[row][col] == 'B' and row - 1 >= 0:
                        board[row - 1, col] = ' '
                    elif rules[row][col] == 'L' and col + 1 < GRID_COLS:
                        board[row, col + 1] = ' '
                    elif rules[row][col] == 'R' and col - 1 >= 0:
                        board[row, col - 1] = ' '

    draw_board()
    pygame.display.flip()

pygame.quit()