from pathlib import Path
from tqdm import tqdm

from utils import Mensagem

import os
import speech_recognition as sr


r = sr.Recognizer()

mensagem = Mensagem()


class ExtracaoDoNomeDoAudio():
	def __init__(self, caminho_do_audio):
		self.caminho_do_audio = caminho_do_audio

	def separar_partes_do_caminho_do_audio(self):
		self.partes_do_caminho_do_audio = self.caminho_do_audio.split("/")

	def extrair_nome_do_audio(self):
		self.nome_do_audio = self.partes_do_caminho_do_audio[-1]
	
	def montar_identificador_do_audio(self):
		"""
		O "Audio to Text" possui mecanismos que garantem que a transcrição de áudios parcialmente e áudios totalmente transcritos seja mais rápida que a de áudios 0% transcritos.

		Isso é importante para evitar possíveis frustrações do usuário com o programa, porém, também pode resultar em alguns erros.

		Pode acontecer que o usuário queira transcrever um áudio diferente, mas que possui o mesmo nome. É essencial que o programa consiga visualizar que, a despeito de terem o nome igual, eles são áudios diferentes.

		A maneira que escolhi do "Audio to Text" ser capaz de fazer isso é colocar um identificador de cada áudio composto por o nome da pasta em que está o áudio, o nome do áudio e a extensão do áudio, com um "_" entre as palavras.

		A chance de dois áudios serem diferentes mesmo estando em pastas de mesmo nome, possuindo o mesmo nome e sendo da mesma extensão de áudio são bem baixas.

		Desse modo, pelo menos para muitos casos, este problema é solucionado por meio deste estilo de identificador.
		"""
		self.identificador_do_audio = "_".join(
			[
				self.partes_do_caminho_do_audio[-2].replace(" ","_"),
				self.nome_do_audio.replace(".", "_")
			]
		)


	def __call__(self):
		self.separar_partes_do_caminho_do_audio()

		self.extrair_nome_do_audio()

		self.montar_identificador_do_audio()


