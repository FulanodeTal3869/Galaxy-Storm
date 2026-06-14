import pygame
import random

pygame.init()
pygame.mixer.init()

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Nave Retrô")

clock = pygame.time.Clock()

# Som
try:
    som_tiro = pygame.mixer.Sound("bala.mp3")
except:
    som_tiro = None

# Imagens
nave_img = pygame.image.load("nave.png").convert_alpha()
nave_img = pygame.transform.scale(nave_img, (64, 64))

inimigo_img = pygame.image.load("inimigo.png").convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))

# Fontes
fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 70)

# Estados
MENU = 0
JOGANDO = 1
GAMEOVER = 2

estado = MENU

# Variáveis globais
velocidade = 8


def reiniciar():
    global jogador_x
    global jogador_y
    global tiros
    global inimigos
    global pontos
    global vida
    global spawn_timer

    jogador_x = LARGURA // 2
    jogador_y = ALTURA - 80

    tiros = []
    inimigos = []

    pontos = 0
    vida = 100

    spawn_timer = 0


class Inimigo:
    def __init__(self):
        self.x = random.randint(0, LARGURA - 50)
        self.y = -50
        self.vel = random.randint(2, 4)

    def mover(self):
        self.y += self.vel

    def desenhar(self):
        tela.blit(inimigo_img, (self.x, self.y))


reiniciar()

rodando = True

while rodando:

    clock.tick(60)

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if estado == MENU:

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar()
                    estado = JOGANDO

        elif estado == JOGANDO:

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:

                    tiros.append(
                        pygame.Rect(jogador_x + 30,jogador_y,5,15))

                    if som_tiro:
                        som_tiro.play()

        elif estado == GAMEOVER:

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar()
                    estado = JOGANDO

    # MENU
    if estado == MENU:

        tela.fill((0, 0, 20))

        titulo = fonte_grande.render("NAVE RETRO",True,(255, 255, 255))

        iniciar = fonte.render("Pressione ESPACO para jogar",True,(255, 255, 255))

        tela.blit(titulo,(LARGURA // 2 - titulo.get_width() // 2,200))

        tela.blit(iniciar,(LARGURA // 2 - iniciar.get_width() // 2,320))

    # JOGO
    elif estado == JOGANDO:

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jogador_x -= velocidade

        if teclas[pygame.K_RIGHT]:
            jogador_x += velocidade

        jogador_x = max(0,min(LARGURA - 64, jogador_x))

        # Spawn dos inimigos (mais lento)
        spawn_timer += 1

        if spawn_timer >= 80:
            inimigos.append(Inimigo())
            spawn_timer = 0

        # Atualizar tiros
        for tiro in tiros[:]:

            tiro.y -= 10

            if tiro.bottom < 0:
                tiros.remove(tiro)

        # Atualizar inimigos
        for inimigo in inimigos[:]:

            inimigo.mover()

            hitbox = pygame.Rect(inimigo.x,inimigo.y,50,50)

            # Colisão tiro x inimigo
            for tiro in tiros[:]:

                if hitbox.colliderect(tiro):

                    if tiro in tiros:
                        tiros.remove(tiro)

                    if inimigo in inimigos:
                        inimigos.remove(inimigo)

                    pontos += 1
                    break

            # Inimigo escapou
            if inimigo in inimigos and inimigo.y > ALTURA:

                inimigos.remove(inimigo)

                vida -= 10

        # Game Over
        if vida <= 0:
            estado = GAMEOVER

        # Desenho
        tela.fill((0, 0, 20))

        tela.blit(nave_img,(jogador_x, jogador_y))

        for tiro in tiros:
            pygame.draw.rect(tela,(255, 255, 0),tiro)

        for inimigo in inimigos:
            inimigo.desenhar()

        # Texto de pontos
        texto = fonte.render(f"Pontos: {pontos}",True,(255, 255, 255))

        tela.blit(texto, (10, 10))

        # Barra de vida
        pygame.draw.rect(tela,(255, 0, 0),(10, 50, 200, 20))

        pygame.draw.rect(tela,(0, 255, 0),(10, 50, vida * 2, 20))

        vida_txt = fonte.render(f"Vida: {vida}",True,(255, 255, 255))

        tela.blit(vida_txt,(220, 45))

    # GAME OVER
    elif estado == GAMEOVER:
        tela.fill((0, 0, 0))
        gameover = fonte_grande.render("GAME OVER",True,(255, 0, 0))
        score = fonte.render(f"Pontos: {pontos}",True,(255, 255, 255))
        reiniciar_txt = fonte.render("Pressione R para reiniciar",True,(255, 255, 255))
        tela.blit(gameover,(LARGURA // 2 - gameover.get_width() // 2,200))
        tela.blit(score,(LARGURA // 2 - score.get_width() // 2,300))
        tela.blit(reiniciar_txt,(LARGURA // 2 - reiniciar_txt.get_width() // 2,350))

    pygame.display.flip()

pygame.quit()