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
