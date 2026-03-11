from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    conn = sqlite3.connect('simulacoes.db')
    conn.row_factory = sqlite3.Row # Permite acessar as colunas pelo nome
    return conn

def criar_tabela():
    conn = conectar()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS simulacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_sistema TEXT NOT NULL,
            software TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Rotas da Aplicação Web ---

@app.route('/')
def index():
    """A Rota principal: Lê os dados (READ) e renderiza a página HTML."""
    conn = conectar()
    simulacoes = conn.execute('SELECT * FROM simulacoes').fetchall()
    conn.close()
    return render_template('index.html', simulacoes=simulacoes)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    """Rota para processar o formulário de criação (CREATE)."""
    nome = request.form['nome_sistema']
    software = request.form['software']
    status = request.form['status']
    
    conn = conectar()
    conn.execute('INSERT INTO simulacoes (nome_sistema, software, status) VALUES (?, ?, ?)', 
                 (nome, software, status))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    """Rota para deletar um registro (DELETE)."""
    conn = conectar()
    conn.execute('DELETE FROM simulacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    criar_tabela()
    # Inicia o servidor web no modo de desenvolvimento
    app.run(debug=True)