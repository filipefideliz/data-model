import pandas as pd
import mysql.connector

# read csv file
df_transaction = pd.read_csv('lake/transacoes.csv')
df_cursos = pd.read_csv('lake/cursos.csv')
df_usuarios = pd.read_csv('lake/usuarios.csv') 

df_cursos.rename(columns={'id': 'id_curso'},inplace=True)
df_usuarios.rename(columns={'id': 'id_usuario'}, inplace=True)

# merge dataframes
fact_table = pd.merge(df_transaction, df_cursos, on='id_curso')
fact_table = pd.merge(fact_table, df_usuarios, on='id_usuario')

# Create dimension tables
#courses_dim = courses_df[['id_curso', 'nome']]
#users_dim = users_df[['id_usuario', 'nome', 'email', 'cpf', 'telefone', 'ano_nascimento', 'mes_nascimento', 'dia_nascimento', 'e_instrutor']]

# connect to MySQL database
conexao = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='test',
    password='test',
    database='test',
    auth_plugin='mysql_native_password'
)

cursor = conexao.cursor()

# create table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS fato_transacoes (id INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, id_curso INT, metodo_pagamento VARCHAR(255), descricao TEXT, nome_curso VARCHAR(255), descricao_curso TEXT, valor_curso DECIMAL(10,2), nome_usuario VARCHAR(255), email VARCHAR(255), cpf VARCHAR(255), telefone VARCHAR(255), ano_nascimento INT, mes_nascimento INT, dia_nascimento INT, e_instrutor BOOLEAN) ENGINE=InnoDB")


for row in fact_table.itertuples():
    cursor.execute(
        f"INSERT INTO fato_transacoes (id_usuario, id_curso, metodo_pagamento, descricao, nome_curso, descricao_curso, valor_curso, nome_usuario, email, cpf, telefone, ano_nascimento, mes_nascimento, dia_nascimento, e_instrutor) VALUES ({row.id_usuario}, {row.id_curso}, '{row.metodo_pagamento}', '{row.descricao_x}', '{row.nome_x}', '{row.descricao_y}', {row.valor}, '{row.nome_y}', '{row.email}', '{row.cpf}', '{row.telefone}', {row.ano_nascimento}, {row.mes_nascimento}, {row.dia_nascimento}, {row.e_instrutor})"
    )

conexao.commit()
cursor.close()