import pygame
import pygbutton
import time
from random import randint
from efeitos import Sound, Cor

class Fruta():
	def __init__(self,altura, largura, tamanho_x = 10, tamanho_y = 10, points_per_fruit = 1, cor = (255, 0, 0), aumenta_cobra = False):
		self.comer_fruta = Sound("eatfruit.wav")
		self.pos_x = randint(0, (largura - tamanho_x)/10)*10
		self.pos_y = randint(0, (altura - tamanho_y)/10)*10
		self.points_per_fruit = points_per_fruit
		self.cor = cor
		self.tamanho_x = tamanho_x
		self.tamanho_y = tamanho_y
		self.altura = altura
		self.largura = largura
		self.aumenta_cobra = aumenta_cobra
		self.chance = randint(0, 101)
	def desenhar_fruta(self, cobra, tela):
		if self.aumenta_cobra:
			while (any((self.pos_x == parte[0] and self.pos_y == parte[1]) for parte in cobra.cobra)):
				self.pos_x = randint(0, (self.largura - self.tamanho_x)/10)*10
				self.pos_y = randint(0, (self.altura - self.tamanho_y)/10)*10
			pygame.draw.rect(tela, self.cor, [self.pos_x, self.pos_y, self.tamanho_x, self.tamanho_y])
		else:
			if self.chance >= 70:
				while (self.pos_x == cobra.cobra[len(cobra.cobra) - 1][0]) and (self.pos_y == cobra.cobra[len(cobra.cobra) - 1][1]):
					self.pos_x = randint(0, (self.largura - self.tamanho_x)/10)*10
					self.pos_y = randint(0, (self.altura - self.tamanho_y)/10)*10
				pygame.draw.rect(tela, self.cor, [self.pos_x, self.pos_y, self.tamanho_x, self.tamanho_y])

	def colisao_fruta(self, cobra, frutas):
		print(cobra.pos_x, cobra.pos_y, self.pos_x, self. pos_y)
		#comparar se a posicao futura da cobra come a fruta
		if cobra.pos_x == self.pos_x and cobra.pos_y == self.pos_y:
			#tocar a musica
			self.comer_fruta.tocar()
			cobra.pontos += self.points_per_fruit
			if self.aumenta_cobra is True:
				cobra.tamanho += 1
				for fruta in frutas:
					fruta.chance = randint(0, 101)
		print(cobra.pontos)

class Cobra():
	def __init__(self, largura, altura, tamanho_x = 10, tamanho_y = 10, cor = (0,255,255)):
		#tamanho da cobra
		self.tamanho_x = tamanho_x
		self.tamanho_y = tamanho_y
		#inicializando a lista
		self.cobra = []
		#inicializando as posicoes
		self.pos_x = randint(0, (altura - tamanho_x)/10)*10
		self.pos_y = randint(0, (largura - tamanho_y)/10)*10
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
		#acessorios da cobra
		self.acessorios = Acessorios()
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
			time.sleep(0.04)
	#calcula a posicao da cobra
	def posicao_cobra(self, frutas, largura, altura):
		game_over = True
		#calcula a posicao nova
		self.pos_x += self.velocidade_x
		self.pos_y += self.velocidade_y
		#confere senao saiu da tela
		game_over = self.cobra_parede(largura, altura)
		print(game_over)
		if game_over:
			return game_over
		#calcula caso ele va bater nas frutas
		for fruta in frutas:
			fruta.colisao_fruta(self, frutas)
		return game_over

	#checa se a cobra bateu na parede
	def cobra_parede(self, largura, altura):
		if self.pos_x < 0:
			#self.pos_x = largura
			self.pos_x = 0
			return True
			#sair = False
		elif self.pos_x > largura:
			self.pos_x = largura
			return True
			#self.pos_x = self.tamanho_x
			#sair = False
		elif self.pos_y < 0:
			self.pos_y = 0
			return True
			#self.pos_y = altura
			#sair = False
		elif self.pos_y > altura:
			self.pos_y = largura
			return True
			#self.pos_y = self.tamanho_y
			#sair = False
		return False
	#aumenta o tamanho da cobra
	def aumentar_cobra(self, game_over):
		parte = []
		if not game_over:
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
				for parte in self.cobra:
					pygame.draw.rect(tela, self.cor, [parte[0], parte[1], self.tamanho_x, self.tamanho_y])
					self.acessorios.olhos(self, tela)
					self.acessorios.lingua(self, tela)



class Acessorios():
	def olhos(self, cobra, tela):
		if cobra.velocidade_y == 0:
			pygame.draw.rect(tela, (0, 0, 0), [cobra.pos_x + 2, cobra.pos_y, 3, 3])
			pygame.draw.rect(tela, (0, 0, 0), [cobra.pos_x + 7, cobra.pos_y, 3, 3])
		elif cobra.velocidade_y < 0:
			pygame.draw.rect(tela, (0, 0, 0), [cobra.pos_x, cobra.pos_y + 2, 3, 3])
			pygame.draw.rect(tela, (0, 0, 0), [cobra.pos_x, cobra.pos_y + 7, 3, 3])
		else:
			pygame.draw.rect(tela, (0, 0, 0), [cobra.pos_x + cobra.tamanho_x - 3, cobra.pos_y + 2, 3, 3])
			pygame.draw.rect(tela, (0, 0, 0), [cobra.pos_x + cobra.tamanho_x - 3, cobra.pos_y + 7, 3, 3])

	def lingua(self,cobra,tela):
		if cobra.velocidade_x < 0:
			pygame.draw.rect(tela, (255, 0, 0), [cobra.pos_x - 1, cobra.pos_y + 5, -3, 3])
			pygame.draw.rect(tela, (255, 0, 0), [cobra.pos_x - 5, cobra.pos_y + 4, -2, 2])
			pygame.draw.rect(tela, (255, 0, 0), [cobra.pos_x - 5, cobra.pos_y + 6, -2, 2])
		elif cobra.velocidade_x > 0:
			pygame.draw.rect(tela, (255, 0, 0), [cobra.pos_x + cobra.tamanho_x + 1, cobra.pos_y + 5, +3, 3])
			pygame.draw.rect(tela, (255, 0, 0), [cobra.pos_x + cobra.tamanho_x + 5, cobra.pos_y + 4, +2, 2])
			pygame.draw.rect(tela, (255, 0, 0), [cobra.pos_x + cobra.tamanho_x + 5, cobra.pos_y + 6, +2, 2])
			