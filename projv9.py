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


# Função para formatar o texto com base nas chaves selecionadas, separando grandes tópicos
def formatar_saida(dados, chaves_selecionadas):
    if isinstance(dados, dict):
        for key, value in dados.items():
            key_sem_prefixo = key.replace("@", "").replace("-", " ").upper()

            # Exibe apenas se a chave estiver na lista de chaves selecionadas
            if key_sem_prefixo in chaves_selecionadas:
                if isinstance(value, dict):
                    print(f"{key_sem_prefixo}:")
                    formatar_saida(value, chaves_selecionadas)
                elif isinstance(value, list):
                    print(f"{key_sem_prefixo}:")
                    for item in value:
                        formatar_saida(item, chaves_selecionadas)
                elif value:  # Exibe apenas se o valor não for nulo
                    print(f"{key_sem_prefixo}: {value}")

                # Adiciona uma linha em branco apenas entre grandes seções
                if key_sem_prefixo in [
                    "TEXTO RESUMO CV RH",
                    "FORMACAO ACADEMICA",
                    "PRODUCAO BIBLIOGRAFICA",
                ]:
                    print("\n")


# Lista de chaves que queremos exibir
chaves_selecionadas = {
    "NOME COMPLETO",
    "NUMERO IDENTIFICADOR",
    "TEXTO RESUMO CV RH",
    "FORMACAO ACADEMICA",
    "NOME INSTITUICAO",
    "ANO DE INICIO",
    "ANO DE CONCLUSAO",
    "TITULO DO TRABALHO DE CONCLUSAO DE CURSO",
    "NOME DO ORIENTADOR",
    "NOME CURSO",
    "STATUS DO CURSO",
    "PRODUCAO BIBLIOGRAFICA",
    "TRABALHOS EM EVENTOS",
    "TITULO DO TRABALHO",
    "ANO DO TRABALHO",
    "ARTIGOS PUBLICADOS",
    "TITULO DO ARTIGO",
    "ANO DO ARTIGO",
    "LIVROS E CAPITULOS",
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
        print("\n" + "-" * 50 + "\n")  # Linha de separação entre currículos
else:
    print(f"Nenhum currículo encontrado com a palavra '{palavra_chave}'.")
