import streamlit as st
import math

# --- 1. CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="MOTORS CALCULATOR", layout="wide", page_icon="⚙️")

st.markdown("""
    <style>
    .metric-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #eab308;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title { color: #fde047; margin: 0; font-size: 1rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px;}
    .metric-value { color: #ffffff; margin: 10px 0 0 0; font-size: 2rem; font-weight: bold; }
    .metric-sub { color: #94a3b8; font-size: 0.85rem; margin-top: 5px;}
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ MOTORS CALCULATOR")
st.markdown("Cálculos avançados para projeto e preparação de motores.")
st.markdown("---")

# --- NAVEGAÇÃO EM ABAS ---
aba1, aba2, aba3 = st.tabs(["📐 Geometria do Bloco", "🔥 Cabeçote e Compressão", "🌪️ Fluxo (TBI, Válvulas e Dutos)"])

# ==========================================
# ABA 1: GEOMETRIA DO BLOCO
# ==========================================
with aba1:
    st.header("Parâmetros do Conjunto Rotativo")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        diametro = st.number_input("Diâmetro do Pistão (mm)", value=63.5, step=0.5, key="d1")
        curso = st.number_input("Curso do Virabrequim (mm)", value=57.3, step=0.5, key="c1")
    with col_b:
        biela = st.number_input("Comprimento da Biela (mm)", value=96.0, step=0.5)
        cilindros = st.number_input("Nº de Cilindros", min_value=1, value=1, step=1, key="cyl1")
    with col_c:
        rpm = st.number_input("Rotação Máxima (RPM)", value=8000, step=100)

    # MATEMÁTICA ABA 1
    raio_cm = (diametro / 2) / 10
    curso_cm = curso / 10
    area_pistao = math.pi * (raio_cm ** 2)
    cil_unit = area_pistao * curso_cm
    cil_total = cil_unit * cilindros
    vmp = (curso * rpm) / 30000
    rl = (curso / 2) / biela

    st.markdown("### 📊 Resultados do Bloco")
    r1, r2, r3 = st.columns(3)
    
    r1.markdown(f"<div class='metric-box'><p class='metric-title'>Cilindrada</p><p class='metric-value'>{cil_total:.1f} cc</p><p class='metric-sub'>Unitária: {cil_unit:.1f} cc</p></div>", unsafe_allow_html=True)
    
    cor_vmp = "#f44336" if vmp > 21 else "#4caf50"
    aviso_vmp = "Risco de Quebra" if vmp > 21 else "Seguro"
    r2.markdown(f"<div class='metric-box' style='border-left: 6px solid {cor_vmp};'><p class='metric-title'>VMP</p><p class='metric-value'>{vmp:.1f} m/s</p><p class='metric-sub' style='color:{cor_vmp};'>{aviso_vmp}</p></div>", unsafe_allow_html=True)
    
    cor_rl = "#f44336" if rl > 0.30 else "#4caf50"
    aviso_rl = "Atrito Elevado" if rl > 0.30 else "Durável"
    r3.markdown(f"<div class='metric-box' style='border-left: 6px solid {cor_rl};'><p class='metric-title'>Relação R/L</p><p class='metric-value'>{rl:.3f}</p><p class='metric-sub' style='color:{cor_rl};'>{aviso_rl}</p></div>", unsafe_allow_html=True)

# ==========================================
# ABA 2: CABEÇOTE E COMPRESSÃO
# ==========================================
with aba2:
    st.header("Cálculo de Taxa e Volume da Câmara")
    
    col_d, col_e = st.columns(2)
    with col_d:
        st.info(f"Cilindrada Unitária calculada: **{cil_unit:.1f} cc**")
        vol_camara = st.number_input("Volume medido na Câmara (cc/ml)", value=18.0, step=0.5)
    with col_e:
        vol_junta = st.number_input("Volume da Junta/Deck (cc/ml)", value=1.5, step=0.1)

    # MATEMÁTICA ABA 2
    vol_total_esmagado = vol_camara + vol_junta
    taxa_compressao = (cil_unit + vol_total_esmagado) / vol_total_esmagado if vol_total_esmagado > 0 else 0

    st.markdown("### 📊 Resultado da Compressão")
    st.markdown(f"<div class='metric-box'><p class='metric-title'>Taxa de Compressão Dinâmica</p><p class='metric-value'>{taxa_compressao:.2f} : 1</p><p class='metric-sub'>Combustível ideal varia conforme a taxa gerada.</p></div>", unsafe_allow_html=True)

# ==========================================
# ABA 3: FLUXO AVANÇADO (TBI E VÁLVULAS)
# ==========================================
with aba3:
    st.header("Dimensionamento Dinâmico de Alimentação e Dutos")
    
    st.markdown(f"**Base geométrica:** {cil_unit:.1f}cc | Pistão: {diametro}mm | Rotação Alvo: {rpm} RPM")
    
    col_x, col_y = st.columns(2)
    with col_x:
        aplicacao = st.selectbox("Aplicação do Motor:", ["Rua / Esportivo (Torque em média alta)", "Pista / Competição (Potência em alta)"])
        tipo_cabecote = st.radio("Cabeçote:", ["2 Válvulas", "4 Válvulas"])
    with col_y:
        if "Rua" in aplicacao:
            ve_padrao = 85.0
            vel_gas_alvo = 75.0 # m/s (Ideal para manter torque e velocidade de fluxo)
        else:
            ve_padrao = 100.0
            vel_gas_alvo = 90.0 # m/s (Foco em enchimento em altíssima rotação)
            
        ve = st.number_input("Eficiência Volumétrica (VE %)", value=ve_padrao, step=5.0)
        vel_gas = st.number_input("Velocidade do Gás Alvo (m/s)", value=vel_gas_alvo, step=1.0)

    # MATEMÁTICA V2 - CFM e TBI
    cfm_necessario = (cil_total * rpm * (ve / 100)) / 5660
    diametro_tbi = math.sqrt((cfm_necessario * 4) / (math.pi * 0.05))
    
    # MATEMÁTICA V2 - Válvulas baseadas no fluxo e velocidade do gás
    area_pistao_mm2 = math.pi * ((diametro / 2) ** 2)
    area_valvula_necessaria = (area_pistao_mm2 * vmp) / vel_gas
    
    if "2 Válvulas" in tipo_cabecote:
        valvula_adm = 2 * math.sqrt(area_valvula_necessaria / math.pi)
        valvula_esc = valvula_adm * 0.85
    else:
        valvula_adm = 2 * math.sqrt((area_valvula_necessaria / 2) / math.pi)
        valvula_esc = valvula_adm * 0.85

    duto_adm = valvula_adm * 0.80
    duto_esc = valvula_esc * 0.85

    st.markdown("### 📊 Dimensionamento por Dinâmica de Fluidos")
    
    c_f1, c_f2 = st.columns(2)
    c_f1.markdown(f"<div class='metric-box' style='border-left: 6px solid #2196f3;'><p class='metric-title'>Carburador / Corpo de Borboleta (TBI)</p><p class='metric-value'>Ø {diametro_tbi:.1f} mm</p><p class='metric-sub'>Fluxo exigido: {cfm_necessario:.1f} CFM</p></div>", unsafe_allow_html=True)
    
    c_f2.markdown(f"<div class='metric-box' style='border-left: 6px solid #9c27b0;'><p class='metric-title'>Gargalo dos Dutos (ADM / ESC)</p><p class='metric-value'>Ø {duto_adm:.1f} / {duto_esc:.1f} mm</p><p class='metric-sub'>Velocidade calculada: {vel_gas} m/s</p></div>", unsafe_allow_html=True)

    st.markdown("#### Diâmetro de Válvulas Corrigido pelo Fluxo")
    st.markdown(f"""
    * **Válvula(s) de Admissão:** Ø {valvula_adm:.1f} mm
    * **Válvula(s) de Escape:** Ø {valvula_esc:.1f} mm
    """)
    st.info("Nota do Sistema: Baseado na aplicação escolhida e velocidade dos gases, este setup é otimizado para a eficiência desejada.")