import sqlite3
import os

# Define o caminho para o arquivo do banco de dados na pasta 'data'
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'homologacao.db')

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados SQLite.
    Cria o arquivo do banco de dados se ele não existir.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Isso permite acessar colunas como dicionários
    return conn

def create_tables():
    """
    Cria as tabelas de Pacientes, Medicos e Atestados se elas não existirem.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela Pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            cpf TEXT UNIQUE,
            cargo TEXT,
            empresa TEXT
        )
    ''')

    # Tabela Medicos (com 'tipo_crm')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            tipo_crm TEXT NOT NULL DEFAULT 'CRM',
            crm TEXT UNIQUE,
            uf_crm TEXT
        )
    ''')

    # Tabela Atestados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atestados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            medico_id INTEGER,
            data_atestado TEXT NOT NULL,
            qtd_dias_atestado INTEGER NOT NULL,
            codigo_cid TEXT NOT NULL,
            data_homologacao TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES medicos(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print(f"Banco de dados criado em: {DB_FILE}")
    print("Tabelas 'pacientes', 'medicos' e 'atestados' verificadas/criadas.")