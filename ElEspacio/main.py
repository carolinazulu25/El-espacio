import pygame
import random

# Inicializar PyGame y el mezclador de sonido
pygame.init()
pygame.mixer.init()

# Configurar la ventana
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El increible espacio")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 150, 255)
ROJO = (255, 0, 0)

# Cargar música y efectos
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.play(-1)  # Repetir infinitamente

# Reloj
reloj = pygame.time.Clock()

# Clases
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        imagen_original = pygame.image.load("Aastronauta.png").convert_alpha()
        self.image = pygame.transform.scale(imagen_original, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad = 7

    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        imagen_original = pygame.image.load("meteoro.png").convert_alpha()
        self.image = pygame.transform.scale(imagen_original, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad = random.randint(3, 7)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidad = random.randint(3, 7)

# Mostrar pantalla de Game Over
def mostrar_game_over(ventana, puntaje):
    fuente = pygame.font.SysFont(None, 64)
    texto = fuente.render("¡Game Over!", True, BLANCO)
    texto2 = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
    ventana.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 10))
    pygame.display.flip()

# Menú interactivo con selección usando flechas y Enter
def mostrar_menu(ventana):
    opciones = ["Jugar", "Salir"]
    seleccion = 0
    fuente_titulo = pygame.font.SysFont(None, 64)
    fuente_opcion = pygame.font.SysFont(None, 48)

    esperando = True
    while esperando:
        ventana.fill(NEGRO)

        # Título del juego
        titulo = fuente_titulo.render("Guardianes del Tiempo", True, BLANCO)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))

        # Mostrar las opciones
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            texto = fuente_opcion.render(opcion, True, color)
            ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 300 + i * 60))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    if opciones[seleccion] == "Jugar":
                        esperando = False
                    elif opciones[seleccion] == "Salir":
                        pygame.quit()
                        exit()

# Bucle principal del juego
def main():
    jugador = Jugador()
    enemigos = pygame.sprite.Group()
    todos = pygame.sprite.Group()
    todos.add(jugador)

    for _ in range(5):
        enemigo = Enemigo()
        enemigos.add(enemigo)
        todos.add(enemigo)

    jugando = True
    puntaje = 0

    while jugando:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        teclas = pygame.key.get_pressed()
        jugador.update(teclas)
        enemigos.update()

        ventana.fill(NEGRO)
        todos.draw(ventana)

        # Dibuja el puntaje
        fuente = pygame.font.SysFont(None, 36)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        ventana.blit(texto_puntaje, (10, 10))

        pygame.display.flip()

        # Comprobar colisiones
        for enemigo in enemigos:
            if jugador.rect.colliderect(enemigo.rect):
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)

                mostrar_game_over(ventana, puntaje)

                esperando = True
                while esperando:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            esperando = False
                            jugando = False
                        elif evento.type == pygame.KEYDOWN:
                            esperando = False
                            jugando = False

        puntaje += 1

    pygame.quit()

if __name__ == "__main__":
    mostrar_menu(ventana)
    main()
