from cortar_audio import Audio, CorteDoAudio, ExportacaoDosCortesDoAudio
from utils import Mensagem
from transcricoes import Transcricoes

import os
import sys

from variaveis_globais import VariaveisGlobais


if __name__ == "__main__":
	parametros = sys.argv[1:]

	mensagem = Mensagem()

	nenhum_parametro_foi_passado = len(parametros) == 0

	if nenhum_parametro_foi_passado:
		mensagem.mostrar_mensagem_de_erro("Você deve passar ao menos 1 áudio para ser transcrito!")
		sys.exit()

	for caminho_do_audio in parametros:
		variaveis_globais = VariaveisGlobais(caminho_do_audio)


		audio = Audio(variaveis_globais)
		audio()

		ocorreu_algum_erro = audio.erro != ""

		if ocorreu_algum_erro:
			mensagem.mostrar_mensagem_de_erro("\n"+audio.erro)
			continue

		variaveis_globais.audio = audio.audio


		corte_do_audio = CorteDoAudio(variaveis_globais)
		corte_do_audio()

		variaveis_globais.lista_de_cortes = corte_do_audio.lista_de_cortes


		exportacao_dos_cortes_do_audio = ExportacaoDosCortesDoAudio(variaveis_globais)
		exportacao_dos_cortes_do_audio()

		variaveis_globais.nome_dos_cortes_atuais = exportacao_dos_cortes_do_audio.nome_dos_cortes_atuais


		transcricoes = Transcricoes(variaveis_globais)
		transcricoes()