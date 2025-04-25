import streamlit as st
import sqlite3
import datetime
import re
import locale
from datetime import datetime

@st.dialog(title="Pesquisa bem-sucedida!", width="small")
def openDialog(a):
    st.write(a)

def fullSql():
    #Conecta ao banco de dados SQLite3.
    with st.spinner(f"Conectando o banco de dados {fileDb}", show_time=True):
        conn = sqlite3.connect(fileDb)
        cursor = conn.cursor()

        #Realiza uma consulta.
        cursor.execute(f"SELECT * FROM '{tableDb}'")
    #Serve para apresentar mensagem genérica 
    #openDialog("Deu certo a pesquisa!")
    return cursor.fetchall()
    
def fragDados():
    #Realiza parser nos dados pesquisados.
    nUnits = len(units)
    for unit in units:
        seq = unit[0]
        name = unit[1]
        datas = unit[2].split('%%&&&&')
        allDados.setdefault(name, [])
        for data in datas: 
            dtSplit = [dt for dt in data.split('$$__@@_@@_##_##_##') if dt != symb]
            nDt = len(dtSplit)
            if nDt > 0:
                listDt = []
                for d, dt in enumerate(dtSplit):
                    dtNew = dt.replace(symb, '').strip()
                    if d == 0:
                        match = re.search(padDat, dtNew)
                        try:
                            if match:
                                dtNew =  match.group(0)
                        except:
                            pass
                    listDt.append(dtNew)
                allDados[name].append(listDt)
    return allDados
    
def dateFormat(dateString):
    dateFormat = "%d/%m/%Y"
    datetimeObj = datetime.strptime(dateString, dateFormat)
    dateObj = datetimeObj.date()
    return dateObj
    
def writeSql():
    nUnits = len(units)
    #Exibe todos os registros na(s) página(s) HMTL.
    st.subheader("Informações no banco de dados")
    st.write(f"Total de unidades : {nUnits}")
    st.divider()
    
    #Exibe dados na tela
    seq = 0
    contGlobal = 0
    contFields = 0 
    for al, dados in allDados.items():
        seq += 1
        name = al
        icon = ':beginner:'
        st.markdown(f"{icon} :red[:blue-background[Unidade {seq}]]")
        icon = ':large_orange_diamond:'
        st.markdown(f"{icon} Denominação : ***{name}***")
        cont = 0 
        nAllDt = 0
        for dado in dados:
            nAllDt += len(dados)
            for d, dt in enumerate(dado):               
                dtNew = dt.replace(symb, '').strip()
                if d == 0:
                    st.html(f"<u>#️⃣ {cont+1}.° lançamento</u>") 
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
            st.html('<br>')
        st.html(f"<u>📙Resumo da unidade</u>") 
        st.markdown(f":sunflower: {cont} lançamentos(s)")
        st.markdown(f":balloon: {nAllDt} campos/dados(s)")
        st.divider()
        contGlobal += cont
        contFields += nAllDt
    st.html('<br>')
    st.html(f"<u>📚 Resumo geral </u>")
    st.markdown(f":beginner: {nUnits} unidade(s) analisadas")
    st.markdown(f":sunflower: {contGlobal} lançamentos(s)")
    st.markdown(f":balloon: {contFields} campos/dados(s)")    
    
def searchElem(unit):
    elemUnit = allDados[unit]
    allElem = {}
    for elem in elemUnit:
        for e, elm in enumerate(elem):
            allElem.setdefault(e, [])
            allElem[e].append(elm)
    return allElem
    
def supplyWindow():
    #Fornece elementos para os widgets na(s) página(s) HTML.
    colOne, colTwo, colThree = st.columns([5,3,3], border=3) #just to highlight these are different cols
    nameKeys = sorted(list(allDados.keys()))
    nameUnits = tuple(nameKeys)
    fDate = "DD/MM/YYYY"
    callOptOne = []
    with st.container():
        with colOne: 
            optionOne = st.selectbox(label=f"📙**Selecione o órgão desejado** (**:blue[{len(nameUnits)}]**)", index=None, 
                                    placeholder="Selecione a unidade de seu interesse.", options=nameUnits, key="one")
        with colTwo:
            if "cal1" not in st.session_state:
                st.session_state.value = "today" 
            if optionOne != "" and optionOne is not None:
                with st.spinner("Wait for it...", show_time=True):
                    returnElem = searchElem(optionOne)
                    callOptOne = returnElem[0]
                    nOptOne = len(callOptOne)
                    if nOptOne > 0:                
                        valCal1 = dateFormat(callOptOne[0])
                        valCal2 = dateFormat(callOptOne[-1])
                    else:
                        callOptOne = []
                        st.rerun()
            else:
                callOptOne = []
                valCal1 = None
                valCal2 = None 
            cal1 = st.date_input(label=":calendar:**Selecione a data inicial**", format=fDate, value=valCal1, min_value=valCal1, 
                                 max_value=valCal2, key="cal1", help="Digite ou escolha a data de início da pesquisa")
        with colThree:
            if "cal2" not in st.session_state:
                st.session_state.value = "today"                
            cal2 = st.date_input(label=":calendar:**Selecione a data final**", format=fDate, value=valCal2, min_value=valCal1, 
                                 max_value="today", key="cal2", help="Digite ou escolha a data de término da pesquisa")
    #st.context.cookies
    #st.context.headers
    #st.context.headers.get_all("pragma")
    #st.write('locale')
    #st.context.locale 
    #st.write('zona')
    #st.context.timezone
    #st.query_params

def main():
    #Define variáveis e chama as funções de impressão na tela e/ou preenhcimento de widgets.
    global symb, elem, padDat, fileDb 
    global tableDb, units, allDados
    symb = '_____'
    elem = ['data', 'categoria', 'fundamento']
    padDat = r'\d{2}/\d{2}/\d{4}'
    fileDb = r'C:\Users\ACER\Desktop\streamlit\bancoDatas.db'
    tableDb = 'bancoDatas'
    allDados = {}
    st.set_page_config(layout="wide", 
                       page_icon="🧊", 
                       initial_sidebar_state="expanded")
    st.get_option("theme.primaryColor")
    st.set_option("client.showErrorDetails", True)
    locale.setlocale(locale.LC_ALL, "de_DE")

    #Pesquisa todo o conteúdo do banco de dados
    units = fullSql()
    nUnits = len(units)
    
    #Fragmenta dados. 
    fragDados()

    # Mostra os resultados na interface Streamlit.
    #writeSql() #exibe na tela os dados do órgão.
    
    #Preenche os dados nos widgets.
    supplyWindow()
    
if __name__ == '__main__':
    #Chama a função iniciadora.
    main()
