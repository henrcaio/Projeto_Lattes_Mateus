import os
import xmltodict
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Função para ler um único arquivo XML e extrair informações
def extrair_informacoes(xml_file):
    with open(xml_file, "r") as f:
        data = xmltodict.parse(f.read())

    # Extraindo campos do XML
    nome = data["CURRICULO-VITAE"]["DADOS-GERAIS"]["@NOME-COMPLETO"]
    lattes_id = data["CURRICULO-VITAE"]["@NUMERO-IDENTIFICADOR"]

    return {
        "nome": nome,
        "lattes_id": lattes_id,
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


# Função para buscar uma palavra nos currículos
def buscar_por_palavra(dados_curriculos, palavra):
    resultados = []
    for curriculo in dados_curriculos:
        for chave, valor in curriculo.items():
            if palavra.lower() in str(valor).lower():  # Busca palavra em valores
                resultados.append(curriculo)
                break  # Evita adicionar o mesmo currículo várias vezes
    return resultados


# Função para selecionar diretório com os arquivos XML
def selecionar_diretorio():
    diretorio = filedialog.askdirectory()
    if diretorio:
        label_diretorio["text"] = f"Diretório: {diretorio}"
        return diretorio
    return None


# Função para realizar a busca pela palavra digitada
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
        resultado_tree.delete(
            *resultado_tree.get_children()
        )  # Limpar a árvore de resultados
        for idx, curriculo in enumerate(resultados_busca, start=1):
            resultado_tree.insert(
                "", "end", values=(idx, curriculo["nome"], curriculo["lattes_id"])
            )
    else:
        messagebox.showinfo(
            "Busca", f"Nenhum currículo encontrado com a palavra '{palavra_chave}'."
        )


# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Busca de Currículos")
root.geometry("600x400")
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
    font=("Arial", 10),
    relief="solid",
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
    relief="solid",
)
botao_busca.pack(pady=5)

# Tabela para exibir os resultados da busca
colunas = ("#", "Nome", "Lattes ID")
resultado_tree = ttk.Treeview(root, columns=colunas, show="headings", height=10)
resultado_tree.pack(padx=10, pady=10)

# Definindo o cabeçalho da tabela
resultado_tree.heading("#", text="#")
resultado_tree.heading("Nome", text="Nome")
resultado_tree.heading("Lattes ID", text="Lattes ID")

# Definindo largura das colunas
resultado_tree.column("#", width=30, anchor="center")
resultado_tree.column("Nome", width=250, anchor="w")
resultado_tree.column("Lattes ID", width=150, anchor="center")

# Estilos visuais para melhorar o design
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", font=("Arial", 10), rowheight=25)

# Iniciar a aplicação
root.mainloop()
