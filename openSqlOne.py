import streamlit as st
import sqlite3

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('bancoDatas.db')
cursor = conn.cursor()

# Realiza uma consulta
cursor.execute("SELECT * FROM 'bancoDatas'")
units = cursor.fetchall()

# Mostra os resultados na interface Streamlit
st.subheader("Informações no banco de dados")
st.write("Unidades:")
for unit in units:
    st.write(len(unit))
    st.write(f" - {unit[0]}")
    st.write(f" - {unit[1]}")
    st.write(f" - {unit[2]}")
