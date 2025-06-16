import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga - Meta con Imagen")

# Cargar la imagen de fondo
background = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\fondo.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cargar la imagen del personaje
player_image = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\imagen_personaje.png")
player_image = pygame.transform.scale(player_image, (50, 50))

# Cargar la imagen de los enemigos
enemy_image = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\enemigo.webp")
enemy_image = pygame.transform.scale(enemy_image, (35, 35))

# Cargar la imagen de la meta
goal_image = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\meta.png")
goal_image = pygame.transform.scale(goal_image, (400, 100))  # Ajuste de tamaño

# Definir colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Jugador
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, 50, 50)
player_speed = 5
lives = 5  # Vidas del jugador

# Meta (objetivo donde se gana)
goal = pygame.Rect(WIDTH//2 - 50, 20, 100, 30)

# Clase Enemigo
class Enemy:
    def __init__(self):
        self.size = random.randint(20, 40)
        self.rect = pygame.Rect(random.randint(0, WIDTH - self.size), random.randint(50, 300), self.size, self.size)
        self.health = random.randint(2, 4)
        self.speed = random.randint(3, 6)

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(50, 300)
            self.rect.x = random.randint(0, WIDTH - self.size)

# Crear enemigos
enemies = [Enemy() for _ in range(8)]

# Proyectiles
bullets = []
bullet_speed = -5

# Estado de teclas presionadas
keys_pressed = {pygame.K_w: False, pygame.K_a: False, pygame.K_d: False}

clock = pygame.time.Clock()
running = True
victory = False  # Nueva variable para controlar el estado de victoria

while running:
    screen.blit(background, (0, 0))  # Dibujar el fondo personalizado

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in keys_pressed:
                keys_pressed[event.key] = True
        if event.type == pygame.KEYUP:
            if event.key in keys_pressed:
                keys_pressed[event.key] = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Disparo con clic izquierdo
            if event.button == 1:
                bullets.append(pygame.Rect(player.x + player.width//2 - 5, player.y, 10, 20))

    if not victory:  # Solo mover elementos si no has ganado
        # Movimiento del jugador
        if keys_pressed[pygame.K_w] and player.y > 0:
            player.y -= player_speed
        if keys_pressed[pygame.K_a] and player.x > 0:
            player.x -= player_speed
        if keys_pressed[pygame.K_d] and player.x < WIDTH - player.width:
            player.x += player_speed

        # Movimiento de los proyectiles
        bullets = [bullet for bullet in bullets if bullet.y > 0]
        for bullet in bullets:
            bullet.y += bullet_speed

        # Movimiento de enemigos
        for enemy in enemies:
            enemy.move()

        # Detección de colisión con enemigos
        bullets_to_remove = []
        enemies_to_remove = []
        for enemy in enemies:
            if player.colliderect(enemy.rect):
                lives -= 1
                enemies_to_remove.append(enemy)
            for bullet in bullets:
                if enemy.rect.colliderect(bullet):
                    enemy.health -= 1
                    bullets_to_remove.append(bullet)
                    if enemy.health <= 0:
                        enemies_to_remove.append(enemy)

        enemies = [enemy for enemy in enemies if enemy not in enemies_to_remove]
        bullets = [bullet for bullet in bullets if bullet not in bullets_to_remove]

        # Verificar si el jugador llegó a la meta
        if player.colliderect(goal):
            victory = True

        # Verificar si el jugador perdió todas sus vidas
        if lives <= 0:
            print("¡Perdiste!")
            running = False

    # Dibujar elementos
    screen.blit(player_image, (player.x, player.y))  # Imagen del jugador
    screen.blit(goal_image, (goal.x - (goal_image.get_width() // 2) + (goal.width // 2), goal.y))  # Meta centrada
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.rect.x, enemy.rect.y))  # Imagen de enemigos
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Dibujar texto de vidas
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Vidas: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

    if victory:
        font_victory = pygame.font.Font(None, 50)
        victory_text = font_victory.render("¡Ganaste!", True, (255, 255, 0))
        screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - victory_text.get_height()//2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()