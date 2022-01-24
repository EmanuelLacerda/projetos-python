from os import listdir, makedirs

from transcricoes import ExtracaoDoNomeDoAudio


class VariaveisGlobais():
	def __init__(self, caminho_do_audio):
		self.caminho_do_audio = caminho_do_audio


		self.PASTA_CORTES = 'cortes/'
		self.PASTA_TRANSCRICOES = 'transcricoes/'


		self.extracao_do_nome_do_audio = ExtracaoDoNomeDoAudio(self.caminho_do_audio)

		self.extracao_do_nome_do_audio()

		self.identificador_do_audio = self.extracao_do_nome_do_audio.identificador_do_audio

		self.nome_do_audio_com_extensao = self.extracao_do_nome_do_audio.nome_do_audio


		try:
			self.arquivos_da_pasta_transcricoes = sorted(
					listdir(
						self.PASTA_TRANSCRICOES
				)
			)
		except FileNotFoundError:
			"""
			No GitHub não é possível enviar pastas vazias que é o caso das subpastas "transcricoes/" e "cortes/".

			Devido a isso, quando o usuário for executar o programa logo após ter feito o clone e ter instalado as libs, não haverá essas duas subpastas.

			Além disso, pode acontecer do usuário, intencionalmente ou não, remover uma dessas subpastas ou até as duas.

			Assim, é necessário que essas subpastas sejam criadas sempre que elas não existirem na pasta raiz.

			A linha de código abaixo faz a criação da subpasta "transcricoes/". A criação da outra subpasta ocorre em outro momento da execução.
			"""
			makedirs("transcricoes/")

			self.arquivos_da_pasta_transcricoes = sorted(
				listdir(
					self.PASTA_TRANSCRICOES
				)
			)


		self.nome_do_documento_que_contera_a_transcricao_do_audio = "doc_de_transcricao_de_{}.odt".format(
				self.identificador_do_audio
		)