class Transcricoes():
	def __init__(self, variaveis_globais):
		self.pasta_cortes = variaveis_globais.PASTA_CORTES
		
		self.pasta_transcricoes = variaveis_globais.PASTA_TRANSCRICOES


		self.caminho_do_audio = variaveis_globais.caminho_do_audio
		
		self.identificador_do_audio = variaveis_globais.identificador_do_audio


		self.nome_dos_cortes_atuais = variaveis_globais.nome_dos_cortes_atuais


		self.nome_do_documento_que_contera_a_transcricao_do_audio = variaveis_globais.nome_do_documento_que_contera_a_transcricao_do_audio


	def montar_caminho_do_corte(self, nome_do_corte):
		self.caminho_do_corte = self.pasta_cortes+nome_do_corte

	def montar_nome_do_documento_contendo_a_transcricao_do_corte(self, nome_do_corte):
		self.nome_do_documento_contendo_a_transcricao_do_corte = "doc_de_transcricao_de_{}.odt".format(
				nome_do_corte.replace(".wav","")
			)

	def calcular_tamanho_do_documento_contendo_a_transcricao_do_corte(self):
		caminho_do_documento_contendo_a_transcricao_do_corte = self.pasta_transcricoes+self.nome_do_documento_contendo_a_transcricao_do_corte


		self.tamanho_do_documento = Path(
			r'{}'.format(
				caminho_do_documento_contendo_a_transcricao_do_corte
			)
		).stat().st_size

	def criar_documento_que_contera_transcricao_do_corte_atual(self):
		self.documento_da_transcricao_do_corte = open("{}{}".format(
				self.pasta_transcricoes,
				self.nome_do_documento_contendo_a_transcricao_do_corte
		),'w')

	def transcrever_corte(self):
		with sr.WavFile(self.caminho_do_corte) as source:
			corte = r.record(source)

		try:
			self.retorno_da_ferramenta_de_transcricao = r.recognize_google(
					corte,
					language='pt-BR',
					show_all=True
				)

		except LookupError:
			print("Não foi possível entender {}".format(caminho_do_corte))

	def retornar_transcricao(self):
		return self.retorno_da_ferramenta_de_transcricao["alternative"][0]['transcript']

	def retornar_transcricao_vazia(self, nome_do_corte):
		return "Não foi possível transcrever {}".format(nome_do_corte)

	def escrever_no_documento_de_transcricao_do_corte_o_resultado_da_sua_transcricao(self):
		caminho_do_documento_contendo_a_transcricao_do_corte = self.pasta_transcricoes+self.nome_do_documento_contendo_a_transcricao_do_corte


		with open(
			caminho_do_documento_contendo_a_transcricao_do_corte,
			'a'
		)  as doc_transcricao:
			doc_transcricao.write(
				self.resultado_da_transcricao
			)

	def montar_caminho_do_arquivo_de_transcricao(self, nome_do_arquivo_de_transcricao):
		self.caminho_do_arquivo_de_transcricao = self.pasta_transcricoes+nome_do_arquivo_de_transcricao

	def montar_nome_do_arquivo_de_transcricao(self):
		self.nome_do_arquivo_de_transcricao = "doc_de_transcricao_de_{}.odt".format(
				self.nome_do_corte
			)

	def montar_caminho_do_nome_do_documento_que_contera_a_transcricao_do_audio(self):
		self.caminho_do_nome_do_documento_que_contera_a_transcricao_do_audio = self.pasta_transcricoes+self.nome_do_documento_que_contera_a_transcricao_do_audio

	def verificar_se_o_corte_ja_foi_transcrito(self):
		"""
		Pode acontecer de, por algum motivo, a execução do programa seja interrompida antes de todos os cortes serem transcritos. Outra situação que pode acontecer é de todos os cortes serem transcritos, mas, o programa é interrompido antes das transcrições de cada corte serem juntas em um único arquivo.

		Em ambas as situações, o usuário pode executar novamente o programa passando o(s) mesmo(s) áudios como parâmetro. O problema é que se o áudio for grande pode acontecer do usuário não querer ter de esperar transcrever tudo novamente, optando, então, por outras opções de programa ou por transcrever manualmente. Independente de quais das duas sejam, existe grandes chances dele abandonar o programa.

		Uma maneira de evitar esse abandono do programa é, antes da transcrição, verificar se o corte atual já foi transcrito. Se o corte atual ainda não foi transcrito, realiza a transcrição. Se não, mostra uma mensagem informando que o corte já foi transcrito.

		Ou seja, da 2° tentativa em diante de transcrever o mesmo áudio só irão passar pela transcrição os cortes que não foram transcritos nas tentativas anteriores.

		Dessa forma, o usuário só gastará um pouco mais de tempo que gastaria se o programa não tivesse sido interrompido.

		O processo de transcrição envolve transcrever o corte, criar o documento que conterá o resultado da transcrição e guardar o resultado da transcrição no documento.

		Isso significa que uma maneira de saber se o corte já foi transcrito é verificando se existe na pasta de transcrições um arquivo que seu nome está relacionado ao nome do corte em questão.

		Mas, esse não deve ser o único critério, pois, com somente ele, vai acontecer do programa apontar que o corte foi transcrito mesmo se a interrupção ocorrer antes de guardar o resultado da transcrição no documento.

		A solução para esse problema é verificar se no documento existe o resultado da transcrição.

		A maneira escolhida de realizar essa verificação foi verificar se o tamanho do documento é maior que 0(zero), pois qualquer documento vazio tem tamanho igual a 0(zero) e qualquer documento com pelo menos 1 caractere tem tamanho maior que 0(zero).

		Enfim, um dado corte já foi transcrito quando existe um documento que seu nome está relacionado com o nome do corte e quando esse mesmo documento possui tamanho maior que 0(zero.)
		"""
		self.o_corte_ja_foi_transcrito = self.nome_do_documento_contendo_a_transcricao_do_corte in self.arquivos_da_pasta_transcricoes and self.tamanho_do_documento > 0

	def verificar_se_foi_possivel_transcrever_o_corte(self):
		"""
		A atual ferramenta que está sendo utilizada para transcrever o áudio retorna "[]" como resultado da transcrição quando não foi possível transcrever nada do áudio.

		Já quando foi possível transcrever, o retorno é um dicionário contendo o resultado da transcrição como sendo o valor de uma das chaves.

		O acesso de uma lista vazia é diferente do acesso de um dicionário. Além disso, é necessário substituir o "[]" por um dicionário contendo como resultado da transcrição a frase "Não foi possível transcrever (nome do corte)".

		Considerando isso, é necessário reconhecer quando foi possível transcrever o corte de modo a saber se será ou não necessário substituir o retorno da ferramenta.

		Dado qual é o retorno quando a transcrição foi possível e quando não foi possível, o tipo do resultado da transcrição sempre será "dict" quando foi possível.

		Logo basta verificar se o tipo é igual a "dict" para saber se deu certo ou não a transcrição.
		"""
		self.foi_possivel_transcrever_o_corte = type(self.retorno_da_ferramenta_de_transcricao) is dict


	def __call__(self):
		quantidade_de_cortes_atuais = len(self.nome_dos_cortes_atuais)

		self.arquivos_da_pasta_transcricoes = sorted(
			os.listdir(self.pasta_transcricoes)
		)


		print("\nTranscrevendo os cortes de {}".format(self.caminho_do_audio))

		for self.nome_do_corte in tqdm(self.nome_dos_cortes_atuais):
			self.nome_do_corte = self.nome_do_corte+".wav"

			self.montar_caminho_do_corte(self.nome_do_corte)
			self.montar_nome_do_documento_contendo_a_transcricao_do_corte(
				self.nome_do_corte
			)


			try:
				self.calcular_tamanho_do_documento_contendo_a_transcricao_do_corte()
			except FileNotFoundError:
				self.tamanho_do_documento = 0


			self.verificar_se_o_corte_ja_foi_transcrito()

			if self.o_corte_ja_foi_transcrito:
				mensagem.mostrar_mensagem_de_alerta("O corte {} já foi transcrito!".format(self.nome_do_corte))
			else:
				self.criar_documento_que_contera_transcricao_do_corte_atual()


				self.transcrever_corte()


				self.verificar_se_foi_possivel_transcrever_o_corte()

				if self.foi_possivel_transcrever_o_corte:
					self.resultado_da_transcricao = self.retornar_transcricao()
				else:
					self.resultado_da_transcricao = self.retornar_transcricao_vazia(self.nome_do_corte)

				self.escrever_no_documento_de_transcricao_do_corte_o_resultado_da_sua_transcricao()

		print(end="\n")


		print("Unindo as transcrições dos cortes de {}".format(self.caminho_do_audio))

		transcricoes = []

		for i,self.nome_do_corte in enumerate(tqdm(self.nome_dos_cortes_atuais)):

			self.nome_do_corte = self.nome_do_corte

			self.montar_nome_do_arquivo_de_transcricao()

			self.montar_caminho_do_arquivo_de_transcricao(
				self.nome_do_arquivo_de_transcricao
			)


			with open(self.caminho_do_arquivo_de_transcricao,'r') as doc_transcricao_do_corte:
					linhas = doc_transcricao_do_corte.readlines()

					if not("Não foi possível transcrever" in linhas[0]):
						transcricoes.extend(linhas)

		
		self.montar_caminho_do_nome_do_documento_que_contera_a_transcricao_do_audio()

		with open(self.caminho_do_nome_do_documento_que_contera_a_transcricao_do_audio,'w') as doc_de_transcricao_do_audio:
		
			for linha in transcricoes:
				doc_de_transcricao_do_audio.write(linha+"\n\n")