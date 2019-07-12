import pygame
import time
from random import randint


class Cor():
	def __init__(self):
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.red = (255, 0, 0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		self.rosina = (255,153,153)
		self.laranja = (105, 70, 0)

class Fruta():
	def __init__(self,altura, largura, tamanho_x = 10, tamanho_y = 10, points_per_fruit = 1, cor = (255, 0, 0), aumenta_cobra = False):
		self.pos_x = randint(0, (largura - tamanho_x)/10)*10
		self.pos_y = randint(0, (altura - tamanho_y)/10)*10
		self.points_per_fruit = points_per_fruit
		self.cor = cor
		self.tamanho_x = tamanho_x
		self.tamanho_y = tamanho_y
		self.altura = altura
		self.largura = largura
		self.aumenta_cobra = aumenta_cobra
	def desenhar_fruta(self, cobra, tela):
		while (self.pos_x == cobra.cobra[len(cobra.cobra) - 1][0]) and (self.pos_y == cobra.cobra[len(cobra.cobra) - 1][1]):
			self.pos_x = randint(0, (self.largura - self.tamanho_x)/10)*10
			self.pos_y = randint(0, (self.altura - self.tamanho_y)/10)*10
		pygame.draw.rect(tela, self.cor, [self.pos_x, self.pos_y, self.tamanho_x, self.tamanho_y])
	def colisao_fruta(self, cobra):
		if cobra.pos_x == self.pos_x and cobra.pos_y == self.pos_y:
			cobra.pontos += self.points_per_fruit
			if self.aumenta_cobra is True:
				cobra.tamanho += 1
		print(cobra.pontos)

class Cobra():
	def __init__(self, largura, altura, tamanho_x = 10, tamanho_y = 10, cor = (0,255,255)):
		#tamanho da cobra
		self.tamanho_x = tamanho_x
		self.tamanho_y = tamanho_y
		#inicializando a lista
		self.cobra = []
		#inicializando as posicoes
		self.pos_x = randint(0, (largura - tamanho_x)/10)*10
		self.pos_y = randint(0, (altura - tamanho_y)/10)*10
		#inicializando a cor
		self.cor = cor
		#colocando na lista
		parte = []
		parte.append(self.pos_x)
		parte.append(self.pos_y)
		self.cobra.append(parte)
		#inicializando os pontos
		self.pontos = 0
		#inicializando a quantidade de partes da cobra
		self.tamanho = 1
		#inicializando a velocidade inicial
		self.velocidade_x = 0.0
		self.velocidade_y = 0.0
	#calcula a velocidade da cobra
	def velocidade_cobra(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				if self.velocidade_x == 0.0:
					self.velocidade_x += -self.tamanho_x
					self.velocidade_y = 0
			elif event.key == pygame.K_RIGHT:
				if self.velocidade_x == 0.0:
					self.velocidade_x += +self.tamanho_x
					self.velocidade_y = 0
			elif event.key == pygame.K_UP:
				if self.velocidade_y == 0.0:
					self.velocidade_y += -self.tamanho_y
					self.velocidade_x = 0
			elif event.key == pygame.K_DOWN:
				if self.velocidade_y == 0.0:
					self.velocidade_y += +self.tamanho_y
					self.velocidade_x = 0
			time.sleep(0.02)
	#calcula a posicao da cobra
	def posicao_cobra(self, frutas, largura, altura):
		#calcula a posicao nova
		self.pos_x += self.velocidade_x
		self.pos_y += self.velocidade_y
		#confere senao saiu da tela
		self.cobra_parede(largura, altura)
		#calcula caso ele va bater nas frutas
		for fruta in frutas:
			fruta.colisao_fruta(self)

	#checa se a cobra bateu na parede
	def cobra_parede(self, largura, altura):
		if self.pos_x < 0:
			self.pos_x = largura
			#sair = False
		elif self.pos_x > largura - self.tamanho_x:
			self.pos_x = self.tamanho_x
			#sair = False
		elif self.pos_y < 0:
			self.pos_y = altura
			#sair = False
		elif self.pos_y > altura - self.tamanho_y:
			self.pos_y = self.tamanho_y
			#sair = False
	#aumenta o tamanho da cobra
	def aumentar_cobra(self):
		parte = []
		parte.append(self.pos_x)
		parte.append(self.pos_y)
		self.cobra.append(parte)
		if len(self.cobra) > self.tamanho:
			del self.cobra[0]
	#desenha a cobra na tela
	def desenhar_cobra(self, tela, cor = None):
			if self.cor == "coral":
				coral = [(255, 153, 00),(255, 255, 255),(0,0,0)]
				# 0 1 2 3 4 5
				#laranja laranja branco preto preto branco
				for k, parte in reversed(list(enumerate(self.cobra))):
					cobra_tamanho = len(self.cobra) - 1
					cobra_parte = abs(cobra_tamanho - k)
					if cobra_parte % 6 == 0 or cobra_parte % 6 == 1:
						pygame.draw.rect(tela, coral[0], [parte[0], parte[1], self.tamanho_x, self.tamanho_y])
					elif cobra_parte % 6 == 2 or cobra_parte % 6 == 5:
						pygame.draw.rect(tela, coral[1], [parte[0], parte[1], self.tamanho_x, self.tamanho_y])
					else:
						pygame.draw.rect(tela, coral[2], [parte[0], parte[1], self.tamanho_x, self.tamanho_y])
			else:
				for parte in cobra.cobra:
					pygame.draw.rect(tela, self.cor, [parte[0], parte[1], self.tamanho_x, self.tamanho_y])


class Menu():
	def __init__(self, tela,cor):
		tela.fill(cor.black)
		#iniciando o jogo
		#criando uma fonte
		self.font = pygame.font.init(None, 25)
		#criando o texto
		def escreve_texto(msg, cor, tela, posicao):
			text = self.font.render(msg,	 True, cor)
			tela.blit(text, posicao)


class Jogo():
	def __init__(self):
		#tamanho da tela
		self.largura = 600
		self.altura = 400
		#elementos do jogo
		self.cores = Cor()
		self.cobra = Cobra(self.altura, self.largura, cor = "coral")
		self.frutas = []
		maca = Fruta(self.altura, self.largura, points_per_fruit = 100, aumenta_cobra = True)
		laranja = Fruta(self.altura, self.largura, points_per_fruit = 500, cor =  self.cores.laranja)
		self.frutas.append(maca)
		self.frutas.append(laranja)
		self.sair = True
		#iniciando o jogo
		pygame.init()
		#controlando o fps do jogo
		self.relogio = pygame.time.Clock()
		#coloca o tamanho da tela do jogo
		self.tela = pygame.display.set_mode((self.largura, self.altura))
		#coloca o titulo do jogo
		pygame.display.set_caption("Snake")
		#criando uma fonte
		self.font = pygame.font.SysFont(None, 25)
	#criando o texto
	def escreve_texto(self,msg, cor):
		self.text = self.font.render(msg, True, cor)
		self.tela.blit(self.text, [50, 0])

	def iniciar_jogo(self):
		parte = [1000, 1000]
		while self.sair:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.sair = False
				#print(event)
				#calcula a velocidade nova da cobra
				self.cobra.velocidade_cobra(event)
			#recobre a tela com a cor escolhida em rgb
			self.tela.fill(self.cores.rosina)
			#calcula a nova posicao da cobra
			self.cobra.posicao_cobra(self.frutas, self.largura, self.altura)
			if any((self.cobra.pos_x == self.parte[0] and self.cobra.pos_y == self.parte[1]) for self.parte in self.cobra.cobra[:-1]):
				break
			#aumenta a cobra se necessario
			self.cobra.aumentar_cobra()
			#desenha a cobra
			self.cobra.desenhar_cobra(self.tela)
			#desenha o score na tela
			self.score = str(self.cobra.pontos)
			self.texto = "score :  " + self.score
			self.escreve_texto(self.texto, self.cores.white)
			#desenha as frutas
			for fruta in self.frutas:
				fruta.desenhar_fruta(self.cobra, self.tela)
			#atualiza a tela toda
			pygame.display.update()
			#limitando o jogo para 15 frames por segundo
			self.relogio.tick(15)
		#para acabar com a tela :)
		pygame.quit()


jogo = Jogo()
jogo.iniciar_jogo()