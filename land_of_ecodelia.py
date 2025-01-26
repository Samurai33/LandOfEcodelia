# Land of Ecodelia: Uma Aventura Psicodélica e Intrigante
# Recriação com estética e narrativa inspiradas no jogo fictício de Mr. Robot.

import pygame
import sys
import time

# Constantes de configuração
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Verde fosforescente típico de monitores antigos
FONT_TITLE_SIZE = 32
FONT_TEXT_SIZE = 16
MAIN_MENU, GAME_MENU, QUESTION, ENDING = "MAIN_MENU", "GAME_MENU", "QUESTION", "ENDING"

# Inicializa o pygame com tratamento de erros
def init_pygame():
    try:
        pygame.init()
    except pygame.error as e:
        print(f"Falha ao inicializar o pygame: {e}")
        sys.exit(1)

# Configurações de tela
def setup_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arcade of Realities")
    return screen

# Carrega fontes
def load_fonts():
    font_title = pygame.font.Font("press_start_2p.ttf", FONT_TITLE_SIZE)
    font_text = pygame.font.Font("press_start_2p.ttf", FONT_TEXT_SIZE)
    return font_title, font_text

# Função para desenhar texto com quebra de linha
def draw_text_wrapped(screen, text, x, y, font, color=GREEN, max_width=WIDTH - 100, max_height=HEIGHT - 100):
    words = text.split(' ')
    lines = []
    current_line = ""
    line_height = font.size("A")[1]
    max_lines = (max_height - y) // line_height

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
        if len(lines) >= max_lines:
            break

    lines.append(current_line)

    for i, line in enumerate(lines[:max_lines]):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * line_height))

