import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 350, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Calculator")


font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
BLUE = (28, 160, 170)
HOVER_COLOR = (100, 100, 100)
CLICK_COLOR = (200, 200, 255)

try:
    click_sound = pygame.mixer.Sound("click.wav")  
except:
    click_sound = None
    print("Sound not found. Skipping click sound.")


input_text = ""
buttons = []


button_labels = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['C', '0', '=', '+']
]


for row_index, row in enumerate(button_labels):
    for col_index, label in enumerate(row):
        x = col_index * 75 + 10
        y = row_index * 75 + 100
        rect = pygame.Rect(x, y, 65, 65)
        buttons.append({'label': label, 'rect': rect, 'clicked': False})

def draw_buttons(mouse_pos):
    for button in buttons:
        rect = button['rect']
        label = button['label']
        clicked = button.get('clicked', False)

        if clicked:
            color = CLICK_COLOR
        elif rect.collidepoint(mouse_pos):
            color = HOVER_COLOR
        else:
            color = GRAY

        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = font.render(label, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def draw_display():
    pygame.draw.rect(screen, DARK_GRAY, (10, 20, WIDTH - 20, 60), border_radius=10)
    display_text = small_font.render(input_text[-25:], True, WHITE)
    screen.blit(display_text, (20, 40))

def handle_click(label):
    global input_text
    if click_sound:
        click_sound.play()

    if label == '=':
        try:
            input_text = str(eval(input_text))
        except:
            input_text = "Error"
    elif label == 'C':
        input_text = ''
    else:
        input_text += label

def handle_key(event):
    global input_text
    if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_RETURN or event.unicode == '=':
        try:
            input_text = str(eval(input_text))
        except:
            input_text = "Error"
        if click_sound:
            click_sound.play()
    elif event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]
        if click_sound:
            click_sound.play()
    elif event.unicode.lower() == 'c':
        input_text = ''
        if click_sound:
            click_sound.play()
    elif event.unicode in '0123456789+-*/.':
        input_text += event.unicode
        if click_sound:
            click_sound.play()


clock = pygame.time.Clock()
while True:
    screen.fill(BLUE)
    mouse_pos = pygame.mouse.get_pos()

    draw_display()
    draw_buttons(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button['rect'].collidepoint(event.pos):
                    button['clicked'] = True
                    handle_click(button['label'])

        elif event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button['clicked'] = False

        elif event.type == pygame.KEYDOWN:
            handle_key(event)

    pygame.display.flip()
    clock.tick(60)
