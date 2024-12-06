import os
import xmltodict
import tkinter as tk
from tkinter import scrolledtext


# Função para ler um único arquivo XML e extrair informações
def extrair_informacoes(xml_file):
    with open(xml_file, "r") as f:
        data = xmltodict.parse(f.read())

    # Extraindo campos do XML
    nome = data["CURRICULO-VITAE"]["DADOS-GERAIS"]["@NOME-COMPLETO"]
    lattes_id = data["CURRICULO-VITAE"]["@NUMERO-IDENTIFICADOR"]
    resumo = (
        data["CURRICULO-VITAE"]["DADOS-GERAIS"]
        .get("RESUMO-CV", {})
        .get("@TEXTO-RESUMO-CV-RH", "Resumo não disponível.")
    )

    # Extraindo formação acadêmica
    formacao = []
    if "FORMACAO-ACADEMICA-TITULACAO" in data["CURRICULO-VITAE"]["DADOS-GERAIS"]:
        for nivel in ["GRADUACAO", "MESTRADO", "DOUTORADO", "POS-DOUTORADO"]:
            if (
                nivel
                in data["CURRICULO-VITAE"]["DADOS-GERAIS"][
                    "FORMACAO-ACADEMICA-TITULACAO"
                ]
            ):
                formacoes_nivel = data["CURRICULO-VITAE"]["DADOS-GERAIS"][
                    "FORMACAO-ACADEMICA-TITULACAO"
                ][nivel]
                if isinstance(formacoes_nivel, list):
                    formacao.extend(formacoes_nivel)
                else:
                    formacao.append(formacoes_nivel)

    # Extraindo produção bibliográfica
    producao_bibliografica = {}
    if "PRODUCAO-BIBLIOGRAFICA" in data["CURRICULO-VITAE"]:
        producao_bibliografica = data["CURRICULO-VITAE"]["PRODUCAO-BIBLIOGRAFICA"]

    # Extração detalhada das subcategorias de produção bibliográfica
    trabalhos_eventos = producao_bibliografica.get("TRABALHOS-EM-EVENTOS", {}).get(
        "TRABALHO-EM-EVENTOS", []
    )
    artigos_publicados = producao_bibliografica.get("ARTIGOS-PUBLICADOS", {}).get(
        "ARTIGO-PUBLICADO", []
    )
    livros_capitulos = producao_bibliografica.get("LIVROS-E-CAPITULOS", {}).get(
        "CAPITULOS-DE-LIVROS-PUBLICADOS", []
    )

    return {
        "NOME-COMPLETO": nome,
        "NUMERO-IDENTIFICADOR": lattes_id,
        "TEXTO-RESUMO-CV-RH": resumo,
        "FORMACAO-ACADEMICA": formacao,
        "PRODUCAO-BIBLIOGRAFICA": {
            "TRABALHOS EM EVENTOS": trabalhos_eventos,
            "ARTIGOS PUBLICADOS": artigos_publicados,
            "LIVROS E CAPITULOS": livros_capitulos,
        },
    }


# Função para processar todos os arquivos XML em um diretório
def processar_arquivos_xml(diretorio):
    curriculos = []
    for filename in os.listdir(diretorio):
        if filename.endswith(".xml"):
            caminho = os.path.join(diretorio, filename)
            curriculo = extrair_informacoes(caminho)
            curriculos.append(curriculo)
    return curriculos


# Função para buscar uma palavra em todos os currículos
def buscar_por_palavra(dados_curriculos, palavra):
    resultados = []
    for curriculo in dados_curriculos:
        for chave, valor in curriculo.items():
            if palavra.lower() in str(valor).lower():  # Busca palavra em valores
                resultados.append(curriculo)
                break  # Evita adicionar o mesmo currículo várias vezes
    return resultados


# Função para remover valores nulos e caracteres indesejados do dicionário
def limpar_dados(dados):
    if isinstance(dados, dict):
        return {
            k.replace("@", "").replace("-", " ").upper(): limpar_dados(v)
            for k, v in dados.items()
            if v
        }
    elif isinstance(dados, list):
        return [limpar_dados(item) for item in dados if item]
    return dados