# Função para renderizar o menu principal
def render_main_menu(screen, font_title, font_text, selected_game, games):
    screen.fill(BLACK)
    draw_text_wrapped(screen, "ARCADE OF REALITIES", WIDTH // 6, HEIGHT // 6, font_title, GREEN)
    draw_text_wrapped(screen, "Selecione um jogo usando as setas", WIDTH // 6, HEIGHT // 4, font_text, GREEN)

    for i, game in enumerate(games):
        prefix = ">" if i == selected_game else " "
        draw_text_wrapped(screen, f"{prefix} {game}", 50, 250 + i * 40, font_text, GREEN)

    pygame.display.flip()

# Função para renderizar o menu do jogo
def render_game_menu(screen, selected_game):
    if selected_game == 0:
        return QUESTION, 0, False
    else:
        screen.fill(BLACK)
        draw_text_wrapped(screen, "Este jogo ainda não está disponível.", WIDTH // 6, HEIGHT // 3, font_text, GREEN)
        pygame.display.flip()
        time.sleep(2)
        return MAIN_MENU, None, None

# Função para digitar texto com efeito de digitação
def type_text(screen, text, x, y, font, color=GREEN, delay=0.05):
    rendered_text = ""
    line_height = font.size("A")[1]
    max_width = WIDTH - x * 2
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            for char in current_line:
                rendered_text += char
                text_surface = font.render(rendered_text, True, color)
                screen.blit(text_surface, (x, y))
                pygame.display.flip()
                time.sleep(delay)
            y += line_height
            current_line = word
            rendered_text = ""

    for char in current_line:
        rendered_text += char
        text_surface = font.render(rendered_text, True, color)
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        time.sleep(delay)

# Função para renderizar a pergunta
def render_question(screen, font_text, questions, current_question, selected_choice, hidden_messages, question_displayed):
    if not question_displayed:
        screen.fill(BLACK)
        question = questions[current_question]
        type_text(screen, question["text"], 50, 100, font_text, GREEN)
        question_displayed = True
    else:
        question = questions[current_question]
        draw_text_wrapped(screen, question["text"], 50, 100, font_text, GREEN)

    for i, choice in enumerate(questions[current_question]["choices"]):
        prefix = ">" if i == selected_choice else " "
        draw_text_wrapped(screen, f"{prefix} {choice}", 50, 200 + i * 40, font_text, GREEN)

    if current_question in hidden_messages:
        draw_text_wrapped(screen, hidden_messages[current_question], 50, 400, font_text, GREEN)

    pygame.display.flip()
    return question_displayed

# Função para renderizar o final do jogo
def render_endgame(screen, font_text, endgame_text):
    y_offset = 100

    for line in endgame_text:
        type_text(screen, line, 50, y_offset, font_text, GREEN)
        y_offset += 50
        pygame.display.flip()

    options = ["Voltar ao menu principal", "Sair"]
    selected_option = 0

    while True:
        draw_text_wrapped(screen, "Escolha uma opção:", 50, y_offset + 50, font_text, GREEN)

        for i, option in enumerate(options):
            prefix = ">" if i == selected_option else " "
            draw_text_wrapped(screen, f"{prefix} {option}", 50, y_offset + 100 + i * 40, font_text, GREEN)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return MAIN_MENU
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()

# Função principal
def main():
    init_pygame()
    screen = setup_screen()
    font_title, font_text = load_fonts()

    games = [
        "Land of Ecodelia",
        "The Fractured Parallel",
        "Void Nexus",
        "Dreams of the Forgotten",
        "Echoes of the Unknown",
        "The Simulacrum"
    ]

    questions = [
        {"text": "Você já chorou durante o sexo?", "choices": ["Sim", "Não"]},
        {"text": "Você já fantasiou sobre matar seu pai?", "choices": ["Sim", "Não"]},
        {"text": "Você já teve medo de perder tudo o que ama?", "choices": ["Sim", "Não"]},
        {"text": "Se a tecnologia pudesse prever sua morte, você gostaria de saber?", "choices": ["Sim", "Não"]},
        {"text": "Você já sentiu que a humanidade está perto do fim?", "choices": ["Sim", "Não"]},
        {"text": "Você sacrificaria uma vida para salvar milhões?", "choices": ["Sim", "Não"]},
        {"text": "Você acredita que somos observados?", "choices": ["Sim", "Não"]},
        {"text": "Se pudesse apagar uma memória, você faria isso?", "choices": ["Sim", "Não"]},
        {"text": "Você acha que merece ser feliz?", "choices": ["Sim", "Não"]},
        {"text": "A chave está na sala?", "choices": ["Sim", "Não"]},
    ]

    hidden_messages = {
        3: "O símbolo de um olho aparece brevemente na tela.",
        5: "Você ouve um sussurro: \"Nós estamos observando...\"",
        8: "Um triângulo com um olho aparece no canto inferior direito."
    }

    endgame_text = [
        "Você finalmente chega ao centro de Ecodelia.",
        "Um holograma de um olho observa cada movimento seu.",
        "A voz ecoa: \"Você agora sabe as respostas ou continua perdido?\"",
        "De repente, tudo ao seu redor começa a desaparecer...",
        "E uma mensagem final surge na tela:",
        "\"Não somos nada além de nossas escolhas.\"",
        "\"A única pergunta que importa é: você estava preparado para fazer as suas?\""
    ]

    current_state = MAIN_MENU
    selected_game = 0
    current_question = 0
    selected_choice = 0
    question_displayed = False

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if current_state == MAIN_MENU:
                    if event.key == pygame.K_UP:
                        selected_game = (selected_game - 1) % len(games)
                    elif event.key == pygame.K_DOWN:
                        selected_game = (selected_game + 1) % len(games)
                    elif event.key == pygame.K_RETURN:
                        current_state, current_question, question_displayed = render_game_menu(screen, selected_game)
                elif current_state == QUESTION:
                    if event.key == pygame.K_UP:
                        selected_choice = (selected_choice - 1) % len(questions[current_question]["choices"])
                    elif event.key == pygame.K_DOWN:
                        selected_choice = (selected_choice + 1) % len(questions[current_question]["choices"])
                    elif event.key == pygame.K_RETURN:
                        if current_question < len(questions) - 1:
                            current_question += 1
                            selected_choice = 0
                            question_displayed = False
                        else:
                            current_state = ENDING

        if current_state == MAIN_MENU:
            render_main_menu(screen, font_title, font_text, selected_game, games)
        elif current_state == QUESTION:
            question_displayed = render_question(screen, font_text, questions, current_question, selected_choice, hidden_messages, question_displayed)
        elif current_state == ENDING:
            current_state = render_endgame(screen, font_text, endgame_text)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
