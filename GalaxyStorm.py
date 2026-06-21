import pygame
import random

pygame.init()
pygame.mixer.init()

# =========================
# TELA
# =========================

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Galaxy Storm")

clock = pygame.time.Clock()

# =========================
# SOM
# =========================

try:
    som_tiro = pygame.mixer.Sound("bala.mp3")
except:
    som_tiro = None

try:
    som_gameover = pygame.mixer.Sound("gameover.mp3")
except:
    som_gameover = None

try:
    som_dano = pygame.mixer.Sound("alarm.mp3")
except:
    som_dano = None

modo_jogo = 1
som_gameover_tocado = False

# =========================
# IMAGENS
# =========================

logo = pygame.image.load("logo.png").convert_alpha()
logo = pygame.transform.scale(logo, (800, 600))

nave_img = pygame.image.load("nave.png").convert_alpha()
nave_img = pygame.transform.scale(nave_img, (64, 64))

# Nave do jogador 2
try:
    nave2_img = pygame.image.load("nave2.png").convert_alpha()
    nave2_img = pygame.transform.scale(nave2_img, (64, 64))
except:
    nave2_img = nave_img

inimigo_img = pygame.image.load("inimigo.png").convert_alpha()
inimigo_img = pygame.transform.scale(inimigo_img, (50, 50))

# Fundo
try:
    fundo = pygame.image.load("Fundo.jpg").convert()
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
except:
    fundo = None

try:
    som_explosao = pygame.mixer.Sound("explosão.wav")
except:
    som_explosao = None


# =========================
# FONTES
# =========================

fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 70)

# =========================
# ESTADOS
# =========================

MENU = 0
JOGANDO = 1
GAMEOVER = 2

condicao = 0

estado = MENU

# =========================
# CONFIG
# =========================

velocidade = 8
modo_jogo = 1

# =========================
# REINICIAR
# =========================

def reiniciar():
    global jogador_x,jogador_y,jogador2_x,jogador2_y,tiros,inimigos,pontos,vida,spawn_timer,som_gameover_tocado

    som_gameover_tocado = False

    jogador_x = 250
    jogador_y = ALTURA - 90

    jogador2_x = 500
    jogador2_y = ALTURA - 90

    tiros = []
    inimigos = []

    pontos = 0
    vida = 100

    spawn_timer = 0

# =========================
# CLASSE INIMIGO
# =========================

class Inimigo:

    def __init__(self):
        self.x = random.randint(0, LARGURA - 50)
        self.y = -50
        self.vel = random.randint(2, 4)

    def mover(self):
        self.y += self.vel

    def desenhar(self):
        tela.blit(inimigo_img, (self.x, self.y))

# =========================
# INICIAR
# =========================

reiniciar()

rodando = True

# =========================
# LOOP PRINCIPAL
# =========================

