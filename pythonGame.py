from random import randint
import pygame
import pygame.mixer

pygame.mixer.init()
pygame.init()

# Adcionando música de fundo
pygame.mixer.music.load('WhatsApp Audio 2025-01-25 at 16.38.19.mpeg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


# Adcionando aúdio para o tiro
shot_sound = pygame.mixer.Sound('WhatsApp Audio 2025-01-25 at 16.39.32.mpeg')

# Configuração da tela
screen = pygame.display.set_mode([960, 540])
pygame.display.set_caption('Jogo de Python')

# Imagens usadas
img_background = pygame.image.load('space bg game.png')
nav_player = pygame.image.load('ship_A.png')
nav_enemy = pygame.image.load('enemy_A.png')
nav_Enemy = pygame.image.load('satellite_A.png')
missil = pygame.image.load('tiro.png')
missil = pygame.transform.scale(missil, (30, 30))

# Fonte para textos
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Cores dos botões
CYAN = (0, 255, 255)
CYAN_HOVER = (0, 200, 200)
RED = (255, 0, 0)
RED_HOVER = (200, 0, 0)
GREEN = (0, 255, 0)
GREEN_HOVER = (0, 200, 0)

# Posição do jogador
y_player, x_player, vel_player = 400, 420, 2

# Posição dos inimigos
y_enemy, x_enemy, vel_enemy = 50, 500, 2
y_Enemy, x_Enemy, vel_Enemy = 50, 300, 2

# Configuração do míssil
vel_missil = 10
x_missil, y_missil = x_player, y_player
shot_target = False

# Variáveis do jogo
vidas = 3
score = 0
game_over = False
start_screen = True
sound_on = True

# Função para reiniciar o jogo
def reset_game():
    global x_player, y_player, vidas, score, x_enemy, y_enemy, x_Enemy, y_Enemy, shot_target, x_missil, y_missil, game_over
    x_player, y_player = 420, 400
    vidas = 3
    score = 0
    x_enemy, y_enemy = randint(1, 700), -50
    x_Enemy, y_Enemy = randint(1, 700), -50
    shot_target = False
    x_missil, y_missil = x_player, y_player
    game_over = False

# Funções para os botões
def start_game():
    global start_screen
    start_screen = False

def quit_game():
    global loop
    loop = False

def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        pygame.mixer.music.unpause()
        print("Som ativado")
    else:
        pygame.mixer.music.pause()
        print("Som desativado")

# Inicializa o jogo
reset_game()

# Função para desenhar botões
def draw_button(surface, text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        if click[0] == 1 and action:  # Clique esquerdo
            action()
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

# Loop principal
loop = True
while loop:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False

    if start_screen:
        # Tela de início
        screen.blit(img_background, (0, 0))
        title_text = game_over_font.render('Bem-vindo ao Jogo Python!', True, (255, 255, 255))
        screen.blit(title_text, (150, 100))

        # Botões na tela de início
        draw_button(screen, 'Começar', 370, 250, 220, 60, CYAN, CYAN_HOVER, start_game)
        draw_button(screen, 'Sair', 370, 330, 220, 60, RED, RED_HOVER, quit_game)
        draw_button(screen, f'Som: {"ON" if sound_on else "OFF"}', 370, 410, 220, 60, GREEN, GREEN_HOVER, toggle_sound)

    elif not game_over:
        keyboard = pygame.key.get_pressed()
        # Movimento do jogador
        if keyboard[pygame.K_UP]:
            y_player -= vel_player
        if keyboard[pygame.K_DOWN]:
            y_player += vel_player
        if keyboard[pygame.K_LEFT]:
            x_player -= vel_player
        if keyboard[pygame.K_RIGHT]:
            x_player += vel_player

        # Limites do jogador
        x_player = max(-13, min(x_player, 911))
        y_player = max(-17, min(y_player, 493))

        # Disparo do míssil
        if keyboard[pygame.K_SPACE] and not shot_target:
            shot_target = True
            x_missil = x_player + 20  # Centraliza o míssil na nave
            y_missil = y_player
            if sound_on:
                shot_sound.play()

        if shot_target:
            y_missil -= vel_missil  # Move o míssil para cima
            if y_missil < 0:  # Verifica se o míssil saiu da tela
                shot_target = False

        # Atualiza retângulos
        player_rect = nav_player.get_rect(topleft=(x_player, y_player))
        enemy_rect = nav_enemy.get_rect(topleft=(x_enemy, y_enemy))
        Enemy_rect = nav_Enemy.get_rect(topleft=(x_Enemy, y_Enemy))
        missil_rect = missil.get_rect(topleft=(x_missil, y_missil))

        # Movimento dos inimigos
        y_enemy += vel_enemy
        y_Enemy += vel_Enemy

        if y_enemy > 530:
            y_enemy = -50
            x_enemy = randint(1, 700)

        if y_Enemy > 530:
            y_Enemy = -50
            x_Enemy = randint(1, 700)

        # Verifica colisão do jogador com os inimigos
        if player_rect.colliderect(enemy_rect) or player_rect.colliderect(Enemy_rect):
            vidas -= 1
            print(f"Vidas restantes: {vidas}")
            if vidas <= 0:
                game_over = True
            else:
                # Reposiciona jogador e inimigos
                x_player, y_player = 420, 400
                x_enemy, y_enemy = randint(1, 700), -50
                x_Enemy, y_Enemy = randint(1, 700), -50

        # Verifica colisão do míssil com os inimigos
        if missil_rect.colliderect(enemy_rect):
            score += 1
            print(f"Score: {score}")
            y_enemy = -50
            x_enemy = randint(1, 700)
            shot_target = False  # Reseta o míssil

        if missil_rect.colliderect(Enemy_rect):
            score += 1
            print(f"Score: {score}")
            y_Enemy = -50
            x_Enemy = randint(1, 700)
            shot_target = False  # Reseta o míssil

        # Desenho na tela
        screen.blit(img_background, (0, 0))
        screen.blit(nav_player, (x_player, y_player))
        screen.blit(nav_enemy, (x_enemy, y_enemy))
        screen.blit(nav_Enemy, (x_Enemy, y_Enemy))
        if shot_target:
            screen.blit(missil, (x_missil, y_missil))

        # Exibe vidas e pontuação
        vidas_text = font.render(f'Vidas: {vidas}', True, (255, 255, 255))
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(vidas_text, (10, 10))
        screen.blit(score_text, (10, 50))

    else:
        # Tela de Game Over
        game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
        final_score_text = font.render(f'Score final: {score}', True, (255, 255, 255))
        restart_text = font.render('Pressione R para reiniciar', True, (255, 255, 255))
        screen.blit(game_over_text, (320, 200))
        screen.blit(final_score_text, (380, 300))
        screen.blit(restart_text, (330, 400))

         # Verifica se o jogador pressionou "R" para reiniciar
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_r]:
            reset_game()

    pygame.display.update()