# Função para formatar a saída dos dados de formação acadêmica
def formatar_formacao_academica(dados, output_text):
    formacao_aca = dados.get("FORMACAO-ACADEMICA", [])
    if formacao_aca:
        output_text.insert(tk.END, "--- Formação Acadêmica ---\n")
        for nivel in formacao_aca:
            # Extrai os valores, mesmo que vazios
            titulo_trabalho = nivel.get(
                "@TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO", ""
            ).strip()
            nome_orientador = nivel.get("@NOME-DO-ORIENTADOR", "").strip()
            numero_id_orientador = nivel.get("@NUMERO-ID-ORIENTADOR", "").strip()
            nome_instituicao = nivel.get("@NOME-INSTITUICAO", "").strip()
            codigo_curso = nivel.get("@CODIGO-CURSO", "").strip()
            nome_curso = nivel.get("@NOME-CURSO", "").strip()
            status_curso = nivel.get("@STATUS-DO-CURSO", "").strip()
            ano_inicio = nivel.get("@ANO-DE-INICIO", "").strip()
            ano_conclusao = nivel.get("@ANO-DE-CONCLUSAO", "").strip()
            codigo_curso_capes = nivel.get("@CODIGO-CURSO-CAPES", "").strip()
            titulo_trabalho_ingles = nivel.get(
                "@TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO-INGLES", ""
            ).strip()
            nome_curso_ingles = nivel.get("@NOME-CURSO-INGLES", "").strip()
            formacao_academica_titulacao = nivel.get(
                "@FORMACAO-ACADEMICA-TITULACAO", ""
            ).strip()
            tipo_graduacao = nivel.get("@TIPO-GRADUACAO", "").strip()
            codigo_instituicao_grad = nivel.get("@CODIGO-INSTITUICAO-GRAD", "").strip()
            nome_instituicao_grad = nivel.get("@NOME-INSTITUICAO-GRAD", "").strip()
            codigo_instituicao_outra_grad = nivel.get(
                "@CODIGO-INSTITUICAO-OUTRA-GRAD", ""
            ).strip()
            nome_instituicao_outra_grad = nivel.get(
                "@NOME-INSTITUICAO-OUTRA-GRAD", ""
            ).strip()
            nome_orientador_grad = nivel.get("@NOME-ORIENTADOR-GRAD", "").strip()

            # Adiciona os campos ao output_text (em vez de imprimir no terminal)
            output_text.insert(
                tk.END,
                f"Título do Trabalho de Conclusão de Curso: {titulo_trabalho or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END, f"Nome do Orientador: {nome_orientador or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END,
                f"Número ID Orientador: {numero_id_orientador or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END, f"Instituição: {nome_instituicao or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"Código do Curso: {codigo_curso or 'Não informado'}\n"
            )
            output_text.insert(tk.END, f"Curso: {nome_curso or 'Não informado'}\n")
            output_text.insert(
                tk.END, f"Status do Curso: {status_curso or 'Não informado'}\n"
            )
            output_text.insert(tk.END, f"Início: {ano_inicio or 'Não informado'}\n")
            output_text.insert(
                tk.END, f"Conclusão: {ano_conclusao or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END,
                f"Código do Curso CAPES: {codigo_curso_capes or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Título do Trabalho de Conclusão de Curso (Inglês): {titulo_trabalho_ingles or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Nome do Curso (Inglês): {nome_curso_ingles or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Formação Acadêmica e Titulação: {formacao_academica_titulacao or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END, f"Tipo de Graduação: {tipo_graduacao or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END,
                f"Código da Instituição Graduação: {codigo_instituicao_grad or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Nome da Instituição Graduação: {nome_instituicao_grad or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Código da Instituição Outra Graduação: {codigo_instituicao_outra_grad or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Nome da Instituição Outra Graduação: {nome_instituicao_outra_grad or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Nome do Orientador Graduação: {nome_orientador_grad or 'Não informado'}\n",
            )
            output_text.insert(tk.END, "\n")  # Linha em branco para separar as seções


def formatar_trabalhos_em_eventos(dados, output_text):
    # Acesso à produção bibliográfica
    producao_bibliografica = dados.get("PRODUCAO-BIBLIOGRAFICA", {})

    trabalhos_em_eventos = producao_bibliografica.get("TRABALHOS EM EVENTOS", [])

    # Verificar se há trabalhos em eventos
    if trabalhos_em_eventos:
        output_text.insert(tk.END, "--- Trabalhos em Eventos ---\n")

        for evento in trabalhos_em_eventos:
            dados_basicos_trabalho = evento.get("DADOS-BASICOS-DO-TRABALHO", {})
            detalhamento_trabalho = evento.get("DETALHAMENTO-DO-TRABALHO", {})
            autores = evento.get("AUTORES", [])
            palavras_chave = evento.get("PALAVRAS-CHAVE", {})

            # Extraindo informações básicas
            titulo_trabalho = dados_basicos_trabalho.get(
                "@TITULO-DO-TRABALHO", ""
            ).strip()
            ano_trabalho = dados_basicos_trabalho.get("@ANO-DO-TRABALHO", "").strip()
            pais_evento = dados_basicos_trabalho.get("@PAIS-DO-EVENTO", "").strip()
            idioma_trabalho = dados_basicos_trabalho.get("@IDIOMA", "").strip()

            # Detalhes do evento
            nome_evento = detalhamento_trabalho.get("@NOME-DO-EVENTO", "").strip()
            cidade_evento = detalhamento_trabalho.get("@CIDADE-DO-EVENTO", "").strip()
            ano_realizacao_evento = detalhamento_trabalho.get(
                "@ANO-DE-REALIZACAO", ""
            ).strip()
            titulo_anais = detalhamento_trabalho.get(
                "@TITULO-DOS-ANAIS-OU-PROCEEDINGS", ""
            ).strip()
            volume = detalhamento_trabalho.get("@VOLUME", "").strip()
            pagina_inicial = detalhamento_trabalho.get("@PAGINA-INICIAL", "").strip()
            pagina_final = detalhamento_trabalho.get("@PAGINA-FINAL", "").strip()

            # Adicionando as informações ao output_text
            output_text.insert(
                tk.END, f"Título do Trabalho: {titulo_trabalho or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"Ano do Trabalho: {ano_trabalho or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"País do Evento: {pais_evento or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"Idioma: {idioma_trabalho or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"Nome do Evento: {nome_evento or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"Cidade do Evento: {cidade_evento or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END,
                f"Ano de Realização: {ano_realizacao_evento or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END,
                f"Título dos Anais/Proceedings: {titulo_anais or 'Não informado'}\n",
            )
            output_text.insert(tk.END, f"Volume: {volume or 'Não informado'}\n")
            output_text.insert(
                tk.END,
                f"Páginas: {pagina_inicial or 'Não informado'} - {pagina_final or 'Não informado'}\n",
            )

            # Exibindo os autores
            if autores:
                output_text.insert(tk.END, "Autores:\n")
                for autor in autores:
                    nome_autor = autor.get("@NOME-COMPLETO-DO-AUTOR", "").strip()
                    nome_para_citacao = autor.get("@NOME-PARA-CITACAO", "").strip()
                    output_text.insert(
                        tk.END,
                        f"{nome_autor or 'Não informado'} ({nome_para_citacao or 'Não informado'})\n",
                    )

            # Exibindo as palavras-chave
            if palavras_chave:
                palavras = [
                    palavras_chave.get(f"@PALAVRA-CHAVE-{i}", "") for i in range(1, 7)
                ]
                output_text.insert(
                    tk.END, f"Palavras-chave: {', '.join([p for p in palavras if p])}\n"
                )

            output_text.insert(
                tk.END, "\n"
            )  # Linha em branco para separar os trabalhos


def formatar_artigos_publicados(dados, output_text):
    # Acesso à produção bibliográfica
    producao_bibliografica = dados.get("PRODUCAO-BIBLIOGRAFICA", {})

    artigos_publicados = producao_bibliografica.get("ARTIGOS PUBLICADOS", [])

    # Verificar se há artigos publicados
    if artigos_publicados:
        output_text.insert(tk.END, "--- Artigos Publicados ---\n")

        for artigo in artigos_publicados:
            dados_basicos_artigo = artigo.get("DADOS-BASICOS-DO-ARTIGO", {})
            detalhamento_artigo = artigo.get("DETALHAMENTO-DO-ARTIGO", {})
            autores = artigo.get("AUTORES", [])
            palavras_chave = artigo.get("PALAVRAS-CHAVE", {})

            # Extraindo informações básicas
            titulo_artigo = dados_basicos_artigo.get("@TITULO-DO-ARTIGO", "").strip()
            ano_artigo = dados_basicos_artigo.get("@ANO-DO-ARTIGO", "").strip()
            pais_publicacao = dados_basicos_artigo.get(
                "@PAIS-DE-PUBLICACAO", ""
            ).strip()
            idioma_artigo = dados_basicos_artigo.get("@IDIOMA", "").strip()
            meio_divulgacao = dados_basicos_artigo.get(
                "@MEIO-DE-DIVULGACAO", ""
            ).strip()
            doi = dados_basicos_artigo.get("@DOI", "").strip()

            # Detalhes do artigo
            nome_periodico = detalhamento_artigo.get(
                "@TITULO-DO-PERIODICO-OU-REVISTA", ""
            ).strip()
            issn = detalhamento_artigo.get("@ISSN", "").strip()
            volume = detalhamento_artigo.get("@VOLUME", "").strip()
            fasciculo = detalhamento_artigo.get("@FASCICULO", "").strip()
            serie = detalhamento_artigo.get("@SERIE", "").strip()
            pagina_inicial = detalhamento_artigo.get("@PAGINA-INICIAL", "").strip()
            pagina_final = detalhamento_artigo.get("@PAGINA-FINAL", "").strip()
            local_publicacao = detalhamento_artigo.get(
                "@LOCAL-DE-PUBLICACAO", ""
            ).strip()

            # Adicionando as informações ao output_text
            output_text.insert(
                tk.END, f"Título do Artigo: {titulo_artigo or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"Ano do Artigo: {ano_artigo or 'Não informado'}\n"
            )
            output_text.insert(
                tk.END, f"País de Publicação: {pais_publicacao or 'Não informado'}\n"
            )
            output_text.insert(tk.END, f"Idioma: {idioma_artigo or 'Não informado'}\n")
            output_text.insert(
                tk.END, f"Meio de Divulgação: {meio_divulgacao or 'Não informado'}\n"
            )
            output_text.insert(tk.END, f"DOI: {doi or 'Não informado'}\n")
            output_text.insert(
                tk.END,
                f"Nome do Periódico/Revista: {nome_periodico or 'Não informado'}\n",
            )
            output_text.insert(tk.END, f"ISSN: {issn or 'Não informado'}\n")
            output_text.insert(tk.END, f"Volume: {volume or 'Não informado'}\n")
            output_text.insert(tk.END, f"Fascículo: {fasciculo or 'Não informado'}\n")
            output_text.insert(tk.END, f"Série: {serie or 'Não informado'}\n")
            output_text.insert(
                tk.END,
                f"Páginas: {pagina_inicial or 'Não informado'} - {pagina_final or 'Não informado'}\n",
            )
            output_text.insert(
                tk.END, f"Local de Publicação: {local_publicacao or 'Não informado'}\n"
            )

            # Exibindo os autores
            if autores:
                output_text.insert(tk.END, "Autores:\n")
                for autor in autores:
                    nome_autor = autor.get("@NOME-COMPLETO-DO-AUTOR", "").strip()
                    nome_para_citacao = autor.get("@NOME-PARA-CITACAO", "").strip()
                    output_text.insert(
                        tk.END,
                        f"{nome_autor or 'Não informado'} ({nome_para_citacao or 'Não informado'})\n",
                    )

            # Exibindo as palavras-chave
            if palavras_chave:
                palavras = [
                    palavras_chave.get(f"@PALAVRA-CHAVE-{i}", "") for i in range(1, 7)
                ]
                output_text.insert(
                    tk.END, f"Palavras-chave: {', '.join([p for p in palavras if p])}\n"
                )

            output_text.insert(tk.END, "\n")  # Linha em branco para separar os artigos


def formatar_capitulos(dados, output_text):
    # Verificar se há capítulos de livro publicados
    producao_bibliografica = dados.get("PRODUCAO-BIBLIOGRAFICA", {})
    livros_e_capitulos = producao_bibliografica.get("LIVROS E CAPITULOS", {})
    capitulos = livros_e_capitulos.get("CAPITULO-DE-LIVRO-PUBLICADO", None)

    # Verificar se é um único dicionário ou uma lista de capítulos
    if capitulos:
        # Se for um único dicionário, transformar em lista para padronizar o processamento
        if isinstance(capitulos, dict):
            capitulos = [capitulos]

        output_text.insert(tk.END, "--- Capítulos de Livros Publicados ---\n")
        for capitulo in capitulos:
            dados_basicos = capitulo.get("DADOS-BASICOS-DO-CAPITULO", {})
            detalhamento = capitulo.get("DETALHAMENTO-DO-CAPITULO", {})
            autores = capitulo.get("AUTORES", [])
            palavras_chave = capitulo.get("PALAVRAS-CHAVE", {})

            # Extraindo informações básicas do capítulo
            titulo_capitulo = dados_basicos.get(
                "@TITULO-DO-CAPITULO-DO-LIVRO", "Não informado"
            )
            ano = dados_basicos.get("@ANO", "Não informado")
            idioma = dados_basicos.get("@IDIOMA", "Não informado")
            pais = dados_basicos.get("@PAIS-DE-PUBLICACAO", "Não informado")
            doi = dados_basicos.get("@DOI", "Não informado")

            # Detalhamento do capítulo
            titulo_livro = detalhamento.get("@TITULO-DO-LIVRO", "Não informado")
            organizadores = detalhamento.get("@ORGANIZADORES", "Não informado")
            cidade_editora = detalhamento.get("@CIDADE-DA-EDITORA", "Não informado")
            editora = detalhamento.get("@NOME-DA-EDITORA", "Não informado")
            pagina_inicial = detalhamento.get("@PAGINA-INICIAL", "Não informado")
            pagina_final = detalhamento.get("@PAGINA-FINAL", "Não informado")
            isbn = detalhamento.get("@ISBN", "Não informado")

            # Adicionando as informações ao output_text
            output_text.insert(tk.END, f"Título do Capítulo: {titulo_capitulo}\n")
            output_text.insert(tk.END, f"Ano: {ano}\n")
            output_text.insert(tk.END, f"Idioma: {idioma}\n")
            output_text.insert(tk.END, f"País: {pais}\n")
            output_text.insert(tk.END, f"DOI: {doi}\n")
            output_text.insert(tk.END, f"Publicado em: {titulo_livro}\n")
            output_text.insert(tk.END, f"Organizadores: {organizadores}\n")
            output_text.insert(tk.END, f"Cidade da Editora: {cidade_editora}\n")
            output_text.insert(tk.END, f"Editora: {editora}\n")
            output_text.insert(tk.END, f"Páginas: {pagina_inicial} - {pagina_final}\n")
            output_text.insert(tk.END, f"ISBN: {isbn}\n")

            # Exibindo autores
            if isinstance(autores, list):
                output_text.insert(tk.END, "Autores:\n")
                for autor in autores:
                    if isinstance(autor, dict):
                        nome_completo = autor.get(
                            "@NOME-COMPLETO-DO-AUTOR", "Não informado"
                        )
                        ordem_autoria = autor.get("@ORDEM-DE-AUTORIA", "Não informado")
                        output_text.insert(
                            tk.END, f"- {nome_completo} (Ordem: {ordem_autoria})\n"
                        )
                    else:
                        output_text.insert(tk.END, f"- {autor} (Formato inválido)\n")
            else:
                output_text.insert(tk.END, "Autores não estão em formato esperado.\n")

            # Exibindo palavras-chave
            output_text.insert(tk.END, "Palavras-chave:\n")
            for i in range(1, 7):
                palavra = palavras_chave.get(f"@PALAVRA-CHAVE-{i}", "")
                if palavra:
                    output_text.insert(tk.END, f"- {palavra}\n")

            output_text.insert(
                tk.END, "\n"
            )  # Linha em branco para separar os capítulos


# Função para formatar a saída de dados gerais
def formatar_saida(dados, chaves_selecionadas):
    dados_limpos = limpar_dados(dados)  # Limpa os dados antes de formatar
    if isinstance(dados_limpos, dict):
        for key, value in dados_limpos.items():
            # Exibe apenas se a chave estiver na lista de chaves selecionadas
            if key in chaves_selecionadas:
                print(f"--- {key.replace('_', ' ').title()} ---")  # Título da seção
                if isinstance(value, dict):
                    formatar_saida(value, chaves_selecionadas)
                elif isinstance(value, list):
                    if value:  # Certifique-se de que a lista não está vazia
                        for item in value:
                            # Formatar cada item da lista com detalhes
                            if isinstance(item, dict):
                                for subkey, subvalue in item.items():
                                    print(
                                        f"{subkey.replace('_', ' ').title()}: {subvalue}"
                                    )
                            else:
                                print(f"{item}")
                    else:
                        print("Nenhum item disponível.")  # Indica listas vazias
                else:  # Exibe apenas se o valor não for nulo
                    print(value)

                # Adiciona uma linha em branco após cada seção
                print("\n")  # Adiciona uma nova linha para melhor espaçamento


# Lista de chaves que queremos exibir
chaves_selecionadas = {
    "NOME COMPLETO",
    "NUMERO IDENTIFICADOR",
    "TEXTO RESUMO CV RH",
}


# Diretório onde os arquivos XML estão localizados
diretorio = "C:\\Users\\henrc\\Desktop\\Proj_Mat"
dados_curriculos = processar_arquivos_xml(diretorio)


# Função de busca e formatação
def buscar_e_exibir():
    palavra_chave = entry_busca.get().strip()  # Obtém a palavra-chave digitada
    if not palavra_chave:
        output_text.delete(1.0, tk.END)  # Limpa a área de texto
        output_text.insert(
            tk.END, "Por favor, insira uma palavra-chave para a busca.\n"
        )
        return

    # Busca nos currículos (essa parte assume que 'dados_curriculos' já foi processado)
    resultados_busca = buscar_por_palavra(dados_curriculos, palavra_chave)

    # Exibe os resultados
    output_text.delete(1.0, tk.END)  # Limpa a área de texto
    if resultados_busca:
        output_text.insert(
            tk.END, f"Currículos que contêm a palavra '{palavra_chave}':\n\n"
        )
        for curriculo in resultados_busca:
            # Formatação personalizada
            formatar_saida(curriculo, chaves_selecionadas, output_text)
            formatar_formacao_academica(
                curriculo, output_text
            )  # Exibe formação acadêmica
            formatar_trabalhos_em_eventos(
                curriculo, output_text
            )  # Exibe trabalhos em eventos
            formatar_artigos_publicados(curriculo, output_text)  # Exibe artigos
            formatar_capitulos(curriculo, output_text)  # Exibe capítulos de livros
            output_text.insert(tk.END, "\n" + "-" * 50 + "\n")  # Linha de separação
    else:
        output_text.insert(
            tk.END, f"Nenhum currículo encontrado com a palavra '{palavra_chave}'.\n"
        )


# Função de formatação que escreve diretamente na área de texto do Tkinter
def formatar_saida(dados, chaves_selecionadas, output_text):
    dados_limpos = limpar_dados(dados)  # Limpa os dados antes de formatar
    if isinstance(dados_limpos, dict):
        for key, value in dados_limpos.items():
            if key in chaves_selecionadas:
                output_text.insert(
                    tk.END, f"--- {key.replace('_', ' ').title()} ---\n"
                )  # Título da seção
                if isinstance(value, dict):
                    formatar_saida(value, chaves_selecionadas, output_text)
                elif isinstance(value, list):
                    if value:  # Certifique-se de que a lista não está vazia
                        for item in value:
                            if isinstance(item, dict):
                                for subkey, subvalue in item.items():
                                    output_text.insert(
                                        tk.END,
                                        f"{subkey.replace('_', ' ').title()}: {subvalue}\n",
                                    )
                            else:
                                output_text.insert(tk.END, f"{item}\n")
                    else:
                        output_text.insert(
                            tk.END, "Nenhum item disponível.\n"
                        )  # Indica listas vazias
                else:
                    output_text.insert(tk.END, f"{value}\n")
                output_text.insert(
                    tk.END, "\n"
                )  # Adiciona uma nova linha para melhor espaçamento


# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Busca por Currículos")

# Caixa de pesquisa
label_busca = tk.Label(root, text="Digite a palavra-chave:")
label_busca.pack(padx=10, pady=5)

entry_busca = tk.Entry(root, width=50)
entry_busca.pack(padx=10, pady=5)

# Botão de busca
btn_buscar = tk.Button(root, text="Buscar", command=buscar_e_exibir)
btn_buscar.pack(pady=10)

# Área de texto para exibir os resultados
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=5)

# Rodar a interface
root.mainloop()
