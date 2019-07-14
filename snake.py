import pygame
import pygbutton
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
		self.chance = randint(0, 101)
	def desenhar_fruta(self, cobra, tela):
		if self.aumenta_cobra:
			while (self.pos_x == cobra.cobra[len(cobra.cobra) - 1][0]) and (self.pos_y == cobra.cobra[len(cobra.cobra) - 1][1]):
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
		if cobra.pos_x == self.pos_x and cobra.pos_y == self.pos_y:
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
		self.pos_x = randint(0, (largura - tamanho_x)/10)*10
		self.pos_y = randint(0, (altura - 2*tamanho_y)/10)*10
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


class Menu():
	def __init__(self, largura = 600, altura = 400):
		#tamanho da tela
		self.largura = largura
		self.altura = altura
		self.tela = pygame.display.set_mode((400, 600))
		self.tela.fill((255,255,255)) 
		self.cores = Cor()
		self.botao1 = Button((170, 200, 100, 50), 'Jogar')
		self.botao2 = pygbutton.PygButton((170, 270, 100, 50), 'Instrucoes')
		self.botao3 = pygbutton.PygButton((170, 330, 100, 50), 'Sair')
		pygame.init()
	def escreve_texto(self, msg, cor, tamanho = 25, posicao = [50,0]):
		#criando o texto
		font = pygame.font.SysFont(None, tamanho)
		text = font.render(msg, True, cor)
		self.tela.blit(text, posicao)
	def iniciar_menu(self):
		sair = True
		while sair:
			self.tela.fill(self.cores.white)
			self.escreve_texto("Snake", self.cores.rosina, 70, [150, 120])
			self.botao1.draw(self.tela)
			self.botao2.draw(self.tela)
			self.botao3.draw(self.tela)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sair = False
				self.botao1.handleEvent(event)
				self.botao2.handleEvent(event)
				self.botao3.handleEvent(event)
			pygame.display.flip()
		pygame.quit()

#classe de botoes para o pygame
class Button(pygbutton.PygButton):
	def mouseClick(self, event):
		jogo = Jogo()
		jogo.iniciar_jogo()
		print("oi")
		return True
	
class Jogo():
	def __init__(self, largura = 400, altura = 600):
		#tamanho da tela
		self.largura = largura
		self.altura = altura
		self.tela = pygame.display.set_mode((largura, altura))
		#elementos do jogo
		self.cores = Cor()
		self.cobra = Cobra(self.altura, self.largura, cor = self.cores.green)
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
		#coloca o titulo do jogo
		pygame.display.set_caption("Snake")
	#criando o texto
	def escreve_texto(self, msg, cor, tela, tamanho = 25, posicao = [50,0]):
		#criando o texto
		font = pygame.font.SysFont(None, tamanho)
		text = font.render(msg, True, cor)
		tela.blit(text, posicao)

	def iniciar_jogo(self):
		parte = [1000, 1000]
		game_over = False
		while self.sair and not game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.sair = False
				#calcula a velocidade nova da cobra
				self.cobra.velocidade_cobra(event)
			#recobre a tela com a cor escolhida em rgb
			self.tela.fill(self.cores.rosina)
			#calcula a nova posicao da cobra
			game_over = self.cobra.posicao_cobra(self.frutas, self.largura, self.altura)
			if any((self.cobra.pos_x == self.parte[0] and self.cobra.pos_y == self.parte[1]) for self.parte in self.cobra.cobra[:-1]):
				game_over = True
			#aumenta a cobra se necessario
			self.cobra.aumentar_cobra(game_over)
			#desenha a cobra
			self.cobra.desenhar_cobra(self.tela)
			#desenha o score na tela
			self.score = str(self.cobra.pontos)
			self.texto = "score :  " + self.score
			self.escreve_texto(self.texto, self.cores.white, self.tela)
			#desenha as frutas
			for fruta in self.frutas:
				fruta.desenhar_fruta(self.cobra, self.tela)
			#atualiza a tela toda
			pygame.display.update()
			#limitando o jogo para 15 frames por segundo
			self.relogio.tick(15)
		#para acabar com a tela :)
		if game_over:
			self.escreve_texto("Game Over", self.cores.white, self.tela, tamanho = 50, posicao = [self.altura/5, self.largura/2])
			pygame.display.update()
			print(self.cobra.pos_x, self.cobra.pos_y)
			print("game over")
			time.sleep(2)

menu = Menu()
menu.iniciar_menu()


'''
#jogo principal
jogo = Jogo()
jogo.iniciar_jogo()
'''