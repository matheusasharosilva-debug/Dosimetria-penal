import streamlit as st
import pandas as pd
st.title("⚖️ Simulador de Dosimetria da Pena")
st.write("**Calculadora completa da dosimetria penal conforme Art. 68 do CP**")
@st.cache_data
def carregar_dados_embedados():
    dados = [
        ['Art. 121', 'Art. 121', 'Crime Base (Caput)', 'Matar alguém:', 72, 'mês', 240, 'mês', 'seis anos', 'vinte anos'],
        ['', 'V -', 'Crime Base (Caput)', 'para assegurar a execução, a ocultação, a impunidade ou vantagem de outro crime:', 144, 'mês', 360, 'mês', 'doze anos', 'trinta anos'],
        ['', 'X -', 'Crime Base (Caput)', 'nas dependências de instituição de ensino:', 144, 'mês', 360, 'mês', 'doze anos', 'trinta anos'],
        ['', '§ 3', 'Crime Qualificado/Autônomo', 'Se o homicídio é culposo:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 122', 'Art. 122', 'Crime Base (Caput)', 'Induzir ou instigar alguém a suicidar-se ou a praticar automutilação:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 123', 'Art. 123', 'Crime Base (Caput)', 'Matar, sob a influência do estado puerperal, o próprio filho, durante o parto ou logo após:', 24, 'mês', 72, 'mês', 'dois anos', 'seis anos'],
        ['Art. 124', 'Art. 124', 'Crime Base (Caput)', 'Provocar aborto em si mesma ou consentir que outrem lho provoque:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 125', 'Art. 125', 'Crime Base (Caput)', 'Provocar aborto, sem o consentimento da gestante:', 36, 'mês', 120, 'mês', 'três anos', 'dez anos'],
        ['Art. 126', 'Art. 126', 'Crime Base (Caput)', 'Provocar aborto com o consentimento da gestante:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
        ['Art. 129', 'Art. 129', 'Crime Base (Caput)', 'Ofender a integridade corporal ou a saúde de outrem:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['', 'IV -', 'Crime Base (Caput)', 'aceleração de parto:', 12, 'mês', 60, 'mês', 'um ano', 'cinco anos'],
        ['', '§ 6', 'Crime Qualificado/Autônomo', 'Se a lesão é culposa:', 2, 'mês', 2, 'mês', 'dois meses', 'dois meses'],
        ['Art. 130', 'Art. 130', 'Crime Base (Caput)', 'Expor alguém, por meio de relações sexuais ou qualquer ato libidinoso, a contágio de moléstia venérea:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['Art. 131', 'Art. 131', 'Crime Base (Caput)', 'Praticar, com o fim de transmitir a outrem moléstia grave de que está contaminado, ato capaz de produzir o contágio:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
        ['Art. 132', 'Art. 132', 'Crime Base (Caput)', 'Expor a vida ou a saúde de outrem a perigo direto e iminente:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['Art. 133', 'Art. 133', 'Crime Base (Caput)', 'Abandonar pessoa que está sob seu cuidado, guarda, vigilância ou autoridade:', 24, 'mês', 60, 'mês', 'dois anos', 'cinco anos'],
        ['Art. 134', 'Art. 134', 'Crime Base (Caput)', 'Expor ou abandonar recém-nascido, para ocultar desonra própria:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 137', 'Art. 137', 'Crime Base (Caput)', 'Participar de rixa, salvo para separar os contendores:', 15, 'dia', 15, 'dia', 'quinze dias', 'quinze dias'],
        ['Art. 138', 'Art. 138', 'Crime Base (Caput)', 'Caluniar alguém, imputando-lhe falsamente fato definido como crime:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 139', 'Art. 139', 'Crime Base (Caput)', 'Difamar alguém, imputando-lhe fato ofensivo à sua reputação:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['Art. 140', 'Art. 140', 'Crime Base (Caput)', 'Injuriar alguém, ofendendo-lhe a dignidade ou o decoro:', 1, 'mês', 6, 'mês', 'um mês', 'seis meses'],
        ['Art. 147', 'Art. 147', 'Crime Base (Caput)', 'Ameaçar alguém, por palavra, escrito ou gesto, de causar-lhe mal injusto e grave:', 1, 'mês', 6, 'mês', 'um mês', 'seis meses'],
        ['Art. 148', 'Art. 148', 'Crime Base (Caput)', 'Privar alguém de sua liberdade, mediante sequestro ou cárcere privado:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 150', 'Art. 150', 'Crime Base (Caput)', 'Entrar ou permanecer, clandestina ou astuciosamente, em casa alheia:', 1, 'mês', 3, 'mês', 'um mês', 'três meses'],
        ['Art. 151', 'Art. 151', 'Crime Base (Caput)', 'Devassar indevidamente o conteúdo de correspondência fechada, dirigida a outrem:', 1, 'mês', 6, 'mês', 'um mês', 'seis meses'],
        ['Art. 154', 'Art. 154', 'Crime Base (Caput)', 'Revelar alguém, sem justa causa, segredo, de que tem ciência em razão de função:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['Art. 155', 'Art. 155', 'Crime Base (Caput)', 'Subtrair, para si ou para outrem, coisa alheia móvel:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
        ['Art. 156', 'Art. 156', 'Crime Base (Caput)', 'Subtrair o condômino, co-herdeiro ou sócio, para si ou para outrem, a quem legitimamente a detém, a coisa comum:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 160', 'Art. 160', 'Crime Base (Caput)', 'Exigir ou receber, como garantia de dívida, abusando da situação de alguém, documento que pode dar causa a procedimento criminal:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 161', 'Art. 161', 'Crime Base (Caput)', 'Suprimir ou deslocar tapume, marco, ou qualquer outro sinal indicativo de linha divisória:', 1, 'mês', 6, 'mês', 'um mês', 'seis meses'],
        ['Art. 162', 'Art. 162', 'Crime Base (Caput)', 'Suprimir ou alterar, indevidamente, em gado ou rebanho alheio, marca ou sinal indicativo de propriedade:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 163', 'Art. 163', 'Crime Base (Caput)', 'Destruir, inutilizar ou deteriorar coisa alheia:', 1, 'mês', 6, 'mês', 'um mês', 'seis meses'],
        ['Art. 164', 'Art. 164', 'Crime Base (Caput)', 'Introduzir ou deixar animais em propriedade alheia, sem consentimento de quem de direito, desde que o fato resulte prejuízo:', 15, 'dia', 15, 'dia', 'quinze dias', 'quinze dias'],
        ['Art. 165', 'Art. 165', 'Crime Base (Caput)', 'Destruir, inutilizar ou deteriorar coisa tombada pela autoridade competente em virtude de valor artístico, arqueológico ou histórico:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 166', 'Art. 166', 'Crime Base (Caput)', 'Alterar, sem licença da autoridade competente, o aspecto de local especialmente protegido por lei:', 1, 'mês', 12, 'mês', 'um mês', 'um ano'],
        ['Art. 169', 'Art. 169', 'Crime Base (Caput)', 'Apropriar-se alguém de coisa alheia vinda ao seu poder por erro, caso fortuito ou força da natureza:', 15, 'dia', 15, 'dia', 'quinze dias', 'quinze dias'],
        ['Art. 171', 'Art. 171', 'Crime Base (Caput)', 'Obter, para si ou para outrem, vantagem ilícita, em prejuízo alheio, induzindo ou mantendo alguém em erro:', 12, 'mês', 60, 'mês', 'um ano', 'cinco anos'],
        ['Art. 176', 'Art. 176', 'Crime Base (Caput)', 'Tomar refeição em restaurante, alojar-se em hotel ou utilizar-se de meio de transporte sem dispor de recursos para efetuar o pagamento:', 15, 'dia', 15, 'dia', 'quinze dias', 'quinze dias'],
        ['Art. 211', 'Art. 211', 'Crime Base (Caput)', 'Destruir, subtrair ou ocultar cadáver ou parte dele:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 212', 'Art. 212', 'Crime Base (Caput)', 'Vilipendiar cadáver ou suas cinzas:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 215', 'Art. 215', 'Crime Base (Caput)', 'Praticar contra alguém e sem a sua anuência ato libidinoso com o objetivo de satisfazer a própria lascívia ou a de terceiro:', 12, 'mês', 60, 'mês', 'um ano', 'cinco anos'],
        ['Art. 217', 'Art. 217', 'Crime Base (Caput)', 'Ter conjunção carnal ou praticar outro ato libidinoso com menor de 14 anos:', 96, 'mês', 180, 'mês', 'oito anos', 'quinze anos'],
        ['Art. 227', 'Art. 227', 'Crime Base (Caput)', 'Induzir alguém a satisfazer a lascívia de outrem:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 230', 'Art. 230', 'Crime Base (Caput)', 'Tirar proveito da prostituição alheia, participando diretamente de seus lucros ou fazendo-se sustentar, no todo ou em parte, por quem a exerça:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
        ['Art. 233', 'Art. 233', 'Crime Base (Caput)', 'Praticar ato obsceno em lugar público, ou aberto ou exposto ao público:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['Art. 235', 'Art. 235', 'Crime Base (Caput)', 'Contrair alguém, sendo casado, novo casamento:', 24, 'mês', 72, 'mês', 'dois anos', 'seis anos'],
        ['Art. 236', 'Art. 236', 'Crime Base (Caput)', 'Contrair casamento, induzindo em erro essencial o outro contraente, ou ocultando-lhe impedimento que não seja casamento anterior:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 237', 'Art. 237', 'Crime Base (Caput)', 'Contrair casamento, conhecendo a existência de impedimento que lhe cause a nulidade absoluta:', 3, 'mês', 3, 'mês', 'três meses', 'três meses'],
        ['Art. 238', 'Art. 238', 'Crime Base (Caput)', 'Atribuir-se falsamente autoridade para celebração de casamento:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 239', 'Art. 239', 'Crime Base (Caput)', 'Simular casamento mediante engano de outra pessoa:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 241', 'Art. 241', 'Crime Base (Caput)', 'Promover no registro civil a inscrição de nascimento inexistente:', 24, 'mês', 72, 'mês', 'dois anos', 'seis anos'],
        ['Art. 250', 'Art. 250', 'Crime Base (Caput)', 'Causar incêndio, expondo a perigo a vida, a integridade física ou o patrimônio de outrem:', 36, 'mês', 72, 'mês', 'três anos', 'seis anos'],
        ['Art. 252', 'Art. 252', 'Crime Base (Caput)', 'Expor a perigo a vida, a integridade física ou o patrimônio de outrem, usando de gás tóxico ou asfixiante:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
        ['Art. 253', 'Art. 253', 'Crime Base (Caput)', 'Fabricar, fornecer, adquirir, possuir ou transportar, sem licença da autoridade, substância ou engenho explosivo, gás tóxico ou asfixiante:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 267', 'Art. 267', 'Crime Base (Caput)', 'Causar epidemia, mediante a propagação de germes patogênicos:', 120, 'mês', 180, 'mês', 'dez anos', 'quinze anos'],
        ['Art. 270', 'Art. 270', 'Crime Base (Caput)', 'Envenenar água potável, de uso comum ou particular, ou substância alimentícia ou medicinal destinada a consumo:', 120, 'mês', 180, 'mês', 'dez anos', 'quinze anos'],
        ['Art. 273', 'Art. 273', 'Crime Base (Caput)', 'Falsificar, corromper, adulterar ou alterar produto destinado a fins terapêuticos ou medicinais:', 120, 'mês', 180, 'mês', 'dez anos', 'quinze anos'],
        ['Art. 288', 'Art. 288', 'Crime Base (Caput)', 'Associarem-se 3 ou mais pessoas, para o fim específico de cometer crimes:', 12, 'mês', 36, 'mês', 'um ano', 'três anos'],
        ['Art. 289', 'Art. 289', 'Crime Base (Caput)', 'Falsificar, fabricando-a ou alterando-a, moeda metálica ou papel-moeda de curso legal no país ou no estrangeiro:', 36, 'mês', 144, 'mês', 'três anos', 'doze anos'],
        ['Art. 297', 'Art. 297', 'Crime Base (Caput)', 'Falsificar, no todo ou em parte, documento público, ou alterar documento público verdadeiro:', 24, 'mês', 72, 'mês', 'dois anos', 'seis anos'],
        ['Art. 298', 'Art. 298', 'Crime Base (Caput)', 'Falsificar, no todo ou em parte, documento particular ou alterar documento particular verdadeiro:', 12, 'mês', 60, 'mês', 'um ano', 'cinco anos'],
        ['Art. 313', 'Art. 313', 'Crime Base (Caput)', 'Apropriar-se de dinheiro ou qualquer utilidade que, no exercício do cargo, recebeu por erro de outrem:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
        ['Art. 321', 'Art. 321', 'Crime Base (Caput)', 'Patrocinar, direta ou indiretamente, interesse privado perante a administração pública, valendo-se da qualidade de funcionário:', 1, 'mês', 3, 'mês', 'um mês', 'três meses'],
        ['Art. 331', 'Art. 331', 'Crime Base (Caput)', 'Desacatar funcionário público no exercício da função ou em razão dela:', 6, 'mês', 6, 'mês', 'seis meses', 'seis meses'],
        ['Art. 334', 'Art. 334', 'Crime Base (Caput)', 'Iludir, no todo ou em parte, o pagamento de direito ou imposto devido pela entrada, pela saída ou pelo consumo de mercadoria:', 12, 'mês', 48, 'mês', 'um ano', 'quatro anos'],
    ]
    colunas = ['Artigo_Base','Artigo_Completo','Tipo_Penal','Descricao_Crime','Pena_Minima_Valor','Pena_Minima_Unidade','Pena_Maxima_Valor','Pena_Maxima_Unidade','Pena_Minima_Texto','Pena_Maxima_Texto']
    return pd.DataFrame(dados, columns=colunas)
@st.cache_data
def processar_dados_crimes(df):
    crimes_dict = {}
    for idx, row in df.iterrows():
        artigo_completo = row['Artigo_Completo']
        descricao = row['Descricao_Crime']
        pena_min_valor = row['Pena_Minima_Valor']
        pena_min_unidade = row['Pena_Minima_Unidade']
        pena_max_valor = row['Pena_Maxima_Valor']
        pena_max_unidade = row['Pena_Maxima_Unidade']
        tipo_penal = row['Tipo_Penal']
        if pena_min_unidade == 'mês' or pena_min_unidade == 'mese':
            pena_min_anos = pena_min_valor / 12
        elif pena_min_unidade == 'dia':
            pena_min_anos = pena_min_valor / 360
        else:
            pena_min_anos = pena_min_valor
        if pena_max_unidade == 'mês' or pena_max_unidade == 'mese':
            pena_max_anos = pena_max_valor / 12
        elif pena_max_unidade == 'dia':
            pena_max_anos = pena_max_valor / 360
        else:
            pena_max_anos = pena_max_valor
        if pd.notna(artigo_completo) and pd.notna(descricao):
            chave = f"{artigo_completo} - {descricao[:80]}..."
            crimes_dict[chave] = {
                'artigo': artigo_completo,
                'descricao_completa': descricao,
                'pena_min': pena_min_anos,
                'pena_max': pena_max_anos,
                'tipo_penal': tipo_penal
            }
    return crimes_dict
df = carregar_dados_embedados()
crimes_data = processar_dados_crimes(df)
st.sidebar.header("💡 Sobre")
st.sidebar.write("**Base Legal:** Art. 68 do Código Penal - Fases: 1.Pena base 2.Atenuantes/Agravantes 3.Majorantes/Minorantes 4.Cálculo 5.Regime 6.Substituição")
st.sidebar.write(f"**📊 Crimes carregados:** {len(crimes_data)}")
st.sidebar.write("**🔍 Buscar crime:**")
busca = st.sidebar.text_input("Digite o artigo ou descrição:")
if busca:
    crimes_filtrados = {k: v for k, v in crimes_data.items() if busca.lower() in k.lower()}
    st.sidebar.write(f"**Resultados ({len(crimes_filtrados)}):**")
    for chave in list(crimes_filtrados.keys())[:5]:
        crime_info = crimes_filtrados[chave]
        st.sidebar.write(f"**{crime_info['artigo']}** - Pena: {crime_info['pena_min']:.1f}-{crime_info['pena_max']:.1f} anos")
st.header("1️⃣ Fase 1: Pena Base e Circunstâncias")
col1, col2 = st.columns([2, 1])
with col1:
    if crimes_data:
        crime_selecionado = st.selectbox("Selecione o Crime:",options=list(crimes_data.keys()),format_func=lambda x: x)
        crime_info = crimes_data[crime_selecionado]
        min_pena = crime_info['pena_min']
        max_pena = crime_info['pena_max']
        st.write(f"**Artigo:** {crime_info['artigo']}")
        st.write(f"**Tipo penal:** {crime_info['tipo_penal']}")
        st.write(f"**Descrição:** {crime_info['descricao_completa']}")
    else:
        st.error("Erro ao carregar dados dos crimes.")
with col2:
    circunstancia = st.radio("Circunstância do Crime:",["Neutra","Desfavorável","Gravemente Desfavorável"])
    pena_base_inicial = min_pena
    ajuste_circunstancia = {"Neutra": 0,"Desfavorável": 0.2,"Gravemente Desfavorável": 0.4}
    fator_circunstancia = ajuste_circunstancia[circunstancia]
    pena_base_ajustada = pena_base_inicial * (1 + fator_circunstancia)
    st.write(f"**Pena prevista:** {min_pena:.1f} a {max_pena:.1f} anos")
    st.write(f"**Pena base inicial:** {pena_base_inicial:.1f} anos")
    st.write(f"**Circunstância {circunstancia.lower()}:** {fator_circunstancia*100:.0f}%")
    st.success(f"**PENA BASE APÓS CIRCUNSTÂNCIAS: {pena_base_ajustada:.1f} anos**")
st.header("2️⃣ Fase 2: Atenuantes e Agravantes Gerais")
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔽 Atenuantes (Art. 65 CP)")
    atenuantes = st.multiselect("Selecione as atenuantes:",["Réu primário de bons antecedentes","Arrependimento espontâneo","Confissão espontânea","Reparação do dano","Coação moral","Embriaguez acidental","Motivo de relevante valor social/moral"])
with col2:
    st.subheader("🔼 Agravantes (Art. 61 CP)")
    agravantes = st.multiselect("Selecione as agravantes:",["Reincidente específico","Motivo fútil/torpe","Crime contra idoso/doente","Uso de disfarce/emboscada","Abuso de confiança/poder","Racismo/xenofobia","Aumento do dano maliciosamente"])
st.header("3️⃣ Fase 3: Causas de Aumento/Diminuição")
majorantes_minorantes_generico = {"majorantes": ["Uso de arma (1/6 a 1/2)","Violência grave (1/3 a 2/3)","Concurso de 2+ pessoas (1/4 a 1/2)","Restrição à liberdade (1/6 a 1/3)","Abuso de confiança (1/6 a 1/3)"],"minorantes": ["Valor ínfimo (1/6 a 1/3)","Arrependimento posterior (1/6 a 1/3)","Circunstâncias atenuantes não previstas (1/6 a 1/3)"]}
col1, col2 = st.columns(2)
with col1:
    majorantes = st.multiselect("Causas de aumento (majorantes):",majorantes_minorantes_generico["majorantes"])
with col2:
    minorantes = st.multiselect("Causas de diminuição (minorantes):",majorantes_minorantes_generico["minorantes"])
st.header("4️⃣ Fase 4: Cálculo Final da Pena")
if st.button("🎯 Calcular Pena Definitiva", type="primary"):
    pena_calculada = pena_base_ajustada
    st.subheader("📊 Detalhamento do Cálculo")
    calculo_detalhado = f"| Etapa | Valor | Ajuste |\n|-------|-------|---------|\n| **Pena Base Inicial** | {pena_base_inicial:.1f} anos | - |\n| Circunstância {circunstancia} | {pena_base_ajustada:.1f} anos | {fator_circunstancia*100:+.0f}% |\n"
    for i, atenuante in enumerate(atenuantes, 1):
        reducao = pena_base_ajustada * (1/6)
        pena_calculada -= reducao
        calculo_detalhado += f"| Atenuante {i} | {pena_calculada:.1f} anos | -{reducao:.1f} anos |\n"
    for i, agravante in enumerate(agravantes, 1):
        aumento = pena_base_ajustada * (1/6)
        pena_calculada += aumento
        calculo_detalhado += f"| Agravante {i} | {pena_calculada:.1f} anos | +{aumento:.1f} anos |\n"
    for i, majorante in enumerate(majorantes, 1):
        aumento = pena_base_ajustada * (1/4)
        pena_calculada += aumento
        calculo_detalhado += f"| Majorante {i} | {pena_calculada:.1f} anos | +{aumento:.1f} anos |\n"
    for i, minorante in enumerate(minorantes, 1):
        reducao = pena_base_ajustada * (1/4)
        pena_calculada -= reducao
        calculo_detalhado += f"| Minorante {i} | {pena_calculada:.1f} anos | -{reducao:.1f} anos |\n"
    pena_final = max(min_pena, min(max_pena, pena_calculada))
    calculo_detalhado += f"| **LIMITES LEGAIS** | **{pena_final:.1f} anos** | **Ajuste final** |"
    st.markdown(calculo_detalhado)
    st.header("5️⃣ Fase 5: Regime de Cumprimento")
    if pena_final > 8:
        regime = "FECHADO"
        cor_regime = "#ff4444"
        descricao = "Presídio de segurança máxima/média"
    elif pena_final >= 4:
        regime = "SEMIABERTO"
        cor_regime = "#ffaa00"
        descricao = "Colônia agrícola, industrial ou similar"
    else:
        regime = "ABERTO"
        cor_regime = "#44cc44"
        descricao = "Casa de albergado, trabalho externo"
    st.markdown(f"""<div style="background-color: {cor_regime}20; padding: 20px; border-radius: 10px; border-left: 5px solid {cor_regime};"><h2 style="color: {cor_regime}; margin: 0;">🔒 REGIME {regime}</h2><p style="margin: 10px 0 0 0; font-size: 16px;"><strong>{descricao}</strong></p></div>""", unsafe_allow_html=True)
    st.header("6️⃣ Fase 6: Substituição da Pena")
    if pena_final <= 4:
        substituicao = "**CABE SUBSTITUIÇÃO** por pena restritiva de direitos"
        cor_subst = "#44cc44"
        fundamento = "Art. 44 CP - Penas até 4 anos podem ser substituídas"
    else:
        substituicao = "**NÃO CABE SUBSTITUIÇÃO**"
        cor_subst = "#ff4444"
        fundamento = "Art. 44 CP - Penas superiores a 4 anos não podem ser substituídas"
    st.markdown(f"""<div style="background-color: {cor_subst}20; padding: 15px; border-radius: 10px; border-left: 5px solid {cor_subst};"><h3 style="color: {cor_subst}; margin: 0;">{substituicao}</h3><p style="margin: 5px 0 0 0;">{fundamento}</p></div>""", unsafe_allow_html=True)
    st.header("📊 Gráfico da Dosimetria")
    faixa_total = max_pena - min_pena
    if faixa_total > 0:
        pos_base = ((pena_base_inicial - min_pena) / faixa_total) * 100
        pos_ajustada = ((pena_base_ajustada - min_pena) / faixa_total) * 100
        pos_final = ((pena_final - min_pena) / faixa_total) * 100
    else:
        pos_base = pos_ajustada = pos_final = 50
             html_grafico = f"""<div style="background: #f8f9fa; padding: 30px; border-radius: 15px; margin: 20px 0;"><h4 style="text-align: center; margin-bottom: 30px;">Evolução da Dosimetria da Pena</h4><div style="position: relative; height: 120px; background: linear-gradient(90deg, #d4f8d4 0%, #fff9c4 50%, #ffcdd2 100%); border-radius: 10px; border: 2px solid #dee2e6; margin-bottom: 60px;"><div style="position: absolute; left: {pos_base}%; top: 0; bottom: 0; width: 3px; background: #007bff; transform: translateX(-50%);"><div style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); white-space: nowrap; background: white; padding: 2px 8px; border-radius: 10px; border: 1px solid #007bff; font-size: 12px; font-weight: bold; color: #007bff;">⚖️ Base: {pena_base_inicial:.1f} anos</div></div><div style="position: absolute; left: {pos_ajustada}%; top: 0; bottom: 0; width: 3px; background: #6f42c1; transform: translateX(-50%);"><div style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); white-space: nowrap; background: white; padding: 2px 8px; border-radius: 10px; border: 1px solid #6f42c1; font-size: 12px; font-weight: bold; color: #6f42c1;">📈 Ajustada: {pena_base_ajustada:.1f} anos</div></div><div style="position: absolute; left: {pos_final}%; top: 0; bottom: 0; width: 4px; background: #dc3545; transform: translateX(-50%);"><div style="position: absolute; bottom: -35px; left: 50%; transform: translateX(-50%); white-space: nowrap; background: white; padding: 2px 8px; border-radius: 10px; border: 1px solid #dc3545; font-size: 12px; font-weight: bold; color: #dc3545;">🎯 Final: {pena_final:.1f} anos</div></div></div><div style="display: flex; justify-content: space-between; margin-top: 20px;"><div style="text-align: center;"><div style="background: #d4f8d4; padding: 10px; border-radius: 5px; border: 1px solid #44cc44;"><strong>🔓 ABERTO</strong><br><small>Até 4 anos</small></div></div><div style="text-align: center;"><div style="background: #fff9c4; padding: 10px; border-radius: 5px; border: 1px solid #ffaa00;"><strong>🔐 SEMIABERTO</strong><br><small>4 a 8 anos</small></div></div><div style="text-align: center;"><div style="background: #ffcdd2; padding: 10px; border-radius: 5px; border: 1px solid #ff4444;"><strong>🔒 FECHADO</strong><br><small>Acima de 8 anos</small></div></div></div></div>"""
    st.markdown(html_grafico, unsafe_allow_html=True)
    st.success(f"**RESUMO FINAL:** Pena de {pena_final:.1f} anos - Regime {regime} - {substituicao}")
st.header("📋 Tabela de Referência")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("📊 Regimes")
    st.table(pd.DataFrame([{"Pena":"Até 4 anos","Regime":"Aberto"},{"Pena":"4 a 8 anos","Regime":"Semiaberto"},{"Pena":"Acima de 8 anos","Regime":"Fechado"}]))
with col2:
    st.subheader("⚖️ Fatores")
    st.table(pd.DataFrame([{"Fator":"Atenuante","Ajuste":"-1/6"},{"Fator":"Agravante","Ajuste":"+1/6"},{"Fator":"Majorante","Ajuste":"+1/6 a +1/2"},{"Fator":"Minorante","Ajuste":"-1/6 a -1/3"}]))
with col3:
    st.subheader("🔀 Substituição")
    st.table(pd.DataFrame([{"Condição":"Pena ≤ 4 anos","Substitui":"Sim"},{"Condição":"Pena > 4 anos","Substitui":"Não"},{"Condição":"Réu reincidente","Substitui":"Restrita"}]))
st.markdown("---")
st.write("**⚖️ Ferramenta educacional - Consulte sempre a legislação atual e um profissional do direito**")
st.write("**📚 Base legal:** Arts. 59, 61, 65, 68 do Código Penal Brasileiro")
