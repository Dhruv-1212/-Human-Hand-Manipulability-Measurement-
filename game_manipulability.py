import pygame
import sys
import pytesseract
from PIL import Image
import Levenshtein

# Initialize Pygame
pygame.init()
drawing_color = (35, 35, 35)

# Set up display
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))



list_text_cord = []


text1 = True

def calculate_cer(hypothesis, reference):
    return Levenshtein.distance(reference, hypothesis) / len(reference)

def perform_ocr(image_path):
    # Perform OCR on the image
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng')

    # Get ground truth (you need to provide the actual text for comparison)
    reference_text = "ACTRB"

    # Calculate Character Error Rate (CER)
    cer = calculate_cer(text, reference_text)

    # Get word recognition accuracy
    reference_words = reference_text.split()
    recognized_words = text.split()
    correct_words = [w for w in recognized_words if w in reference_words]
    word_accuracy = len(correct_words) / len(reference_words)

    # Get word confidence levels
    word_confidences = pytesseract.image_to_data(Image.open(image_path), lang='eng', output_type=pytesseract.Output.DICT)['conf']

    
    return word_confidences[0]

def cordi(list_text_cord):
    # Ensure that there are points to process
    if not list_text_cord:
        return None

    # Extract x and y coordinates from the list of points
    x_values, y_values = zip(*list_text_cord)

    # Calculate the bounding box
    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)

    return [[min_x, min_y], [max_x, max_y]]



marks=[]
screen.fill((255, 255, 255))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, drawing_color, (pos[0], pos[1]), 5)

            # Add the clicked position to the appropriate list
            
            list_text_cord.append(pos)
           

        

    # Draw buttons
    button_width, button_height = 120, 40
    button_margin = 10
    button_padding = 20
    button_rect1 = pygame.Rect(width - button_width - button_margin - button_padding,
                               button_margin, button_width, button_height)
    

    pygame.draw.rect(screen, (0, 0, 0), button_rect1)
   

    # Draw text on buttons
    font = pygame.font.Font(None, 36)
    text_surface1 = font.render("evaluate", True, (255, 255, 255))


    screen.blit(text_surface1, (button_rect1.x + 10, button_rect1.y + 10))


    # Check if a button is pressed
    if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
        mouse_pos = pygame.mouse.get_pos()
        if button_rect1.collidepoint(mouse_pos):
            l = cordi(list_text_cord)  # 2 corners of the text

            x1, y1 = l[0][0], l[0][1]
            x2, y2 = l[1][0], l[1][1]

            
            screenshot_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)

            screenshot = pygame.Surface(screenshot_rect.size)
            screenshot.blit(screen, (0, 0), screenshot_rect)
            pygame.image.save(screenshot, "manipulability.png")
            screen.fill((255, 255, 255))
            marks.append(perform_ocr("manipulability.png"))
            print(marks)
            list_text_cord.clear()

    pygame.display.flip()

    # Control the frame rate    
