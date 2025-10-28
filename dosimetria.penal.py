import streamlit as st
import pandas as pd

# Título
st.title("⚖️ Simulador de Dosimetria da Pena")
st.write("**Calculadora completa da dosimetria penal conforme Art. 68 do CP**")

# ========== CARREGAR E PROCESSAR DADOS DO EXCEL ==========
@st.cache_data
def carregar_dados_crimes():
    try:
        # Carregar o arquivo Excel
        df = pd.read_excel('crimes_cp_final.xlsx')

        # Criar dicionário de crimes
        crimes_dict = {}
        penas_dict = {}

        for idx, row in df.iterrows():
            artigo_completo = row['Artigo_Completo']
            descricao = row['Descricao_Crime']
            pena_min = row['Pena_Minima']
            pena_max = row['Pena_Maxima']
            tipo_penal = row['Tipo_Penal']

            # Processar valores de pena
            if pd.notna(pena_min) and pd.notna(pena_max):
                # Converter textos como "seis anos" para números
                if isinstance(pena_min, str) and any(char.isalpha() for char in pena_min):
                    # Simplificação - em produção você precisaria de um parser mais robusto
                    try:
                        if 'seis' in pena_min.lower():
                            pena_min_num = 6
                        elif 'um' in pena_min.lower():
                            pena_min_num = 1
                        elif 'dois' in pena_min.lower():
                            pena_min_num = 2
                        elif 'três' in pena_min.lower() or 'tres' in pena_min.lower():
                            pena_min_num = 3
                        elif 'quatro' in pena_min.lower():
                            pena_min_num = 4
                        elif 'cinco' in pena_min.lower():
                            pena_min_num = 5
                        else:
                            pena_min_num = 3  # padrão
                    except:
                        pena_min_num = 3
                else:
                    try:
                        pena_min_num = float(pena_min)
                    except:
                        pena_min_num = 3

                # Fazer o mesmo para pena máxima
                if isinstance(pena_max, str) and any(char.isalpha() for char in pena_max):
                    try:
                        if 'vinte' in pena_max.lower():
                            pena_max_num = 20
                        elif 'trinta' in pena_max.lower():
                            pena_max_num = 30
                        elif 'quinze' in pena_max.lower():
                            pena_max_num = 15
                        elif 'dez' in pena_max.lower():
                            pena_max_num = 10
                        else:
                            pena_max_num = 10  # padrão
                    except:
                        pena_max_num = 10
                else:
                    try:
                        pena_max_num = float(pena_max)
                    except:
                        pena_max_num = 10

                # Calcular pena base (média)
                pena_base = (pena_min_num + pena_max_num) / 2

                if pd.notna(artigo_completo) and pd.notna(descricao):
                    chave = f"{artigo_completo} - {descricao[:50]}..."
                    crimes_dict[chave] = {
                        'artigo': artigo_completo,
                        'descricao_completa': descricao,
                        'pena_min': pena_min_num,
                        'pena_max': pena_max_num,
                        'pena_base': pena_base,
                        'tipo_penal': tipo_penal
                    }

        return crimes_dict

    except Exception as e:
        st.error(f"Erro ao carregar dados do Excel: {e}")
        return {}

# Carregar dados
crimes_data = carregar_dados_crimes()

# Sidebar com informações
st.sidebar.header("💡 Sobre")
st.sidebar.write("""
**Base Legal:**
- Art. 68 do Código Penal
- Fases da dosimetria:
  1. Pena base + circunstâncias
  2. Atenuantes/Agravantes
  3. Majorantes/Minorantes
  4. Cálculo final
  5. Regime
  6. Substituição
""")

# Mostrar estatísticas dos dados carregados
if crimes_data:
    st.sidebar.write(f"**📊 Crimes carregados:** {len(crimes_data)}")
    st.sidebar.write("**🔍 Buscar crime:**")
    busca = st.sidebar.text_input("Digite o artigo ou descrição:")
    if busca:
        crimes_filtrados = {k: v for k, v in crimes_data.items() if busca.lower() in k.lower()}
        for chave in list(crimes_filtrados.keys())[:5]:  # Mostrar apenas os 5 primeiros
            crime_info = crimes_filtrados[chave]
            st.sidebar.write(f"**{crime_info['artigo']}**")
            st.sidebar.write(f"Pena: {crime_info['pena_min']}-{crime_info['pena_max']} anos")
            st.sidebar.write("---")

# ========== FASE 1: PENA BASE + CIRCUNSTÂNCIAS ==========
st.header("1️⃣ Fase 1: Pena Base e Circunstâncias")

col1, col2 = st.columns([2, 1])

