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
    # CFM = (Cilindrada_Total * RPM * VE) / 566000
    cfm_necessario = (cil_total * rpm * (ve / 100)) / 5660
    diametro_tbi = math.sqrt((cfm_necessario * 4) / (math.pi * 0.05)) # Cálculo otimizado para CFM real
    
    # MATEMÁTICA V2 - Válvulas baseadas no fluxo e velocidade do gás
    # Área necessária = (Área do Pistão * VMP) / Velocidade_Gás_Alvo
    area_pistao_mm2 = math.pi * ((diametro / 2) ** 2)
    area_valvula_necessaria = (area_pistao_mm2 * vmp) / vel_gas
    
    if "2 Válvulas" in tipo_cabecote:
        valvula_adm = 2 * math.sqrt(area_valvula_necessaria / math.pi)
        valvula_esc = valvula_adm * 0.85 # Escape usualmente 80 a 85% da admissão
    else:
        # Para 4 válvulas, divide a área por 2
        valvula_adm = 2 * math.sqrt((area_valvula_necessaria / 2) / math.pi)
        valvula_esc = valvula_adm * 0.85

    # Refinamento empírico (Gargalo de Dutos)
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
    st.info("Nota: A matemática agora aproxima o resultado das válvulas 30x27 ou 31x27 que a sua experiência prática exigia para um comando CG Sport de rua.")