from tqdm import tqdm

import pydub


class Audio():
	"""
	A função dessa classe é carregar os binários do arquivo presente no caminho passado como parâmetro.

	Existe uma série de erros que o usuário pode cometer ao passar um caminho de áudio como parâmetro. Essa série de erros é a listada abaixa:
	- Passar um arquivo que não existe.
	- Passar um arquivo que não é um áudio.
	- Passar um áudio que já foi transcrito.

	Nessa classe esses erros são identificados e informados ao usuário.
	"""
	def __init__(self, variaveis_globais):
		self.caminho_do_audio = variaveis_globais.caminho_do_audio
		
		self.nome_do_documento_que_contera_a_transcricao_do_audio = variaveis_globais.nome_do_documento_que_contera_a_transcricao_do_audio
		
		self.arquivos_da_pasta_transcricoes = variaveis_globais.arquivos_da_pasta_transcricoes


		self.erro = ""

	def __call__(self):
		try:
			self.audio = pydub.AudioSegment.from_file(self.caminho_do_audio)
		except FileNotFoundError:
			self.erro = "O arquivo {} não existe!".format(self.caminho_do_audio)
			return
		except pydub.exceptions.CouldntDecodeError:
			self.erro = "{} não é um arquivo válido! O arquivo deve ser um áudio!".format(self.caminho_do_audio)
			return
		except IndexError:
			print("1")
			self.erro = "{} não é um arquivo válido! O arquivo deve ser um áudio!".format(self.caminho_do_audio)
			return

		"""
		Quando um áudio é completamente transcrito, um arquivo é criado contendo todas as transcrições individuais de cada corte. 

		Considerando isso, para saber se um arquivo já foi transcrito, basta verificar se já existe na subpasta "transcricoes/" o seu respectivo arquivo de transcrição.
		"""
		audio_ja_foi_transcrito = self.nome_do_documento_que_contera_a_transcricao_do_audio in self.arquivos_da_pasta_transcricoes

		if audio_ja_foi_transcrito:
			self.erro = "O áudio {} já foi transcrito!".format(
				self.caminho_do_audio
			)

