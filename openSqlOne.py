import streamlit as st
import sqlite3
import re

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('bancoDatas.db')
cursor = conn.cursor()

# Realiza uma consulta
cursor.execute("SELECT * FROM 'bancoDatas'")
units = cursor.fetchall()
nUnits = len(units)

# Mostra os resultados na interface Streamlit
st.subheader("Informações no banco de dados")
st.write(f"Total de unidades : {nUnits}")
st.divider()
symb = '_____'
elem = ['data', 'categoria', 'fundamento']
padDat = r'\d{2}/\d{2}/\d{4}'

for unit in units:
    seq = unit[0]
    name = unit[1]
    datas = unit[2].split('%%&&&&')
    icon = ':beginner:'
    st.markdown(f"{icon} :red[:blue-background[Unidade {seq}]]")
    icon = ':large_orange_diamond:'
    st.markdown(f"{icon} Denominação : ***{name}***")
    nAllDt = 0
    cont = 0 
    for data in datas: 
        dtSplit = [dt for dt in data.split('$$__@@_@@_##_##_##') if dt != symb]
        nDt = len(dtSplit)
        if nDt > 0:
            nAllDt += nDt
            for d, dt in enumerate(dtSplit):
                dtNew = dt.replace(symb, '').strip()
                if d == 0:
                    st.html(f"<u>#️⃣ {cont+1}.° lançamento</u>") #
                    cont += 1
                    match = re.search(padDat, dtNew)
                    try:
                        if match:
                            dtNew =  match.group(0)
                    except:
                        pass
                match d:
                    case 0:
                        icon = ':calendar:'
                    case 1:
                        icon = ':newspaper:'                
                    case _:
                        icon = ':closed_book:' 
                st.markdown(f"{icon} **:blue[{elem[d]}]**: {dtNew}")
        st.text('')
    st.markdown(f":sunflower: {cont} lançamentos(s)")
    st.markdown(f":balloon: {nAllDt} campos/dados(s)")
    st.divider()
