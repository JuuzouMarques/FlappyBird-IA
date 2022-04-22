import pygame
import os
import random

# Constantes
TELA_LARGURA = 500
TELA_ALTURA = 800
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('Arial', 50)

# Classes


class Passaro:
    IMGS = IMAGENS_PASSARO
    # Animações da Rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    # Atributos
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagemImagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular o Deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # Restringir o Deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento

        # Ângulo do Pássaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # Definir qual imagem do pássaro usar
        self.contagemImagem += 1
        if self.contagemImagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagemImagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagemImagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagemImagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagemImagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagemImagem = 0

        # Não bater asa se o pássaro estiver caindo
        if self.angulo < -80:
            self.imagem = self.IMGS[1]
            self.contagemImagem = self.TEMPO_ANIMACAO*2

        # Desenhar a imagem
        imagemRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posCentroImagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagemRotacionada.get_rect(center=posCentroImagem)
        tela.blit(imagemRotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIADADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posTopo = 0
        self.posBase = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 450)
        self.posTopo = self.altura - self.CANO_TOPO.get_height()
        self.posBase = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIADADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.posTopo))
        tela.blit(self.CANO_BASE, (self.x, self.posBase))

    def colidir(self, passaro):
        passaroMask = passaro.get_mask()
        topoMask = pygame.mask.from_surface(self.CANO_TOPO)
        baseMask = pygame.mask.from_surface(self.CANO_BASE)
        distanciaTopo = (self.x - passaro.x, self.posTopo - round(passaro.y))
        distanciaBase = (self.x - passaro.x, self.posBase - round(passaro.y))
        topoPonto = passaroMask.overlap(topoMask, distanciaTopo)
        basePonto = passaroMask.overlap(baseMask, distanciaBase)
        if topoPonto or basePonto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE
        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))


def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_PONTOS.render(f'Pontuação: {pontos}', True, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # Interação com o Usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # Mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()
        adicionarCano = False
        removerCanos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionarCano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                removerCanos.append(cano)
        if adicionarCano:
            pontos += 1
            canos.append(Cano(600))
        for cano in removerCanos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y <= 0:
                passaros.pop(i)

        desenharTela(tela, passaros, canos, chao, pontos)


# Programa Principal
if __name__ == '__main__':
    main()
