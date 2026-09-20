import pygame
import random
import sys

# Inicialização do motor gráfico
pygame.init()

# ==========================================
# CONFIGURAÇÕES DA TELA E CONSTANTES
# ==========================================
LARGURA_TELA = 800
ALTURA_TELA = 600
display = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Projeto Extensão: Alfabetização Motora Digital")

# Paleta de Cores de Alto Contraste (Acessibilidade Visual)
COR_FUNDO = (30, 30, 40)
COR_TEXTO = (255, 255, 255)
COR_DESTAQUE = (255, 215, 0)
COR_UI_FUNDO = (0, 0, 0)

# Fontes grandes e legíveis
fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fonte_instrucao = pygame.font.SysFont("Arial", 24)
fonte_hud = pygame.font.SysFont("Arial", 28, bold=True)

# Temporizador global
fps_clock = pygame.time.Clock()

# ==========================================
# VARIÁVEIS DE ESTADO E ENTIDADES (Refatoradas)
# ==========================================
# Atributos do Cursor (Substituindo o antigo "jogador")
dimensao_cursor = 65
pos_x_cursor = LARGURA_TELA // 2
pos_y_cursor = ALTURA_TELA - dimensao_cursor - 20
vel_movimento = 9

# Atributos do Objeto Coletável (Substituindo a antiga "estrela")
dimensao_coletavel = 35
pos_x_coletavel = random.randint(0, LARGURA_TELA - dimensao_coletavel)
pos_y_coletavel = -50
queda_vel = 4.5

# Variáveis de Controle de Fluxo
pontos_adquiridos = 0
tempo_maximo = 60 # 60 segundos de jogo
estado_atual = "MENU" # Estados: MENU, JOGANDO, FIM

# ==========================================
# FUNÇÕES DE INTERFACE E LÓGICA
# ==========================================
def renderizar_painel_hud(superficie, x, y, largura, altura, opacidade):
    """
    Desenha o painel transparente para exibir o placar e tempo.
    Mantém o padrão visual do projeto garantindo a leitura sobre objetos do jogo.
    """
    painel = pygame.Surface((largura, altura))
    painel.set_alpha(opacidade)
    painel.fill(COR_UI_FUNDO)
    superficie.blit(painel, (x, y))

def tela_menu_inicial():
    display.fill(COR_FUNDO)
    
    texto_titulo = fonte_titulo.render("Treinamento Motor", True, COR_DESTAQUE)
    texto_instrucao1 = fonte_instrucao.render("Use as SETAS (Esquerda/Direita) para mover.", True, COR_TEXTO)
    texto_instrucao2 = fonte_instrucao.render("Colete os itens amarelos antes do tempo acabar.", True, COR_TEXTO)
    texto_iniciar = fonte_instrucao.render("Pressione [ESPAÇO] para Iniciar", True, COR_DESTAQUE)
    
    display.blit(texto_titulo, (LARGURA_TELA//2 - texto_titulo.get_width()//2, 150))
    display.blit(texto_instrucao1, (LARGURA_TELA//2 - texto_instrucao1.get_width()//2, 250))
    display.blit(texto_instrucao2, (LARGURA_TELA//2 - texto_instrucao2.get_width()//2, 300))
    display.blit(texto_iniciar, (LARGURA_TELA//2 - texto_iniciar.get_width()//2, 450))

def tela_fim_de_jogo():
    display.fill(COR_FUNDO)
    
    texto_fim = fonte_titulo.render("Tempo Esgotado!", True, COR_TEXTO)
    texto_placar = fonte_instrucao.render(f"Você conseguiu {pontos_adquiridos} pontos.", True, COR_DESTAQUE)
    texto_reiniciar = fonte_instrucao.render("Pressione [R] para Reiniciar ou [ESC] para Sair", True, COR_TEXTO)
    
    display.blit(texto_fim, (LARGURA_TELA//2 - texto_fim.get_width()//2, 200))
    display.blit(texto_placar, (LARGURA_TELA//2 - texto_placar.get_width()//2, 280))
    display.blit(texto_reiniciar, (LARGURA_TELA//2 - texto_reiniciar.get_width()//2, 400))

# ==========================================
# LOOP PRINCIPAL DO SISTEMA
# ==========================================
tempo_inicio_jogo = 0

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            if estado_atual == "MENU" and evento.key == pygame.K_SPACE:
                estado_atual = "JOGANDO"
                pontos_adquiridos = 0
                queda_vel = 4.5
                tempo_inicio_jogo = pygame.time.get_ticks()
                
            elif estado_atual == "FIM" and evento.key == pygame.K_r:
                estado_atual = "MENU"

    # Máquina de Estados
    if estado_atual == "MENU":
        tela_menu_inicial()
        
    elif estado_atual == "FIM":
        tela_fim_de_jogo()
        
    elif estado_atual == "JOGANDO":
        # 1. Movimentação e Input
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and pos_x_cursor > 0:
            pos_x_cursor -= vel_movimento
        if teclas[pygame.K_RIGHT] and pos_x_cursor < LARGURA_TELA - dimensao_cursor:
            pos_x_cursor += vel_movimento

        # Lógica de Gravidade
        pos_y_coletavel += queda_vel
        if pos_y_coletavel > ALTURA_TELA:
            pos_y_coletavel = -50
            pos_x_coletavel = random.randint(0, LARGURA_TELA - dimensao_coletavel)

        # 2. Detecção de Colisão
        hitbox_cursor = pygame.Rect(pos_x_cursor, pos_y_cursor, dimensao_cursor, dimensao_cursor)
        hitbox_coletavel = pygame.Rect(pos_x_coletavel, pos_y_coletavel, dimensao_coletavel, dimensao_coletavel)

        if hitbox_cursor.colliderect(hitbox_coletavel):
            pontos_adquiridos += 15
            pos_y_coletavel = -50
            pos_x_coletavel = random.randint(0, LARGURA_TELA - dimensao_coletavel)
            queda_vel += 0.15 # Curva de dificuldade suave

        # 3. Lógica do Cronômetro
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio_jogo) // 1000
        tempo_restante = max(0, tempo_maximo - tempo_decorrido)
        
        if tempo_restante <= 0:
            estado_atual = "FIM"

        # 4. Renderização do Jogo
        display.fill(COR_FUNDO)

        # Desenhar cursor (Cesta) e objeto (Estrela/Componente)
        pygame.draw.rect(display, COR_TEXTO, hitbox_cursor, border_radius=8)
        pygame.draw.circle(display, COR_DESTAQUE, (int(pos_x_coletavel + dimensao_coletavel/2), int(pos_y_coletavel + dimensao_coletavel/2)), dimensao_coletavel//2)

        # Desenhar UI Transparente
        renderizar_painel_hud(display, 20, 20, 380, 50, 160)
        
        texto_pontos = fonte_hud.render(f"Pontuação: {pontos_adquiridos}", True, COR_TEXTO)
        texto_tempo = fonte_hud.render(f"Tempo: {tempo_restante}s", True, COR_DESTAQUE if tempo_restante > 10 else (255, 50, 50))
        
        display.blit(texto_pontos, (35, 30))
        display.blit(texto_tempo, (240, 30))

    pygame.display.update()
    fps_clock.tick(60)