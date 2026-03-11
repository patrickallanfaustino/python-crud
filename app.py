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

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar()
    
    # Se o usuário enviou o formulário com alterações (POST)
    if request.method == 'POST':
        nome = request.form['nome_sistema']
        software = request.form['software']
        status = request.form['status']
        
        # Executa o comando UPDATE no banco de dados
        conn.execute('''
            UPDATE simulacoes 
            SET nome_sistema = ?, software = ?, status = ?
            WHERE id = ?
        ''', (nome, software, status, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    # Se o usuário está apenas acessando a página para ver o formulário (GET)
    else:
        # Busca a simulação específica no banco para preencher a tela
        simulacao = conn.execute('SELECT * FROM simulacoes WHERE id = ?', (id,)).fetchone()
        conn.close()
        return render_template('editar.html', simulacao=simulacao)

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