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
    "PRODUCAO BIBLIOGRAFICA",
    # "TRABALHOS EM EVENTOS",
    # "ARTIGOS PUBLICADOS",
    "LIVROS E CAPITULOS",
}

# Diretório onde os arquivos XML estão localizados
diretorio = "C:\\Users\\henrc\\Desktop\\Proj_Mat"
dados_curriculos = processar_arquivos_xml(diretorio)

palavra_chave = input("Busca: ")

# Realizar a busca
resultados_busca = buscar_por_palavra(dados_curriculos, palavra_chave)
if resultados_busca:
    print(f"\nCurrículos que contêm a palavra '{palavra_chave}':\n")
    for curriculo in resultados_busca:
        print(curriculo)

else:
    print(f"Nenhum currículo encontrado com a palavra '{palavra_chave}'.")
