import os
import streamlit as st
import camelot
import pandas as pd

# 📌 Configuração do Streamlit
st.title("📄 Extrator de Tabelas de PDF")
st.write("Faça upload de um PDF para extrair tabelas e salvar como CSV.")

# 📌 Upload do arquivo PDF
pdf_file = st.file_uploader("📂 Escolha um arquivo PDF", type="pdf")

if pdf_file:
    # 📌 Salvar temporariamente o arquivo
    file_path = f"temp_{pdf_file.name}"
    with open(file_path, "wb") as f:
        f.write(pdf_file.read())

    # 📌 Definição da área da tabela e colunas
    table_areas = ['65,558,500,298']
    columns = ['65,105,165,230,290,350,385,453']

    # 📌 Ler as tabelas do PDF
    st.write("🔍 Extraindo tabelas... Aguarde.")
    tables = camelot.read_pdf(
        file_path, 
        pages="all",  
        flavor="stream",
        table_areas=table_areas,
        columns=columns,
        strip_text='.\n'
    )

    # 📌 Remover o arquivo temporário
    os.remove(file_path)
