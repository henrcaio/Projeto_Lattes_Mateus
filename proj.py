import os
import xmltodict


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
        "LIVRO-PUBLICADO-OU-ORGANIZADO", []
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
def formatar_formacao_academica(dados):
    formacao_aca = dados.get("FORMACAO-ACADEMICA", [])
    if formacao_aca:
        print(f"--- Formação Acadêmica ---")
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

            # Imprime todos os campos, mesmo que estejam vazios
            print(
                f"Título do Trabalho de Conclusão de Curso: {titulo_trabalho or 'Não informado'}"
            )
            print(f"Nome do Orientador: {nome_orientador or 'Não informado'}")
            print(f"Número ID Orientador: {numero_id_orientador or 'Não informado'}")
            print(f"Instituição: {nome_instituicao or 'Não informado'}")
            print(f"Código do Curso: {codigo_curso or 'Não informado'}")
            print(f"Curso: {nome_curso or 'Não informado'}")
            print(f"Status do Curso: {status_curso or 'Não informado'}")
            print(f"Início: {ano_inicio or 'Não informado'}")
            print(f"Conclusão: {ano_conclusao or 'Não informado'}")
            print(f"Código do Curso CAPES: {codigo_curso_capes or 'Não informado'}")
            print(
                f"Título do Trabalho de Conclusão de Curso (Inglês): {titulo_trabalho_ingles or 'Não informado'}"
            )
            print(f"Nome do Curso (Inglês): {nome_curso_ingles or 'Não informado'}")
            print(
                f"Formação Acadêmica e Titulação: {formacao_academica_titulacao or 'Não informado'}"
            )
            print(f"Tipo de Graduação: {tipo_graduacao or 'Não informado'}")
            print(
                f"Código da Instituição Graduação: {codigo_instituicao_grad or 'Não informado'}"
            )
            print(
                f"Nome da Instituição Graduação: {nome_instituicao_grad or 'Não informado'}"
            )
            print(
                f"Código da Instituição Outra Graduação: {codigo_instituicao_outra_grad or 'Não informado'}"
            )
            print(
                f"Nome da Instituição Outra Graduação: {nome_instituicao_outra_grad or 'Não informado'}"
            )
            print(
                f"Nome do Orientador Graduação: {nome_orientador_grad or 'Não informado'}"
            )
            print("\n")  # Linha em branco para separar as seções


def formatar_trabalhos_em_eventos(dados):
    # Acesso à produção bibliográfica
    producao_bibliografica = dados.get("PRODUCAO-BIBLIOGRAFICA", {})

    trabalhos_em_eventos = producao_bibliografica.get("TRABALHOS EM EVENTOS", [])

    # Verificar se há trabalhos em eventos
    if trabalhos_em_eventos:
        print(f"--- Trabalhos em Eventos ---")

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

            # Imprimindo as informações formatadas
            print(f"Título do Trabalho: {titulo_trabalho or 'Não informado'}")
            print(f"Ano do Trabalho: {ano_trabalho or 'Não informado'}")
            print(f"País do Evento: {pais_evento or 'Não informado'}")
            print(f"Idioma: {idioma_trabalho or 'Não informado'}")
            print(f"Nome do Evento: {nome_evento or 'Não informado'}")
            print(f"Cidade do Evento: {cidade_evento or 'Não informado'}")
            print(f"Ano de Realização: {ano_realizacao_evento or 'Não informado'}")
            print(f"Título dos Anais/Proceedings: {titulo_anais or 'Não informado'}")
            print(f"Volume: {volume or 'Não informado'}")
            print(
                f"Páginas: {pagina_inicial or 'Não informado'} - {pagina_final or 'Não informado'}"
            )

            # Exibindo os autores
            if autores:
                print("Autores:")
                for autor in autores:
                    nome_autor = autor.get("@NOME-COMPLETO-DO-AUTOR", "").strip()
                    nome_para_citacao = autor.get("@NOME-PARA-CITACAO", "").strip()
                    print(
                        f"{nome_autor or 'Não informado'} ({nome_para_citacao or 'Não informado'})"
                    )

            # Exibindo as palavras-chave
            if palavras_chave:
                palavras = [
                    palavras_chave.get(f"@PALAVRA-CHAVE-{i}", "") for i in range(1, 7)
                ]
                print("Palavras-chave: ", ", ".join([p for p in palavras if p]))

            print("\n")  # Linha em branco para separar os trabalhos


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
    # "PRODUCAO BIBLIOGRAFICA",
    # "TRABALHOS EM EVENTOS",
    # "ARTIGOS PUBLICADOS",
    # "LIVROS E CAPITULOS",
}


# Diretório onde os arquivos XML estão localizados
diretorio = "C:\\Users\\henrc\\Desktop\\Proj_Mat"
dados_curriculos = processar_arquivos_xml(diretorio)

palavra_chave = input("Busca: ")

# Realizar a busca
resultados_busca = buscar_por_palavra(dados_curriculos, palavra_chave)

# Exibir resultados da pesquisa formatados
if resultados_busca:
    print(f"\nCurrículos que contêm a palavra '{palavra_chave}':\n")
    for curriculo in resultados_busca:
        formatar_saida(curriculo, chaves_selecionadas)
        formatar_formacao_academica(curriculo)  # Adiciona a parte de formação acadêmica
        formatar_trabalhos_em_eventos(curriculo)  # Adiciona a parte de eventos
        print("\n" + "-" * 50 + "\n")  # Linha de separação entre currículos
else:
    print(f"Nenhum currículo encontrado com a palavra '{palavra_chave}'.")
