import tkinter as tk
from tkinter import messagebox

# --- Documentação do Código ---
# Jogo da Velha com GUI (Tkinter), utilizando uma estrutura de matriz (lista de listas)
# para representar o tabuleiro (tabuleiro[linha][coluna]).

class TicTacToeMatrizApp:
    """
    Classe principal para o Jogo da Velha com GUI.
    Utiliza uma matriz 3x3 para o tabuleiro.
    """
    def __init__(self, master):
        self.master = master
        master.title("Jogo da Velha (Matriz 3x3)")
        
        # 1. Configuração do Estado do Jogo
        self.tabuleiro = self._inicializar_tabuleiro() # Matriz 3x3
        self.jogador_atual = 'X'
        self.jogo_ativo = True
        
        # 2. Configuração da Interface
        self.botoes = {} # Dicionário para armazenar os botões, chave: (linha, coluna)
        self.criar_widgets()

    def _inicializar_tabuleiro(self):
        """ Inicializa o tabuleiro como uma matriz 3x3 com espaços. """
        return [[" " for _ in range(3)] for _ in range(3)]

    def criar_widgets(self):
        """ Cria e posiciona todos os elementos da interface (rótulos e botões). """

        # Rótulo de Mensagem
        self.label_mensagem = tk.Label(self.master, text=f"Vez do Jogador {self.jogador_atual}", font=('Arial', 14, 'bold'))
        self.label_mensagem.grid(row=0, column=0, columnspan=3, pady=10)

        # Criação dos Botões do Tabuleiro
        for linha in range(3):
            for coluna in range(3):
                # Usamos lambda com argumentos fixos para garantir que 'l' e 'c' capturem os valores corretos
                botao = tk.Button(self.master, 
                                    text=' ', 
                                    font=('Arial', 24, 'bold'), 
                                    width=5, 
                                    height=2,
                                    bg="#f9bc04",
                                    command=lambda l=linha, c=coluna: self.fazer_jogada(l, c))
                
                # O grid começa na linha 1, pois a linha 0 é o label_mensagem
                botao.grid(row=linha + 1, column=coluna, padx=5, pady=5) 
                self.botoes[(linha, coluna)] = botao
            
        # Botão de Reiniciar Jogo
        self.botao_reiniciar = tk.Button(self.master, 
                                         text="Reiniciar Jogo", 
                                         font=('Arial', 14),
                                         command=self.reiniciar_jogo)
        self.botao_reiniciar.grid(row=5, column=0, columnspan=3, pady=20)


    def fazer_jogada(self, linha, coluna):
        """ 
        Executada quando um botão é clicado. Processa a jogada usando linha e coluna.
        """
        if self.jogo_ativo and self.tabuleiro[linha][coluna] == ' ':
            # 1. Atualiza o estado do jogo (matriz) e a interface (botão)
            self.tabuleiro[linha][coluna] = self.jogador_atual
            
            # Obtém o botão pelo dicionário de botões
            botao_clicado = self.botoes[(linha, coluna)] 
            botao_clicado['text'] = self.jogador_atual
            
            # Define a cor do texto
            cor = 'blue' if self.jogador_atual == 'X' else 'red'
            botao_clicado['fg'] = cor 

            # 2. Verifica as condições de fim de jogo
            if self._verificar_vitoria(self.jogador_atual):
                self.label_mensagem.config(text=f"Parabéns! O jogador {self.jogador_atual} VENCEU!")
                self.jogo_ativo = False
                self._desabilitar_botoes()
            elif self._verificar_empate():
                self.label_mensagem.config(text="O jogo terminou em EMPATE!")
                self.jogo_ativo = False
            else:
                # 3. Troca o jogador
                self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
                self.label_mensagem.config(text=f"Vez do Jogador {self.jogador_atual}")

    
    def _verificar_vitoria(self, jogador):
        """ Verifica se o jogador atual venceu, usando a lógica da matriz 3x3. """
        
        # Verifica linhas e colunas (Lógica do código original)
        for i in range(3):
            # Linhas
            if all([celula == jogador for celula in self.tabuleiro[i]]):
                self._destacar_vitoria([(i, c) for c in range(3)])
                return True
            # Colunas
            if all([self.tabuleiro[j][i] == jogador for j in range(3)]):
                self._destacar_vitoria([(r, i) for r in range(3)])
                return True
                
        # Verifica diagonais
        diag_principal = all([self.tabuleiro[i][i] == jogador for i in range(3)])
        if diag_principal:
            self._destacar_vitoria([(i, i) for i in range(3)])
            return True
        
        diag_secundaria = all([self.tabuleiro[i][2 - i] == jogador for i in range(3)])
        if diag_secundaria:
            self._destacar_vitoria([(i, 2 - i) for i in range(3)])
            return True
            
        return False
        
    def _verificar_empate(self):
        """ Verifica se o jogo terminou em empate. """
        # Verifica se todas as células da matriz estão preenchidas
        return all(cell != " " for row in self.tabuleiro for cell in row)
        
    def _desabilitar_botoes(self):
        """ Desabilita todos os botões após o fim do jogo. """
        for botao in self.botoes.values():
            botao.config(state=tk.DISABLED)

    def _destacar_vitoria(self, coordenadas_vencedoras):
        """ Altera a cor dos botões que formaram a combinação vencedora. """
        for linha, coluna in coordenadas_vencedoras:
            self.botoes[(linha, coluna)].config(bg='lightgreen')

    def reiniciar_jogo(self):
        """ Redefine o estado do jogo e a interface para um novo jogo. """
        self.tabuleiro = self._inicializar_tabuleiro()
        self.jogador_atual = 'X'
        self.jogo_ativo = True
        
        # Resetar a aparência e o estado dos botões
        for (linha, coluna), botao in self.botoes.items():
            botao.config(text=' ', 
                         state=tk.NORMAL, 
                         bg="#575702", 
                         fg='black') 
            
        self.label_mensagem.config(text=f"Vez do Jogador {self.jogador_atual}")


if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeMatrizApp(root)
    root.mainloop()