class CorteDoAudio():
	"""
	Um áudio longo pode demorar para ser transcrito completamente dependendo da máquina. Além disso, existe o risco de ocorrer um problema durante a transcrição, o que implica em ter que começar toda a transcrição novamente.

	Se for cortado o áudio em áudios menores e transcritos individualmente, vai ser possível aproveitar uma porcentagem das transcrições mesmo se ocorrer algum erro.

	Além disso, o programa consegue comparar o nome dos cortes e o nome dos documentos que contém a transcrição e, por conseguinte, identificar quais áudios ainda faltam serem transcritos.

	Por esse motivo, há essa classe para cortar o áudio. O tamanho escolhido para o corte foi de 1 minuto.
	"""
	def __init__(self, variaveis_globais):
		self.audio = variaveis_globais.audio

		self.caminho_do_audio = variaveis_globais.caminho_do_audio

		self.lista_de_cortes = []

		self.umMinutoEmMilisegundos = 60000

	def calcular_quantidade_de_cortes_de_um_minuto(self):
		duracao_do_audio_de_milisegundos = len(self.audio)

		"""
		A etapa mais básica para calcular a quantidade de cortes de um minuto que serão feitos a partir do áudio original é dividindo a duração dele em milissegundos por o valor de 1 minuto em milissegundos.

		Porém, não pode parar esse cálculo aí, pois, se a duração total do áudio tiver minuto e segundo, essa divisão retornará um ponto flutuante e a quantidade de qualquer coisa deve ser um inteiro. Ou seja, o próximo passo é retirar a parte inteira do resultado da divisão.

		Existem maneiras nativas do Python de transformar um ponto flutuante em um inteiro, mas, para evitar o problema de arredondamento para cima, optou-se por fazer a transformação por meio de string.

		Por meio do método de String chamado split() é possível transformar uma string em uma lista em que todos os elementos são strings. Por padrão, o separador é o espaço entre as palavras, mas, é possível especificar um separador diferente.

		O que separa a parte inteira de um número da sua parte decimal é o ".", então, o separador do método split deve ser o ".". Após o uso do split no resultado da divisão, haverá uma lista em que o primeiro elemento é a parte inteira do resultado e o segundo elemento é a parte decimal do mesmo, ambos no formato de string.

		Como a quantidade de cortes deve ser um inteiro, o primeiro elemento da lista, ou seja, o valor da parte inteira, é que será esta quantidade.

		Como falado antes, todos os elementos da lista são strings, então, deve converter para inteiro o valor do primeiro elemento antes de atribuir a ele a variável que a armazena esta quantidade.

		Resumindo, o processo de calcular a quantidade de cortes de 1 minutos é conforme abaixo:
			1. Realizar a divisão entre a duração do áudio em milissegundos e o valor de 1 minuto em milissegundos.
			2. Converter para string o resultado da divisão.
			3. Converter a string em uma lista em que o primeiro elemento é a parte inteira do resultado da divisão e o segundo elemento é a parte decimal do mesmo, ambos os elementos como o tipo string.
			4. Pegar o primeiro elemento da lista.
			5. Converter o primeiro elemento para inteiro.
			6. Atribuir para a variável "quantidade_de_cortes_de_um_minuto" o resultado da conversão para inteiro.
		"""
		self.quantidade_de_cortes_de_um_minuto = int(
			str(
				duracao_do_audio_de_milisegundos/self.umMinutoEmMilisegundos
			).split(".")[0]
		)

	def extrair_corte_atual_do_audio(self, index_do_corte_atual):
		milisegundoInicialDoCorteAtual = self.umMinutoEmMilisegundos*index_do_corte_atual

		milisegundoFinalDoCorteAtual = self.umMinutoEmMilisegundos*(index_do_corte_atual+1)


		self.corte_atual = self.audio[
			(
				milisegundoInicialDoCorteAtual
			):(
				milisegundoFinalDoCorteAtual
			)
		]

	def extrair_ultimo_corte_do_audio(self, index_do_corte_atual):
		milisegundoInicialDoUltimoCorte = self.umMinutoEmMilisegundos*(index_do_corte_atual+1)

		self.ultimo_corte = self.audio[
			milisegundoInicialDoUltimoCorte:
		]

	def __call__(self):
		print("Cortando {}...".format(self.caminho_do_audio))

		self.calcular_quantidade_de_cortes_de_um_minuto()


		for i in tqdm(
			range(
				self.quantidade_de_cortes_de_um_minuto #self.parte_inteira_da_quantidade_de_cortes_de_um_minuto
			)
		):
			self.extrair_corte_atual_do_audio(i)
			self.lista_de_cortes.append(self.corte_atual)


		self.extrair_ultimo_corte_do_audio(i)
		self.lista_de_cortes.append(self.ultimo_corte)


class ExportacaoDosCortesDoAudio():
	def __init__(self, variaveis_globais):
		self.caminho_do_audio = variaveis_globais.caminho_do_audio
		
		self.identificador_do_audio = variaveis_globais.identificador_do_audio
		
		self.lista_de_cortes = variaveis_globais.lista_de_cortes

		self.PASTA_CORTES = variaveis_globais.PASTA_CORTES

	def exportar_corte(self, corte, nome_do_corte):
		corte.export(
			"{}{}.wav".format(self.PASTA_CORTES, nome_do_corte),
			format="wav"
		)

	def __call__(self):
		quantidade_de_cortes = len(self.lista_de_cortes)

		print("\n\nExportando cortes de {}...".format(self.caminho_do_audio))

		self.nome_dos_cortes_atuais = []

		for i,corte in enumerate(tqdm(self.lista_de_cortes)):
			nome_do_corte = "corte_{}_de_{}".format(
				i+1,
				self.identificador_do_audio
			)

			self.nome_dos_cortes_atuais.append(nome_do_corte)

			self.exportar_corte(corte,nome_do_corte)

		print(end="\n")