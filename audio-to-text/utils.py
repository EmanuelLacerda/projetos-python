from colr import color


class Mensagem():
	def __init__(self):
		pass

	def mostrar_mensagem_de_erro(self, mensagem):
		print(color(mensagem, fore='red', style='normal'))

	def mostrar_mensagem_de_alerta(self, mensagem):
		print(color(mensagem, fore='yellow', style='normal'))
