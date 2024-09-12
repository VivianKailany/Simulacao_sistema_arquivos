class INode:
    def __init__(self, nome, pasta=False):
        self.nome = nome
        self.tamanho = 0
        self.pasta = pasta
        self.ponteiros = []  # Lista de ponteiros para blocos de dados
        self.filhos = {} if pasta else None

class SistemaDeArquivos:
    def __init__(self):
        # Criação do diretório raiz
        self.raiz = INode("C:\\", pasta=True)
        self.pasta_atual = self.raiz
        self.historico_diretorios = []  # Pilha de diretórios anteriores
        self.blocos_de_dados = {}  # Dicionário para armazenar blocos de dados
        self.proximo_indice_bloco = 0  # Índice para novos blocos de dados

    def listar_pasta(self):
        if len(self.pasta_atual.filhos) == 0:
            print("Pasta vazia.")
            return
        
        print("Conteúdo da pasta atual:")
        for nome, inode in self.pasta_atual.filhos.items():
            tipo = "Pasta" if inode.pasta else "Arquivo"
            print(f"{tipo} -> {nome}")

    def criar(self, nome, pasta=False):
        if nome in self.pasta_atual.filhos:
            print(f"{nome} já existe!")
            return
        
        inode = INode(nome, pasta=pasta)
        self.pasta_atual.filhos[nome] = inode
        print(f"{'Pasta' if pasta else 'Arquivo'} '{nome}' criada.")

    def mudar_pasta(self, nome):
        if nome == "..":
            if self.pasta_atual == self.raiz:
                print("Você já está no diretório raiz.")
            else:
                self.pasta_atual = self.historico_diretorios.pop()
                print("Você voltou para a pasta:", self.pasta_atual.nome)
        elif nome == ".":
            print("Você já está no diretório atual.")
        elif nome in self.pasta_atual.filhos and self.pasta_atual.filhos[nome].pasta:
            self.historico_diretorios.append(self.pasta_atual)
            self.pasta_atual = self.pasta_atual.filhos[nome]
            print("Você entrou no diretório:", self.pasta_atual.nome)
        else:
            print(f"{nome} não é um diretório válido.")

    def mover(self, nome_arquivo, nome_diretorio_alvo):
        if nome_arquivo not in self.pasta_atual.filhos:
            print(f"{nome_arquivo} não encontrado.")
            return
        
        if nome_diretorio_alvo not in self.pasta_atual.filhos or not self.pasta_atual.filhos[nome_diretorio_alvo].pasta:
            print(f"{nome_diretorio_alvo} não é um diretório válido.")
            return
        
        inode_arquivo = self.pasta_atual.filhos.pop(nome_arquivo)
        self.pasta_atual.filhos[nome_diretorio_alvo].filhos[nome_arquivo] = inode_arquivo
        print(f"Arquivo '{nome_arquivo}' movido para '{nome_diretorio_alvo}'.")

    def escrever_arquivo(self, nome_arquivo, dados):
        if nome_arquivo not in self.pasta_atual.filhos or self.pasta_atual.filhos[nome_arquivo].pasta:
            print(f"{nome_arquivo} não é um arquivo válido.")
            return
        
        inode = self.pasta_atual.filhos[nome_arquivo]
        
        tamanho_bloco = len(dados)
        endereco_bloco = self.proximo_indice_bloco
        self.blocos_de_dados[endereco_bloco] = dados
        inode.ponteiros.append(endereco_bloco)
        inode.tamanho += tamanho_bloco
        self.proximo_indice_bloco += 1
        print(f"Dados escritos no arquivo '{nome_arquivo}'.")

    def ler_arquivo(self, nome_arquivo):
        if nome_arquivo not in self.pasta_atual.filhos or self.pasta_atual.filhos[nome_arquivo].pasta:
            print(f"{nome_arquivo} não é um arquivo válido.")
            return
        
        inode = self.pasta_atual.filhos[nome_arquivo]
        print(f"Conteúdo do arquivo '{nome_arquivo}':")
        for ponteiro in inode.ponteiros:
            if ponteiro in self.blocos_de_dados:
                print(self.blocos_de_dados[ponteiro])

    def deletar(self, nome):
        if nome not in self.pasta_atual.filhos:
            print(f"{nome} não encontrado.")
            return
        
        inode = self.pasta_atual.filhos[nome]
        
        if inode.pasta and inode.filhos:
            print(f"Diretório '{nome}' não está vazio.")
            return
        
        # liberar os blocos de dados
        if not inode.pasta:
            for ponteiro in inode.ponteiros:
                if ponteiro in self.blocos_de_dados:
                    del self.blocos_de_dados[ponteiro]
            inode.ponteiros.clear()  # Limpa a lista de ponteiros após liberar os blocos
        
        # Remover a entrada da pasta
        del self.pasta_atual.filhos[nome]
        print(f"{'Diretório' if inode.pasta else 'Arquivo'} '{nome}' excluído.")


fs = SistemaDeArquivos()

fs.listar_pasta()


fs.criar("Sistemas Operacionais", pasta=True)
fs.criar("inodes.txt")
fs.listar_pasta()



fs.mudar_pasta("Sistemas Operacionais")
fs.criar("word.doc")
fs.listar_pasta()
fs.mudar_pasta("..")
fs.listar_pasta()


fs.mover("inodes.txt", "Sistemas Operacionais")
fs.mudar_pasta("Sistemas Operacionais")
fs.listar_pasta()


fs.escrever_arquivo("inodes.txt", "Um inode é basicamente uma estrutura de dados, pré-definida e que tem por papel armazenar metadados de cada arquivo e diretório do sistema de arquivos usados pelos sistemas operacionais oriundos do Unix.")
fs.ler_arquivo("inodes.txt")
fs.listar_pasta()

# Exclusão de arquivos e pastas
fs.deletar("word.doc")
fs.listar_pasta()
fs.deletar("inodes.txt")
fs.listar_pasta()
fs.mudar_pasta("..")
fs.listar_pasta()
fs.deletar("Sistemas Operacionais")


fs.listar_pasta()
fs.ler_arquivo("inodes.txt")
fs.mudar_pasta("..")
fs.mudar_pasta(".")