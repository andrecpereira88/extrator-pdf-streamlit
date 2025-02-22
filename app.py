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

if pdf_file:
    # 📌 Salvar temporariamente o arquivo
    file_path = f"temp_{pdf_file.name}"
    with open(file_path, "wb") as f:
        f.write(pdf_file.read())

    # 📌 Verificar se o PDF é válido
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            num_paginas = len(reader.pages)

        st.write(f"📄 O PDF tem {num_paginas} páginas.")
        
    except Exception as e:
        st.error("❌ Erro ao abrir o PDF. Verifique se o arquivo não está corrompido.")
        os.remove(file_path)
        st.stop()

    # 📌 Tentativa de extração
    st.write("🔍 Extraindo tabelas...")

    try:
        # 📌 Extração SEM `table_areas` primeiro
        tables = camelot.read_pdf(
            file_path, 
            pages="all",  
            flavor="stream",
            strip_text='.\n'
        )

        # 📌 Se nenhuma tabela for encontrada, tenta com `table_areas`
        if tables.n == 0:
            st.write("⚠ Nenhuma tabela detectada com configuração padrão. Tentando com `table_areas`...")
            table_areas = ['65,558,500,298']
            columns = ['65,105,165,230,290,350,385,453']

            tables = camelot.read_pdf(
                file_path, 
                pages="all",
                flavor="stream",
                table_areas=table_areas,
                columns=columns,
                strip_text='.\n'
            )

        # 📌 Verificar se há tabelas detectadas
        if tables.n > 0:
            df_list = [table.df for table in tables]
            df_final = pd.concat(df_list, ignore_index=True)  
            df_final = df_final.drop_duplicates()

            # 📌 Definir cabeçalho correto e corrigir colunas duplicadas
            df_final.columns = df_final.iloc[0]  
            df_final = df_final[1:].reset_index(drop=True)  
            df_final.columns = [f"{col}_{i}" if col == "" else col for i, col in enumerate(df_final.columns)]

            # 📌 Definir índice como "C&V" (se existir)
            if "C&V" in df_final.columns:
                df_final.set_index("C&V", inplace=True)

            # 📌 Exibir DataFrame no Streamlit
            st.write("📝 Tabela extraída:")
            st.dataframe(df_final)

            # 📌 Criar CSV para download
            output_csv = "tabelas_processadas.csv"
            df_final.to_csv(output_csv, index=True, encoding="utf-8")

            with open(output_csv, "rb") as f:
                st.download_button("📥 Baixar CSV", f, file_name="tabelas_processadas.csv")

        else:
            st.write("❌ Nenhuma tabela detectada.")

    except Exception as e:
        st.error(f"⚠️ Erro ao extrair tabelas: {e}")

    # 📌 Remover o arquivo temporário
    os.remove(file_path)
