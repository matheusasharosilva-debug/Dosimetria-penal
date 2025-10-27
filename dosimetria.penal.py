import streamlit as st
import math

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

    # 📊 GRÁFICO VISUAL COM HTML/CSS
    st.subheader("📊 Dosimetria da Pena - Gráfico Visual")
    
    # Calcular porcentagens para o gráfico
    faixa_total = max_pena - min_pena
    pos_base = ((pena_base - min_pena) / faixa_total) * 100 if faixa_total > 0 else 50
    pos_final = ((pena_final - min_pena) / faixa_total) * 100 if faixa_total > 0 else 50
    
    # Criar gráfico com HTML/CSS
    st.markdown(f"""
    <div style="background: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <div style="position: relative; height: 80px; background: linear-gradient(90deg, #d4f8d4 0%, #fff9c4 50%, #ffcdd2 100%); border-radius: 10px; border: 2px solid #ccc;">
            <!-- Linha da Pena Base -->
            <div style="position: absolute; left: {pos_base}%; top: 0; bottom: 0; width: 4px; background: blue; transform: translateX(-50%);">
                <div style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); white-space: nowrap; font-weight: bold; color: blue;">
                    ⚖️ Base: {pena_base:.1f} anos
                </div>
            </div>
            
            <!-- Linha da Pena Final -->
            <div style="position: absolute; left: {pos_final}%; top: 0; bottom: 0; width: 4px; background: red; transform: translateX(-50%);">
                <div style="position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); white-space: nowrap; font-weight: bold; color: red;">
                    🎯 Final: {pena_final:.1f} anos
                </div>
            </div>
            
            <!-- Marcadores de regime -->
            <div style="position: absolute; left: 0%; bottom: -40px; font-size: 12px;">
                🔓 Aberto<br>(<4 anos)
            </div>
            <div style="position: absolute; left: 50%; bottom: -40px; transform: translateX(-50%); font-size: 12px;">
                🔐 Semiaberto<br>(4-8 anos)
            </div>
            <div style="position: absolute; right: 0%; bottom: -40px; font-size: 12px;">
                🔒 Fechado<br>(>8 anos)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Legenda do gráfico
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟩 **Regime Aberto** - Até 4 anos")
    with col2:
        st.markdown("🟨 **Regime Semiaberto** - 4 a 8 anos")
    with col3:
        st.markdown("🟥 **Regime Fechado** - Acima de 8 anos")
    
    # Detalhamento numérico
    st.subheader("📈 Detalhamento do Cálculo")
    
    detalhes = f"""
    | Etapa | Valor | Cálculo |
    |-------|-------|---------|
    | Pena Mínima | {min_pena} anos | - |
    | Pena Máxima | {max_pena} anos | - |
    | **Pena Base** | **{pena_base:.1f} anos** | ({min_pena} + {max_pena}) ÷ 2 |
    | Atenuantes ({len(atenuantes)}) | -{pena_base * (1/6) * len(atenuantes):.1f} anos | -1/6 para cada |
    | Agravantes ({len(agravantes)}) | +{pena_base * (1/6) * len(agravantes):.1f} anos | +1/6 para cada |
    | **Pena Final** | **{pena_final:.1f} anos** | Base + Ajustes |
    """
    
    st.markdown(detalhes)

