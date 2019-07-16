import pygame


class Sound():
	def __init__(self, nome_musica, volume = 0.5):
		self.som = pygame.mixer.Sound(nome_musica)
		pygame.mixer.music.set_volume(volume)
	def tocar(self, quantidade = 1):
		pygame.mixer.Sound.play(self.som)


class Cor():
	def __init__(self):
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.red = (255, 0, 0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		self.rosina = (255,153,153)
		self.laranja = (105, 70, 0)
		self.coral = "coral"
		self.lista_cores = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255,153,153), (105, 70, 0), "coral"]
