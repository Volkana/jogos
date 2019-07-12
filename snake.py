import pygame
import time
from random import randint

#variaveis de cores
#cores em RGB
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#tamanho da tela
largura = 600
altura = 400

#tamanho da cobra
tamanho_x = 10
tamanho_y = 10
#posicao inicial da cobra e maca
cobra = []
parte = []
pos_x = randint(0, (largura - tamanho_x)/10)*10
pos_y = randint(0, (altura - tamanho_y)/10)*10
parte.append(pos_x)
parte.append(pos_y)
cobra.append(parte)

pontos = 0
tamanho = 1
posm_x = randint(0, (largura - tamanho_x)/10)*10
posm_y = randint(0, (altura - tamanho_y)/10)*10
maca = True
velocidade_x = 0.0
velocidade_y = 0.0
pygame.init()

#controlando o fps do jogo
relogio = pygame.time.Clock()

#coloca o tamanho da tela do jogo
tela = pygame.display.set_mode((largura, altura))
#coloca o titulo do jogo
pygame.display.set_caption("bem-vindo ao meu jogo  :)")

#criando uma fonte
font = pygame.font.SysFont(None, 25)
#criando o texto
def escreve_texto(msg, cor):
	text = font.render(msg, True, cor)
	tela.blit(text, [50, 0])



#funcao calcula a velocidade da cobra baseada nos eventos de keyboard:
#e calcula a posicao atual da cobra
def velocidade_cobra(event, velocidade_x, velocidade_y):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			if velocidade_x == 0.0:
				print("entra")
				velocidade_x += -tamanho_x
				velocidade_y = 0
		elif event.key == pygame.K_RIGHT:
			if velocidade_x == 0.0:
				velocidade_x += +tamanho_x
				velocidade_y = 0
		elif event.key == pygame.K_UP:
			if velocidade_y == 0.0:
				velocidade_y += -tamanho_y
				velocidade_x = 0
		elif event.key == pygame.K_DOWN:
			if velocidade_y == 0.0:
				velocidade_y += +tamanho_y
				velocidade_x = 0
		print((velocidade_x == 0), velocidade_y)
	return velocidade_x, velocidade_y

def posicao_cobra(cobra, pos_x, pos_y, posm_x, posm_y, velocidade_x, velocidade_y,pontos, tamanho):
	#calcula a posicao nova
	pos_x += velocidade_x
	pos_y += velocidade_y
	#confere senao saiu da tela
	pos_x, pos_y = cobra_parede(pos_x, pos_y)
	#calcula caso ele va bater na maca
	if posm_x == pos_x and posm_y == pos_y:
		pontos += 1
		tamanho += 1
	#corpo -> fica no lugar q o seu antecessor estava
	return pontos, pos_x, pos_y, tamanho
 
def cobra_parede(pos_x, pos_y):
	if pos_x < 0:
		pos_x = largura
		#sair = False
	elif pos_x > largura - tamanho_x:
		pos_x = tamanho_x
		#sair = False
	elif pos_y < 0:
		pos_y = altura
		#sair = False
	elif pos_y > altura - tamanho_y:
		pos_y = tamanho_y
		#sair = False
	return pos_x, pos_y
sair = True

def aumentar_cobra(cobra, pos_x, pos_y, tamanho):
	parte = []
	parte.append(pos_x)
	parte.append(pos_y)
	cobra.append(parte)
	if len(cobra) > tamanho:
		del cobra[0]
	return cobra

while sair:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sair = False
		#print(event)
		#calcula a velocidade nova da cobra
		velocidade_x, velocidade_y = velocidade_cobra(event, velocidade_x, velocidade_y)
	#recobre a tela com a cor escolhida em rgb
	tela.fill(black)
	#calcula a nova posicao da cobra
	pontos, pos_x, pos_y, tamanho = posicao_cobra(cobra, pos_x, pos_y, posm_x, posm_y, velocidade_x, velocidade_y, pontos, tamanho)
	if any((pos_x == parte[0] and pos_y == parte[1]) for parte in cobra[:-1]):
		break
	#aumenta a cobra se necessario
	cobra = aumentar_cobra(cobra, pos_x, pos_y, tamanho)

	#desenha um retangulo na tela
	for parte in cobra:
		pygame.draw.rect(tela, green, [parte[0], parte[1], tamanho_x, tamanho_y])
	#desenha o score na tela
	score = str(pontos)
	texto = "score :  " + score
	escreve_texto(texto, white)
	#desenha uma maca
	while (posm_x == cobra[len(cobra) - 1][0]) and (posm_y == cobra[len(cobra) - 1][1]):
		posm_x = randint(0, (largura - tamanho_x)/10)*10
		posm_y = randint(0, (altura - tamanho_y)/10)*10
	pygame.draw.rect(tela, red, [posm_x, posm_y, tamanho_x, tamanho_y])
	#atualiza a tela toda
	pygame.display.update()
	#limitando o jogo para 25 frames por segundo
	relogio.tick(25)



#para acabar com a tela :)
pygame.quit()