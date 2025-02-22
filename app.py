import os
import camelot
import pandas as pd
import streamlit as st

# 📌 Configuração da página
st.title("📄 Extrator de Tabelas de PDF")
st.write("Faça upload de um PDF e extraia as tabelas para CSV.")

# 📌 Upload do arquivo pelo usuário
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
    st.write("🔍 Extraindo tabelas... Aguarde um momento.")
    tables = camelot.read_pdf(
        file_path, 
        pages="1-30",
        flavor="stream",
        table_areas=table_areas,
        columns=columns,
        strip_text='.\n'
    )

    # 📌 Verificar se há tabelas detectadas
    if tables.n > 0:
        df_list = [table.df for table in tables]
        df_final = pd.concat(df_list, ignore_index=True)  

        # 📌 Remover duplicatas
        df_final = df_final.drop_duplicates()

        # 📌 Definir a linha correta como cabeçalho (índice)
        header_row = 0
        df_final.columns = df_final.iloc[header_row]  
        df_final = df_final[1:].reset_index(drop=True)  

        # 📌 Definir índice como "C&V" (ou outra coluna chave)
        if "C&V" in df_final.columns:
            df_final.set_index("C&V", inplace=True)

        # 📌 Exibir DataFrame no Streamlit
        st.write("📝 Tabela extraída:")
        st.dataframe(df_final)

        # 📌 Criar arquivo CSV para download
        output_csv = "tabelas_processadas.csv"
        df_final.to_csv(output_csv, index=True, encoding="utf-8")

        # 📌 Botão para baixar o CSV
        with open(output_csv, "rb") as f:
            st.download_button("📥 Baixar CSV", f, file_name="tabelas_processadas.csv")

    else:
        st.write("❌ Nenhuma tabela detectada.")

    # 📌 Remover o arquivo temporário
    os.remove(file_path)
