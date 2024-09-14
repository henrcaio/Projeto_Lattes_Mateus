import os
import xmltodict


# Função para ler um único arquivo XML e extrair informações
def extrair_informacoes(xml_file):
    with open(xml_file, "r") as f:
        data = xmltodict.parse(f.read())

    # Extraindo campos do XML
    nome = data["CURRICULO-VITAE"]["DADOS-GERAIS"]["@NOME-COMPLETO"]
    lattes_id = data["CURRICULO-VITAE"]["@NUMERO-IDENTIFICADOR"]
    resumo = data["CURRICULO-VITAE"]["DADOS-GERAIS"]["RESUMO-CV"]["@TEXTO-RESUMO-CV-RH"]
    formacao = data["CURRICULO-VITAE"]["DADOS-GERAIS"]["FORMACAO-ACADEMICA-TITULACAO"]
    # projetos = data["CURRICULO-VITAE"]["PRODUCAO-BIBLIOGRAFICA"]
    # producoes = data["curriculo"].get("producoes", "N/A")

    # Retorna um dicionário com as informações do currículo
    return {
        "nome": nome,
        "lattes_id": lattes_id,
        "resumo": resumo,
        # "formacao": formacao,
        # "projetos": projetos,
        # "producoes": producoes,
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


def buscar_por_palavra(dados_curriculos, palavra):
    resultados = []
    for curriculo in dados_curriculos:
        for chave, valor in curriculo.items():
            if palavra.lower() in str(valor).lower():  # Busca palavra em valores
                resultados.append(curriculo)
                break  # Evita adicionar o mesmo currículo várias vezes
    return resultados


# Diretório onde os arquivos XML estão localizados
diretorio = "C:\\Users\\henrc\\Desktop\\Proj_Mat"
dados_curriculos = processar_arquivos_xml(diretorio)


palavra_chave = input("Busca: ")


# Realizar a busca
resultados_busca = buscar_por_palavra(dados_curriculos, palavra_chave)

# Exibir resultados da pesquisa
if resultados_busca:
    print(f"Currículos que contém a palavra '{palavra_chave}':")
    for curriculo in resultados_busca:
        print(curriculo)
else:
    print(f"Nenhum currículo encontrado com a palavra '{palavra_chave}'.")
