import os
import xmltodict
import tkinter as tk
from tkinter import filedialog, messagebox


# Função para ler um único arquivo XML e extrair informações
def extrair_informacoes(xml_file):
    with open(xml_file, "r") as f:
        data = xmltodict.parse(f.read())

    # Extraindo campos do XML
    nome = data["CURRICULO-VITAE"]["DADOS-GERAIS"].get("@NOME-COMPLETO", "N/A")
    lattes_id = data["CURRICULO-VITAE"].get("@NUMERO-IDENTIFICADOR", "N/A")
    resumo = data["CURRICULO-VITAE"]["DADOS-GERAIS"]["RESUMO-CV"].get(
        "@TEXTO-RESUMO-CV-RH", "N/A"
    )
    formacao = data["CURRICULO-VITAE"]["DADOS-GERAIS"].get(
        "FORMACAO-ACADEMICA-TITULACAO", {}
    )
    projetos = data["CURRICULO-VITAE"].get("PRODUCAO-BIBLIOGRAFICA", "N/A")
    producoes = data["CURRICULO-VITAE"].get("producoes", "N/A")

    return {
        "nome": nome,
        "lattes_id": lattes_id,
        "resumo": resumo,
        "formacao": formatar_formacao(formacao),
        "projetos": projetos,
        "producoes": producoes,
    }


# Função para formatar a formação acadêmica
def formatar_formacao(formacao):
    formacao_formatada = []

    # Se formacao for um dicionário, transforme-o em uma lista
    if isinstance(formacao, dict):
        formacao = [formacao]

    niveis = ["GRADUACAO", "MESTRADO", "DOUTORADO", "POS-DOUTORADO"]

    for nivel in niveis:
        for item in formacao:
            if isinstance(item, dict) and item.get("@NIVEL") == str(
                niveis.index(nivel) + 1
            ):
                instituicao = item.get("@NOME-INSTITUICAO", "N/A")
                curso = item.get("@NOME-CURSO", "N/A")
                ano_inicio = item.get("@ANO-DE-INICIO", "N/A")
                ano_conclusao = item.get("@ANO-DE-CONCLUSAO", "N/A")
                resumo = f"{nivel} - {curso} ({instituicao}) - Início: {ano_inicio}, Conclusão: {ano_conclusao}"
                formacao_formatada.append(resumo)

    if not formacao_formatada:
        return "Nenhuma formação acadêmica encontrada."

    return "\n".join(formacao_formatada)


# Função para processar todos os arquivos XML em um diretório
def processar_arquivos_xml(diretorio):
    curriculos = []
    for filename in os.listdir(diretorio):
        if filename.endswith(".xml"):
            caminho = os.path.join(diretorio, filename)
            curriculo = extrair_informacoes(caminho)
            curriculos.append(curriculo)
    return curriculos


# Função para buscar uma palavra nos currículos
def buscar_por_palavra(dados_curriculos, palavra):
    resultados = []
    for curriculo in dados_curriculos:
        for chave, valor in curriculo.items():
            if palavra.lower() in str(valor).lower():
                resultados.append(curriculo)
                break  # Evita adicionar o mesmo currículo várias vezes
    return resultados


# Função para selecionar o diretório de arquivos XML
def selecionar_diretorio():
    diretorio = filedialog.askdirectory()
    if diretorio:
        label_diretorio["text"] = f"Diretório: {diretorio}"
        return diretorio
    return None


# Função para realizar a busca
def realizar_busca():
    palavra_chave = entry_palavra.get().strip()
    diretorio = label_diretorio["text"].replace("Diretório: ", "").strip()

    if not diretorio or not palavra_chave:
        messagebox.showwarning(
            "Atenção",
            "Por favor, selecione um diretório e insira uma palavra para busca.",
        )
        return

    dados_curriculos = processar_arquivos_xml(diretorio)
    resultados_busca = buscar_por_palavra(dados_curriculos, palavra_chave)

    if resultados_busca:
        resultado_text.delete(1.0, tk.END)  # Limpar o Text widget
        for idx, curriculo in enumerate(resultados_busca, start=1):
            resultado_text.insert(tk.END, f"Currículo {idx}:\n")
            resultado_text.insert(tk.END, f"Nome: {curriculo['nome']}\n")
            resultado_text.insert(tk.END, f"Lattes ID: {curriculo['lattes_id']}\n")
            # resultado_text.insert(tk.END, f"Resumo: {curriculo['resumo']}\n")
            resultado_text.insert(tk.END, f"Formação:\n{curriculo['formacao']}\n")
            # resultado_text.insert(tk.END, f"Projetos: {curriculo['projetos']}\n")
            # resultado_text.insert(tk.END, f"Produções: {curriculo['producoes']}\n")
            resultado_text.insert(tk.END, "-" * 40 + "\n")
    else:
        messagebox.showinfo(
            "Busca", f"Nenhum currículo encontrado com a palavra '{palavra_chave}'."
        )


# Interface gráfica (GUI)
root = tk.Tk()
root.title("Busca de Currículos")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# Diretório Label e Botão de Seleção
frame_diretorio = tk.Frame(root, bg="#f0f0f0")
frame_diretorio.pack(padx=10, pady=5)

label_diretorio = tk.Label(
    frame_diretorio,
    text="Diretório: Nenhum selecionado",
    bg="#f0f0f0",
    font=("Arial", 10),
)
label_diretorio.pack(side=tk.LEFT)

botao_diretorio = tk.Button(
    frame_diretorio,
    text="Selecionar Diretório",
    command=selecionar_diretorio,
    bg="#007BFF",
    fg="white",
    font=("Arial", 10),
)
botao_diretorio.pack(side=tk.RIGHT)

# Campo de entrada para a palavra-chave
frame_busca = tk.Frame(root, bg="#f0f0f0")
frame_busca.pack(padx=10, pady=5)

label_palavra = tk.Label(
    frame_busca, text="Palavra-chave:", bg="#f0f0f0", font=("Arial", 10)
)
label_palavra.pack(side=tk.LEFT)

entry_palavra = tk.Entry(frame_busca, width=30, font=("Arial", 10))
entry_palavra.pack(side=tk.LEFT, padx=5)

# Botão para realizar a busca
botao_busca = tk.Button(
    root,
    text="Buscar",
    command=realizar_busca,
    bg="#28a745",
    fg="white",
    font=("Arial", 10),
)
botao_busca.pack(pady=5)

# Campo de texto para exibir os resultados
resultado_text = tk.Text(root, width=70, height=20, font=("Arial", 10))
resultado_text.pack(padx=10, pady=10)

# Iniciar a aplicação
root.mainloop()
