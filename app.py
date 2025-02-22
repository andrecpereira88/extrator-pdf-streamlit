import os
import streamlit as st
import camelot
import pandas as pd
from PyPDF2 import PdfReader

# 📌 Configuração da página
st.title("📄 Extrator de Tabelas de PDF")
st.write("Faça upload de um PDF e extraia as tabelas para CSV.")

# 📌 Upload do arquivo pelo usuário
pdf_file = st.file_uploader("📂 Escolha um arquivo PDF", type="pdf")

# 📌 Definição da área da tabela e colunas (sem espaços extras)
table_areas = ['65,558,500,298']  # Área exata da tabela
columns = ['65,105,165,230,290,350,385,453']  # Posicionamento das colunas

# 📌 Lendo as tabelas do PDF
print("🔍 Extraindo tabelas do PDF...")
tables = camelot.read_pdf(
    pages='1-30',
    flavor='stream',
    table_areas=table_areas,
    columns=columns,
    strip_text='.\n'
)

# 📌 Verificar quantas tabelas foram encontradas
print(f"✅ Total de tabelas detectadas: {tables.n}")

if tables.n > 0:
    # 📌 Criar um DataFrame e concatenar todas as tabelas extraídas
    df_list = [table.df for table in tables]
    df_final = pd.concat(df_list, ignore_index=True)  

    # 📌 Remover duplicatas
    df_final = df_final.drop_duplicates()

    # 📌 Definir a linha correta como cabeçalho (índice)
    header_row = 0  # 🔄 Se o cabeçalho real estiver em outra linha, ajuste aqui!
    df_final.columns = df_final.iloc[header_row]  # Define a primeira linha como cabeçalho
    df_final = df_final[1:].reset_index(drop=True)  # Remove a linha duplicada

    # 📌 Definir índice como "C&V" (ou outra coluna chave)
    df_final.set_index("C&V", inplace=True)

    # 📌 Salvar os dados extraídos em um arquivo CSV
    output_csv = "tabelas_processadas.csv"
    df_final.to_csv(output_csv, index=True, encoding="utf-8")
    print(f"📁 Arquivo CSV salvo em: {output_csv}")

    # 📌 Exibir um exemplo do DataFrame processado
    print("📝 Primeiras linhas da tabela após processamento:")
    print(df_final.head())

    # 📌 Plotar a detecção da tabela para conferir o posicionamento
    #fig = camelot.plot(tables[0], kind="contour")  
    #plt.show()

else:
    print("❌ Nenhuma tabela detectada no PDF.")