while rodando:

    clock.tick(60)

    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill((0, 0, 20))

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # =====================
        # MENU
        # =====================

        if estado == MENU:

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_1:
                    modo_jogo = 1
                    condicao = 53
                    reiniciar()
                    estado = JOGANDO

                if evento.key == pygame.K_2:
                    modo_jogo = 2
                    condicao = 27
                    reiniciar()
                    estado = JOGANDO


        # =====================
        # JOGANDO
        # =====================

        elif estado == JOGANDO:

            if evento.type == pygame.KEYDOWN:

                # Jogador 1 atira
                if evento.key == pygame.K_f:

                    tiros.append(
                        pygame.Rect(jogador_x + 30,jogador_y,5,15))

                    if som_tiro:
                        som_tiro.play()

                # Jogador 2 atira
                if modo_jogo == 2:

                    if evento.key == pygame.K_KP_0:

                        tiros.append(
                            pygame.Rect(jogador2_x + 30,jogador2_y,5,15))

                        if som_tiro:
                            som_tiro.play()

        # =====================
        # GAME OVER
        # =====================

        elif estado == GAMEOVER:

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_r:
                    reiniciar()
                    estado = JOGANDO

                if evento.key == pygame.K_ESCAPE:
                    estado = MENU

    # =========================
    # MENU
    # =========================

    if estado == MENU:

        tela.fill((0, 0, 0))

        tela.blit(logo,(LARGURA // 2 - logo.get_width() // 2,20))


    # =========================
    # JOGANDO
    # =========================

    elif estado == JOGANDO:

        teclas = pygame.key.get_pressed()

        # Jogador 1

        if teclas[pygame.K_a]:
            jogador_x -= velocidade

        if teclas[pygame.K_d]:
            jogador_x += velocidade

        # Jogador 2

        if modo_jogo == 2:

            if teclas[pygame.K_LEFT]:
                jogador2_x -= velocidade

            if teclas[pygame.K_RIGHT]:
                jogador2_x += velocidade

        jogador_x = max(0,min(LARGURA - 64, jogador_x))

        jogador2_x = max(0, min(LARGURA - 64, jogador2_x))

        # =====================
        # SPAWN
        # =====================

        spawn_timer += 1

        if spawn_timer >= condicao:
            inimigos.append(Inimigo())
            spawn_timer = 0

        # =====================
        # TIROS
        # =====================

        for tiro in tiros[:]:

            tiro.y -= 10

            if tiro.bottom < 0:
                tiros.remove(tiro)

        # =====================
        # INIMIGOS
        # =====================

        for inimigo in inimigos[:]:

            inimigo.mover()

            hitbox = pygame.Rect(inimigo.x,inimigo.y,50,50)

            for tiro in tiros[:]:

                if hitbox.colliderect(tiro):

                    if tiro in tiros:
                        tiros.remove(tiro)

                    if inimigo in inimigos:
                        inimigos.remove(inimigo)

                        if som_explosao:
                            som_explosao.play()

                    pontos += 1
                    break

            if inimigo in inimigos:

                if inimigo.y > ALTURA:

                    inimigos.remove(inimigo)

                    vida -= 10

                    if som_dano:
                        som_dano.play()

        # =====================
        # GAME OVER
        # =====================

        if vida <= 0:

            estado = GAMEOVER

            if not som_gameover_tocado:

                if som_gameover:
                    som_gameover.play()

                som_gameover_tocado = True

        # =====================
        # DESENHO
        # =====================
        
        # Jogador 1
        tela.blit(nave_img,(jogador_x, jogador_y))

        # Jogador 2
        if modo_jogo == 2:
            tela.blit(nave2_img,(jogador2_x, jogador2_y))

        # Tiros
        for tiro in tiros:
            pygame.draw.rect(tela,(255, 255, 0),tiro)

        # Inimigos
        for inimigo in inimigos:
            inimigo.desenhar()

        # Pontos
        texto = fonte.render(f"Pontos: {pontos}",True,(255, 255, 255))

        tela.blit(texto, (10, 10))

        # Vida
        pygame.draw.rect(tela,(255, 0, 0),(10, 50, 200, 20))

        pygame.draw.rect(tela,(0, 255, 0),(10, 50, vida * 2, 20))

        vida_txt = fonte.render(f"Vida: {vida}",True,(255, 255, 255))

        tela.blit(vida_txt, (220, 45))

    # =========================
    # GAME OVER
    # =========================

    elif estado == GAMEOVER:

        tela.fill((0, 0, 0))

        gameover = fonte_grande.render("GAME OVER",True,(255, 0, 0))
        score = fonte.render(f"Pontos: {pontos}",True,(255, 255, 255))
        reiniciar_txt = fonte.render("R - Reiniciar",True,(255, 255, 255))
        menu_txt = fonte.render("ESC - Menu",True,(255, 255, 255))

        tela.blit(gameover,(LARGURA // 2 - gameover.get_width() // 2,180))
        tela.blit(score,(LARGURA // 2 - score.get_width() // 2,280))
        tela.blit(reiniciar_txt,(LARGURA // 2 - reiniciar_txt.get_width() // 2,340))
        tela.blit(menu_txt,(LARGURA // 2 - menu_txt.get_width() // 2,390))

    pygame.display.flip()
pygame.quit()