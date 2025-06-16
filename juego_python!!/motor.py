import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Guerra Galáctica")

# Cargar imágenes
fondo = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

imagen_jugador = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\imagen_personaje.png")
imagen_jugador = pygame.transform.scale(imagen_jugador, (50, 50))

imagen_enemigo = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\enemigo.webp")
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (35, 35))

imagen_meta = pygame.image.load(r"C:\Users\Nehuen\OneDrive\Escritorio\juego_python!!\meta.png")
imagen_meta = pygame.transform.scale(imagen_meta, (400, 100))

# Color del disparo
BLANCO = (255, 255, 255)

# Configuración del jugador
jugador = pygame.Rect(ANCHO//2 - 25, ALTO - 60, 50, 50)
velocidad_jugador = 5
vidas = 5

# Meta (objetivo donde se gana)
meta = pygame.Rect(ANCHO//2 - 50, 20, 100, 30)

# Clase Enemigo
class Enemigo:
    def __init__(self):
        self.tamaño = random.randint(20, 40)
        self.rect = pygame.Rect(random.randint(0, ANCHO - self.tamaño), random.randint(50, 300), self.tamaño, self.tamaño)
        self.salud = random.randint(2, 4)
        self.velocidad = random.randint(3, 6)

    def mover(self):
        self.rect.y += self.velocidad
        if self.rect.y > ALTO:
            self.rect.y = random.randint(50, 300)
            self.rect.x = random.randint(0, ANCHO - self.tamaño)

# Crear enemigos
enemigos = [Enemigo() for _ in range(8)]

# Proyectiles
proyectiles = []
velocidad_proyectil = -5

# Estado de teclas presionadas
teclas_presionadas = {pygame.K_w: False, pygame.K_a: False, pygame.K_d: False}

# Control del tiempo
reloj = pygame.time.Clock()
ejecutando = True
victoria = False

while ejecutando:
    pantalla.blit(fondo, (0, 0))

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key in teclas_presionadas:
                teclas_presionadas[evento.key] = True
        if evento.type == pygame.KEYUP:
            if evento.key in teclas_presionadas:
                teclas_presionadas[evento.key] = False
        if evento.type == pygame.MOUSEBUTTONDOWN:  
            if evento.button == 1:
                proyectiles.append(pygame.Rect(jugador.x + jugador.width//2 - 5, jugador.y, 10, 20))

    if not victoria:
        # Movimiento del jugador
        if teclas_presionadas[pygame.K_w] and jugador.y > 0:
            jugador.y -= velocidad_jugador
        if teclas_presionadas[pygame.K_a] and jugador.x > 0:
            jugador.x -= velocidad_jugador
        if teclas_presionadas[pygame.K_d] and jugador.x < ANCHO - jugador.width:
            jugador.x += velocidad_jugador

        # Movimiento de los proyectiles
        proyectiles = [p for p in proyectiles if p.y > 0]
        for proyectil in proyectiles:
            proyectil.y += velocidad_proyectil

        # Movimiento de enemigos
        for enemigo in enemigos:
            enemigo.mover()

        # Detección de colisión con enemigos
        proyectiles_a_eliminar = []
        enemigos_a_eliminar = []
        for enemigo in enemigos:
            if jugador.colliderect(enemigo.rect):
                vidas -= 1
                enemigos_a_eliminar.append(enemigo)
            for proyectil in proyectiles:
                if enemigo.rect.colliderect(proyectil):
                    enemigo.salud -= 1
                    proyectiles_a_eliminar.append(proyectil)
                    if enemigo.salud <= 0:
                        enemigos_a_eliminar.append(enemigo)

        enemigos = [e for e in enemigos if e not in enemigos_a_eliminar]
        proyectiles = [p for p in proyectiles if p not in proyectiles_a_eliminar]

        # Verificar si el jugador llegó a la meta
        if jugador.colliderect(meta):
            victoria = True

        # Verificar si el jugador perdió todas sus vidas
        if vidas <= 0:
            print("¡Perdiste!")
            ejecutando = False

    # Dibujar elementos
    pantalla.blit(imagen_jugador, (jugador.x, jugador.y))
    pantalla.blit(imagen_meta, (meta.x - (imagen_meta.get_width() // 2) + (meta.width // 2), meta.y))
    for enemigo in enemigos:
        pantalla.blit(imagen_enemigo, (enemigo.rect.x, enemigo.rect.y))
    for proyectil in proyectiles:
        pygame.draw.rect(pantalla, BLANCO, proyectil)

    # Dibujar texto de vidas
    fuente = pygame.font.Font(None, 36)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))

    if victoria:
        fuente_victoria = pygame.font.Font(None, 50)
        texto_victoria = fuente_victoria.render("¡Ganaste!", True, (255, 255, 0))
        pantalla.blit(texto_victoria, (ANCHO//2 - texto_victoria.get_width()//2, ALTO//2 - texto_victoria.get_height()//2))

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()