with col1:
    if crimes_data:
        # Usar crimes do Excel como opções
        crime_selecionado = st.selectbox(
            "Selecione o Crime:",
            options=list(crimes_data.keys()),
            format_func=lambda x: x
        )
        crime_info = crimes_data[crime_selecionado]

        min_pena = crime_info['pena_min']
        max_pena = crime_info['pena_max']
        pena_base_inicial = crime_info['pena_base']

        st.write(f"**Artigo:** {crime_info['artigo']}")
        st.write(f"**Tipo penal:** {crime_info['tipo_penal']}")
        st.write(f"**Descrição completa:** {crime_info['descricao_completa']}")
    else:
        # Fallback para lista fixa se não carregar do Excel
        crime = st.selectbox("Tipo de Crime:", [
            "Roubo (Art. 157)",
            "Roubo Qualificado (Art. 157, §1º)",
            "Furto (Art. 155)",
            "Furto Qualificado (Art. 155, §4º)",
            "Estelionato (Art. 171)",
            "Lesão Corporal (Art. 129)",
            "Lesão Corporal Grave (Art. 129, §1º)",
            "Homicídio Simples (Art. 121)",
            "Homicídio Qualificado (Art. 121, §2º)"
        ])

        # Define pena base conforme crime (fallback)
        penas_base_fallback = {
            "Roubo (Art. 157)": {"min": 4, "max": 10, "base": 7},
            "Roubo Qualificado (Art. 157, §1º)": {"min": 8, "max": 15, "base": 11.5},
            "Furto (Art. 155)": {"min": 1, "max": 4, "base": 2.5},
            "Furto Qualificado (Art. 155, §4º)": {"min": 2, "max": 8, "base": 5},
            "Estelionato (Art. 171)": {"min": 1, "max": 5, "base": 3},
            "Lesão Corporal (Art. 129)": {"min": 3, "max": 8, "base": 5.5},
            "Lesão Corporal Grave (Art. 129, §1º)": {"min": 6, "max": 12, "base": 9},
            "Homicídio Simples (Art. 121)": {"min": 6, "max": 20, "base": 13},
            "Homicídio Qualificado (Art. 121, §2º)": {"min": 12, "max": 30, "base": 21}
        }

        min_pena = penas_base_fallback[crime]["min"]
        max_pena = penas_base_fallback[crime]["max"]
        pena_base_inicial = penas_base_fallback[crime]["base"]

with col2:
    circunstancia = st.radio("Circunstância do Crime:", [
        "Neutra",
        "Desfavorável",
        "Gravemente Desfavorável"
    ])

# Ajuste por circunstância
ajuste_circunstancia = {
    "Neutra": 0,
    "Desfavorável": 0.2,  # +20%
    "Gravemente Desfavorável": 0.4  # +40%
}

# Aplica ajuste da circunstância
fator_circunstancia = ajuste_circunstancia[circunstancia]
pena_base_ajustada = pena_base_inicial * (1 + fator_circunstancia)

st.write(f"**Pena prevista no tipo penal:** {min_pena} a {max_pena} anos")
st.write(f"**Pena base inicial:** {pena_base_inicial} anos")
st.write(f"**Circunstância {circunstancia.lower()}:** {fator_circunstancia*100:.0f}% de ajuste")
st.success(f"**PENA BASE APÓS CIRCUNSTÂNCIAS: {pena_base_ajustada:.1f} anos**")

# ========== FASE 2: ATENUANTES E AGRAVANTES ==========
st.header("2️⃣ Fase 2: Atenuantes e Agravantes Gerais")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔽 Atenuantes (Art. 65 CP)")
    atenuantes = st.multiselect(
        "Selecione as atenuantes:",
        [
            "Réu primário de bons antecedentes",
            "Arrependimento espontâneo",
            "Confissão espontânea",
            "Reparação do dano",
            "Coação moral",
            "Embriaguez acidental",
            "Motivo de relevante valor social/moral"
        ]
    )

with col2:
    st.subheader("🔼 Agravantes (Art. 61 CP)")
    agravantes = st.multiselect(
        "Selecione as agravantes:",
        [
            "Reincidente específico",
            "Motivo fútil/torpe",
            "Crime contra idoso/doente",
            "Uso de disfarce/emboscada",
            "Abuso de confiança/poder",
            "Racismo/xenofobia",
            "Aumento do dano maliciosamente"
        ]
    )

# ========== FASE 3: MAJORANTES E MINORANTES ==========
st.header("3️⃣ Fase 3: Causas de Aumento/Diminuição")

st.write("**Causas específicas do tipo penal selecionado:**")

