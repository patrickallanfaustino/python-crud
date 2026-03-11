import sqlite3

def conectar():
    """Cria a conexão com o banco de dados SQLite."""
    # Se o arquivo não existir, o SQLite cria automaticamente
    return sqlite3.connect('simulacoes.db')

def criar_tabela():
    """Cria a tabela de simulações se ela não existir."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_sistema TEXT NOT NULL,
            software TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def inserir_simulacao(nome_sistema, software, status):
    """Insere um novo registro de simulação no banco."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO simulacoes (nome_sistema, software, status)
        VALUES (?, ?, ?)
    ''', (nome_sistema, software, status))
    
    conn.commit()
    conn.close()
    print(f"Sucesso: Simulação '{nome_sistema}' registrada!")

# Bloco principal para testar o código
if __name__ == '__main__':
    # 1. Cria a tabela no banco de dados
    criar_tabela()
    
    # 2. Insere alguns dados de teste
    inserir_simulacao("Enzima_Substrato_01", "GROMACS", "Concluído")
    inserir_simulacao("Membrana_Lipidica", "OpenMM", "Em andamento")