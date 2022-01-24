from transcricoes import ExtracaoDoNomeDoAudio

import os


class VariaveisGlobais():
	def __init__(self, caminho_do_audio):
		self.caminho_do_audio = caminho_do_audio


		self.PASTA_CORTES = 'cortes/'
		self.PASTA_TRANSCRICOES = 'transcricoes/'


		self.extracao_do_nome_do_audio = ExtracaoDoNomeDoAudio(self.caminho_do_audio)

		self.extracao_do_nome_do_audio()

		self.identificador_do_audio = self.extracao_do_nome_do_audio.identificador_do_audio

		self.nome_do_audio_com_extensao = self.extracao_do_nome_do_audio.nome_do_audio


		self.arquivos_da_pasta_transcricoes = sorted(
			os.listdir(
				self.PASTA_TRANSCRICOES
			)
		)


		self.nome_do_documento_que_contera_a_transcricao_do_audio = "doc_de_transcricao_de_{}.odt".format(
				self.identificador_do_audio
		)