# Lista genérica de majorantes/minorantes (poderia ser expandida com dados do Excel)
majorantes_minorantes_generico = {
    "majorantes": [
        "Uso de arma (1/6 a 1/2)",
        "Violência grave (1/3 a 2/3)",
        "Concurso de 2+ pessoas (1/4 a 1/2)",
        "Restrição à liberdade (1/6 a 1/3)",
        "Abuso de confiança (1/6 a 1/3)"
    ],
    "minorantes": [
        "Valor ínfimo (1/6 a 1/3)",
        "Arrependimento posterior (1/6 a 1/3)",
        "Circunstâncias atenuantes não previstas (1/6 a 1/3)"
    ]
}

col1, col2 = st.columns(2)

with col1:
    majorantes = st.multiselect(
        "Causas de aumento (majorantes):",
        majorantes_minorantes_generico["majorantes"]
    )

with col2:
    minorantes = st.multiselect(
        "Causas de diminuição (minorantes):",
        majorantes_minorantes_generico["minorantes"]
    )

# ========== FASE 4: CÁLCULO FINAL ==========
st.header("4️⃣ Fase 4: Cálculo Final da Pena")

if st.button("🎯 Calcular Pena Definitiva", type="primary"):

    # Começa com a pena base ajustada
    pena_calculada = pena_base_ajustada

    st.subheader("📊 Detalhamento do Cálculo")

    calculo_detalhado = f"""
    | Etapa | Valor | Ajuste |
    |-------|-------|---------|
    | **Pena Base Inicial** | {pena_base_inicial} anos | - |
    | Circunstância {circunstancia} | {pena_base_ajustada:.1f} anos | {fator_circunstancia*100:+.0f}% |
    """

    # Aplica atenuantes (-1/6 cada)
    ajuste_atenuantes = 0
    for i, atenuante in enumerate(atenuantes, 1):
        reducao = pena_base_ajustada * (1/6)
        ajuste_atenuantes -= reducao
        pena_calculada -= reducao
        calculo_detalhado += f"| Atenuante {i} | {pena_calculada:.1f} anos | -{reducao:.1f} anos |\n"

    # Aplica agravantes (+1/6 cada)
    ajuste_agravantes = 0
    for i, agravante in enumerate(agravantes, 1):
        aumento = pena_base_ajustada * (1/6)
        ajuste_agravantes += aumento
        pena_calculada += aumento
        calculo_detalhado += f"| Agravante {i} | {pena_calculada:.1f} anos | +{aumento:.1f} anos |\n"

    # Aplica majorantes (+1/6 a +1/2 cada)
    ajuste_majorantes = 0
    for i, majorante in enumerate(majorantes, 1):
        aumento = pena_base_ajustada * (1/4)  # Média de 1/4
        ajuste_majorantes += aumento
        pena_calculada += aumento
        calculo_detalhado += f"| Majorante {i} | {pena_calculada:.1f} anos | +{aumento:.1f} anos |\n"

    # Aplica minorantes (-1/6 a -1/3 cada)
    ajuste_minorantes = 0
    for i, minorante in enumerate(minorantes, 1):
        reducao = pena_base_ajustada * (1/4)  # Média de 1/4
        ajuste_minorantes -= reducao
        pena_calculada -= reducao
        calculo_detalhado += f"| Minorante {i} | {pena_calculada:.1f} anos | -{reducao:.1f} anos |\n"

    # Limites legais
    pena_final = max(min_pena, min(max_pena, pena_calculada))

    calculo_detalhado += f"| **LIMITES LEGAIS** | **{pena_final:.1f} anos** | **Ajuste final** |"

    st.markdown(calculo_detalhado)

    # ========== FASE 5: DETERMINAÇÃO DO REGIME ==========
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

    st.markdown(f"""
    <div style="background-color: {cor_regime}20; padding: 20px; border-radius: 10px; border-left: 5px solid {cor_regime};">
        <h2 style="color: {cor_regime}; margin: 0;">🔒 REGIME {regime}</h2>
        <p style="margin: 10px 0 0 0; font-size: 16px;"><strong>{descricao}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # ========== FASE 6: SUBSTITUIÇÃO DA PENA ==========
    st.header("6️⃣ Fase 6: Substituição da Pena")

    if pena_final <= 4:
        substituicao = "**CABE SUBSTITUIÇÃO** por pena restritiva de direitos"
        cor_subst = "#44cc44"
        fundamento = "Art. 44 CP - Penas até 4 anos podem ser substituídas"
    else:
        substituicao = "**NÃO CABE SUBSTITUIÇÃO**"
        cor_subst = "#ff4444"
        fundamento = "Art. 44 CP - Penas superiores a 4 anos não podem ser substituídas"

    st.markdown(f"""
    <div style="background-color: {cor_subst}20; padding: 15px; border-radius: 10px; border-left: 5px solid {cor_subst};">
        <h3 style="color: {cor_subst}; margin: 0;">{substituicao}</h3>
        <p style="margin: 5px 0 0 0;">{fundamento}</p>
    </div>
    """, unsafe_allow_html=True)

    # ========== GRÁFICO VISUAL DA DOSIMETRIA ==========
    st.header("📊 Gráfico da Dosimetria")

    # Calcular posições para o gráfico
    faixa_total = max_pena - min_pena
    pos_base = ((pena_base_inicial - min_pena) / faixa_total) * 100
    pos_ajustada = ((pena_base_ajustada - min_pena) / faixa_total) * 100
    pos_final = ((pena_final - min_pena) / faixa_total) * 100

    # Criar gráfico visual com HTML/CSS
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 30px; border-radius: 15px; margin: 20px 0;">
        <h4 style="text-align: center; margin-bottom: 30px;">Evolução da Dosimetria da Pena</h4>

        <div style="position: relative; height: 120px; background: linear-gradient(90deg, #d4f8d4 0%, #fff9c4 50%, #ffcdd2 100%); border-radius: 10px; border: 2px solid #dee2e6; margin-bottom: 60px;">

            <!-- Linha da Pena Base -->
            <div style="position: absolute; left: {pos_base}%; top: 0; bottom: 0; width: 3px; background: #007bff; transform: translateX(-50%);">
                <div style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); white-space: nowrap; background: white; padding: 2px 8px; border-radius: 10px; border: 1px solid #007bff; font-size: 12px; font-weight: bold; color: #007bff;">
                    ⚖️ Base: {pena_base_inicial} anos
                </div>
            </div>

            <!-- Linha da Pena Ajustada -->
            <div style="position: absolute; left: {pos_ajustada}%; top: 0; bottom: 0; width: 3px; background: #6f42c1; transform: translateX(-50%);">
                <div style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); white-space: nowrap; background: white; padding: 2px 8px; border-radius: 10px; border: 1px solid #6f42c1; font-size: 12px; font-weight: bold; color: #6f42c1;">
                    📈 Ajustada: {pena_base_ajustada:.1f} anos
                </div>
            </div>

            <!-- Linha da Pena Final -->
            <div style="position: absolute; left: {pos_final}%; top: 0; bottom: 0; width: 4px; background: #dc3545; transform: translateX(-50%);">
                <div style="position: absolute; bottom: -35px; left: 50%; transform: translateX(-50%); white-space: nowrap; background: white; padding: 2px 8px; border-radius: 10px; border: 1px solid #dc3545; font-size: 12px; font-weight: bold; color: #dc3545;">
                    🎯 Final: {pena_final:.1f} anos
                </div>
            </div>

        </div>

        <!-- Legenda dos regimes -->
        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <div style="text-align: center;">
                <div style="background: #d4f8d4; padding: 10px; border-radius: 5px; border: 1px solid #44cc44;">
                    <strong>🔓 ABERTO</strong><br>
                    <small>Até 4 anos</small>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #fff9c4; padding: 10px; border-radius: 5px; border: 1px solid #ffaa00;">
                    <strong>🔐 SEMIABERTO</strong><br>
                    <small>4 a 8 anos</small>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #ffcdd2; padding: 10px; border-radius: 5px; border: 1px solid #ff4444;">
                    <strong>🔒 FECHADO</strong><br>
                    <small>Acima de 8 anos</small>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resumo final
    st.success(f"**RESUMO FINAL:** Pena de {pena_final:.1f} anos - Regime {regime} - {substituicao}")

# ========== TABELA DE REFERÊNCIA ==========
st.header("📋 Tabela de Referência")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Regimes")
    st.table([
        {"Pena": "Até 4 anos", "Regime": "Aberto"},
        {"Pena": "4 a 8 anos", "Regime": "Semiaberto"},
        {"Pena": "Acima de 8 anos", "Regime": "Fechado"}
    ])

with col2:
    st.subheader("⚖️ Fatores")
    st.table([
        {"Fator": "Atenuante", "Ajuste": "-1/6"},
        {"Fator": "Agravante", "Ajuste": "+1/6"},
        {"Fator": "Majorante", "Ajuste": "+1/6 a +1/2"},
        {"Fator": "Minorante", "Ajuste": "-1/6 a -1/3"}
    ])

with col3:
    st.subheader("🔀 Substituição")
    st.table([
        {"Condição": "Pena ≤ 4 anos", "Substitui": "Sim"},
        {"Condição": "Pena > 4 anos", "Substitui": "Não"},
        {"Condição": "Réu reincidente", "Substitui": "Restrita"}
    ])

# Rodapé
st.markdown("---")
st.write("**⚖️ Ferramenta educacional - Consulte sempre a legislação atual e um profissional do direito**")
st.write("**📚 Base legal:** Arts. 59, 61, 65, 68 do Código Penal Brasileiro")
