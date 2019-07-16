import pygame
import pygbutton
import time
from random import randint
from personagens import Cobra, Fruta
from efeitos import Cor, Sound


#definindo o audio
pygame.mixer.pre_init(44100, 16, 2 , 4096) 


class Menu():
	def __init__(self, largura = 600, altura = 400):
		#tamanho da tela
		self.largura = largura
		self.altura = altura
		self.tela = pygame.display.set_mode((400, 600))
		self.tela.fill((255,255,255)) 
		self.cores = Cor()
		#botao de iniciar o jogo
		self.botao2 = Button2((170, 270, 100, 50), 'Jogar')
		#botao de sair do jogo
		self.botao3 = Button3((170, 330, 100, 50), 'Sair')
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
			self.botao2.draw(self.tela)
			self.botao3.draw(self.tela)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sair = False
				self.botao2.handleEvent(event)
				self.botao3.handleEvent(event)
			pygame.display.flip()
		pygame.quit()

#classe de botoes para o pygame

class Button2(pygbutton.PygButton):
	def mouseClick(self, event):
		mudar_cor = Mudar_cor()
		mudar_cor.desenhar_tela()

class Button3(pygbutton.PygButton):
	def mouseClick(self, event):
		quit()

class Mudar_cor():
	def __init__(self, largura = 400, altura = 600):
		self.largura = largura
		self.altura = altura
		self.tela = pygame.display.set_mode((largura, altura))
		self.cores = Cor()
		self.cobra = Cobra(self.altura, self.largura, cor = self.cores.green)
		self.lista_botao =[]
		self.botao_jogar = Botao_jogar(150, 550, largura = 50, altura = 100, cor = self.cores.white)
		#criando um botao para cada cor
		posx = 75
		posy = 225
		for pos, cor in enumerate(self.cores.lista_cores):
			botao = Botao_cor(posx = posx, posy = posy, cor = cor)
			self.lista_botao.append(botao)
			posx += 75
			if posx > 300:
				posx = 75
				posy += 75

	def escreve_texto(self, msg, cor, tamanho = 25, posicao = [50,0]):
		#criando o texto
		font = pygame.font.SysFont(None, tamanho)
		text = font.render(msg, True, cor)
		self.tela.blit(text, posicao)
		
	def desenhar_tela(self):
		self.cobra.cobra = [[150,100],[160,100],[170,100],[180,100],[180,110],[180,120],[190,120],[200,120]]
		self.cobra.pos_x = 150
		self.cobra.pos_y = 100
		sair = True
		while sair:
			for event in pygame.event.get():
				for botao in self.lista_botao:
					botao.tratar_evento(self.cobra)
				sair = self.botao_jogar.tratar_evento(self.cobra)
				if event.type == pygame.QUIT:
					sair = False
			self.tela.fill(self.cores.rosina)
			self.escreve_texto("Escolha a cor da sua cobra", self.cores.white, 35, [50,50])
			self.cobra.desenhar_cobra(self.tela)
			pygame.draw.rect(self.tela, self.cores.rosina, [50, 200, 300, 350])
			for botao in self.lista_botao:
				botao.desenhar_botao(self.tela)

			self.botao_jogar.desenhar_botao(self.tela)
			pygame.display.flip()

class Botao_cor():
	def __init__(self, posx, posy, msg = "oi", cor = (255, 0, 0), largura= 50, altura= 50):
		self.msg = msg
		self.cor = cor
		self.largura = largura
		self.altura = altura
		self.posx = posx
		self.posy = posy
	def desenhar_botao(self, tela):
		mouse = pygame.mouse.get_pos()
		#muda a cor do botao caso passe o mouse por cima
		if self.posx + self.altura > mouse[0] > self.posx and self.posy + self.largura > mouse[1] > self.posy:
			pygame.draw.rect(tela, (0,0,0), [self.posx, self.posy, self.altura, self.largura])
		else:
			if self.cor == "coral":
				pygame.draw.rect(tela, (0,0,0), [self.posx, self.posy, self.altura, self.largura])
				return
			pygame.draw.rect(tela, self.cor, [self.posx, self.posy, self.altura, self.largura])
	def tratar_evento(self, cobra):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if self.posx + self.altura > mouse[0] > self.posx and self.posy + self.largura > mouse[1] > self.posy and click[0] == 1:
			self.acao(cobra)
			return False
		return True
	def acao(self,cobra):
		cobra.cor = self.cor

class Botao_jogar(Botao_cor):
	def acao(self, cobra):
		jogo = Jogo(cobra.cor)
		jogo.iniciar_jogo()

class Jogo():
	def __init__(self, cor = (0, 255, 0), largura = 400, altura = 600):
		#tamanho da tela
		self.largura = largura
		self.altura = altura
		self.tela = pygame.display.set_mode((largura, altura))
		#elementos do jogo
		self.cores = Cor()
		self.cobra = Cobra(self.altura, self.largura, cor = cor)
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
		#controlando a musica 
		pygame.mixer.music.load("snake_song.mp3")
		pygame.mixer.music.set_volume(0.4)
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
		pygame.mixer.music.play(-1)
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
		pygame.mixer.music.stop()
		if game_over:
			self.escreve_texto("Game Over", self.cores.white, self.tela, tamanho = 50, posicao = [self.altura/5, self.largura/2])
			pygame.display.update()
			print(self.cobra.pos_x, self.cobra.pos_y)
			print("game over")
			time.sleep(2)

menu = Menu()
menu.iniciar_menu()
