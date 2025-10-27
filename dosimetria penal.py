
import streamlit as st
import matplotlib.pyplot as plt

# Configuração
st.set_page_config(page_title="Dosimetria da Pena", page_icon="⚖️")

# Título
st.title("⚖️ Simulador de Dosimetria da Pena")
st.write("**Calculadora da dosimetria penal conforme Art. 68 do CP**")

# Sidebar com informações
st.sidebar.header("💡 Sobre")
st.sidebar.write("""
**Base Legal:**
- Art. 68 do Código Penal
- Regime fechado: > 8 anos
- Regime semiaberto: 4-8 anos
- Regime aberto: < 4 anos
""")

# Fase 1: Pena Base
st.header("1️⃣ Pena Base")

crime = st.selectbox("Tipo de Crime:", [
    "Roubo (Art. 157)",
    "Furto (Art. 155)",
    "Estelionato (Art. 171)",
    "Lesão Corporal (Art. 129)",
    "Homicídio (Art. 121)"
])

# Define pena mínima e máxima baseada no crime
penas = {
    "Roubo (Art. 157)": {"min": 4, "max": 10},
    "Furto (Art. 155)": {"min": 1, "max": 4},
    "Estelionato (Art. 171)": {"min": 1, "max": 5},
    "Lesão Corporal (Art. 129)": {"min": 3, "max": 8},
    "Homicídio (Art. 121)": {"min": 6, "max": 20}
}

min_pena = penas[crime]["min"]
max_pena = penas[crime]["max"]

st.write(f"Pena prevista: **{min_pena} a {max_pena} anos**")

# Fase 2: Atenuantes e Agravantes
st.header("2️⃣ Circunstâncias")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔽 Atenuantes")
    atenuantes = st.multiselect(
        "Selecione as atenuantes:",
        ["Réu primário", "Boa conduta social", "Confissão espontânea",
         "Reparação do dano", "Coação moral", "Embriaguez acidental"]
    )

with col2:
    st.subheader("🔼 Agravantes")
    agravantes = st.multiselect(
        "Selecione as agravantes:",
        ["Réu reincidente", "Motive fútil", "Crime contra idoso",
         "Uso de arma", "Abuso de confiança", "Racismo"]
    )

# Fase 3: Cálculo
st.header("3️⃣ Cálculo da Pena")

if st.button("🎯 Calcular Pena Final"):
    # Pena base (média)
    pena_base = (min_pena + max_pena) / 2

    # Ajustes por circunstâncias
    ajuste = 0

    # Cada atenuante reduz 1/6 da pena
    for atenuante in atenuantes:
        ajuste -= pena_base * (1/6)

    # Cada agravante aumenta 1/6 da pena
    for agravante in agravantes:
        ajuste += pena_base * (1/6)

    pena_final = pena_base + ajuste

    # Limites legais
    pena_final = max(min_pena, min(max_pena, pena_final))

    # Resultado
    st.success(f"**PENA FINAL: {pena_final:.1f} ANOS**")

    # Determinar regime
    if pena_final > 8:
        regime = "🔒 REGIME FECHADO"
        cor = "red"
    elif pena_final >= 4:
        regime = "🔐 REGIME SEMIABERTO"
        cor = "orange"
    else:
        regime = "🔑 REGIME ABERTO"
        cor = "green"

    st.markdown(f"<h3 style='color: {cor}'>{regime}</h3>", unsafe_allow_html=True)

    # Gráfico
    st.subheader("📊 Dosimetria da Pena")

    fig, ax = plt.subplots(figsize=(10, 6))

    categorias = ['Pena Mínima', 'Pena Base', 'Pena Final', 'Pena Máxima']
    valores = [min_pena, pena_base, pena_final, max_pena]
    cores = ['lightblue', 'blue', 'red', 'lightcoral']

    bars = ax.bar(categorias, valores, color=cores)
    ax.set_ylabel('Anos de Pena')
    ax.set_title('Evolução da Dosimetria')

    # Adicionar valores nas barras
    for bar, valor in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{valor:.1f} anos', ha='center', va='bottom')

    st.pyplot(fig)

# Tabela de referência
st.header("📋 Tabela de Regimes")

regimes = [
    {"Pena": "Até 4 anos", "Regime": "Aberto", "Características": "Albergado, trabalho externo"},
    {"Pena": "4 a 8 anos", "Regime": "Semiaberto", "Características": "Colônia agrícola, industrial"},
    {"Pena": "Acima de 8 anos", "Regime": "Fechado", "Características": "Presídio de segurança"}
]

st.table(regimes)

# Material de estudo
with st.expander("📚 Fundamentação Legal"):
    st.write("""
    **Art. 68 CP - Critérios para dosimetria:**
    1. Pena base conforme crime
    2. Atenuantes (reduzem 1/6 cada)
    3. Agravantes (aumentam 1/6 cada)
    4. Majorantes e minorantes

    **Regimes:**
    - Fechado: pena > 8 anos
    - Semiaberto: pena 4-8 anos
    - Aberto: pena < 4 anos
    """)
    # Pode adicionar consulta a APIs jurídicas
st.sidebar.header("📖 Jurisprudência")
st.sidebar.write("""
**Súmulas relevantes:**
- STF Súmula 715
- STJ Súmula 341
""")


# Rodapé
st.markdown("---")
st.write("**GitHub:** github.com/seu-usuario/dosimetria-penal")
st.write("*Ferramenta educacional - Consulte sempre a legislação atual*")
st.write("**🌐 Fontes Oficiais:**")
st.write("[Código Penal](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm) | [Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm)")
