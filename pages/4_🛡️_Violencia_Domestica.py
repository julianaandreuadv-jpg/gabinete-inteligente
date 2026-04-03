import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Violência Doméstica", page_icon="🛡️", layout="wide")
st.title("🛡️ Motor de Violência Doméstica (Maria da Penha)")
st.markdown("Gestão de Medidas Protetivas de Urgência (MPU) e processamento com perspectiva de gênero (CNJ).")
st.markdown("---")

# 2. Cláusula de Guarda (Segurança)
if 'api_key' not in st.session_state:
    st.warning("⚠️ Atenção: Volte à página inicial e insira sua Chave API para ativar este módulo.")
    st.stop()

# Conecta o cérebro da IA
genai.configure(api_key=st.session_state['api_key'])
model = genai.GenerativeModel('gemini-1.5-pro')

# Regras Globais do Kernel (Linguagem Simples + ABNT + Protocolo CNJ)
REGRAS_GLOBAIS = """
- Aplique o Pacto pela Linguagem Simples (CNJ). 
- Estruture a decisão em Markdown ABNT (negritos, tópicos, dispositivo em lista).
- OBRIGATÓRIO: Aplique as diretrizes do 'Protocolo para Julgamento com Perspectiva de Gênero' do CNJ.
"""

# 3. Organização Visual em Abas (Tabs)
aba_mpu, aba_art16, aba_sentenca = st.tabs([
    "🚨 Medidas Protetivas (MPU)", 
    "⚖️ Audiência Art. 16 (Retratação)", 
    "📜 Sentença de Mérito (VD)"
])

# ==========================================
# ABA 1: MEDIDAS PROTETIVAS DE URGÊNCIA (MPU)
# ==========================================
with aba_mpu:
    st.header("Análise Cautelar de MPU (Prazo Legal: 48h)")
    
    col1, col2 = st.columns(2)
    with col1:
        vitima = st.text_input("Qualificação da Vítima:")
        tipo_violencia = st.multiselect("Tipos de Violência (Art. 7º, LMP):", 
                                        ["Física", "Psicológica", "Sexual", "Patrimonial", "Moral"])
    with col2:
        agressor = st.text_input("Qualificação do Suposto Agressor:")
        medidas_pedidas = st.text_input("Medidas Requeridas (ex: Afastamento do lar, proibição de contato):")
        
    relato_fatos = st.text_area("Síntese do Boletim de Ocorrência / Relato da Vítima:", height=150)
    
    if st.button("🚨 Gerar Decisão de MPU"):
        if relato_fatos:
            with st.spinner("Analisando risco iminente à integridade da vítima..."):
                prompt_mpu = f"""
                {REGRAS_GLOBAIS}
                Redija uma decisão interlocutória apreciando pedido de Medidas Protetivas de Urgência.
                Vítima: {vitima}. Agressor: {agressor}.
                Violências relatadas: {tipo_violencia}. Medidas requeridas: {medidas_pedidas}.
                Fatos: {relato_fatos}
                
                Instruções Críticas:
                - Fundamente a decisão com base na Súmula 589 do STJ (especial relevância da palavra da vítima).
                - Reconheça expressamente a vulnerabilidade de gênero.
                - No dispositivo, fixe claramente o escopo das medidas (distância em metros, meios de comunicação proibidos) e a advertência de prisão preventiva em caso de descumprimento (Art. 313, III, CPP).
                """
                st.markdown(model.generate_content(prompt_mpu).text)
        else:
            st.error("Insira o relato dos fatos para análise de risco.")

# ==========================================
# ABA 2: AUDIÊNCIA DO ART. 16 (Retratação)
# ==========================================
with aba_art16:
    st.header("Gestão da Audiência de Renúncia (Art. 16, LMP)")
    st.info("⚠️ Lembrete do Sistema: Esta audiência só é cabível em crimes de Ação Penal Pública Condicionada (ex: Ameaça). É incabível em lesão corporal (Súmula 542 STJ).")
    
    crime_imputado = st.selectbox("Crime Imputado:", ["Ameaça (Art. 147, CP)", "Lesão Corporal (Art. 129, §13, CP)", "Outros"])
    decisao_vitima = st.radio("Postura da Vítima na Audiência:", ["Manteve a renúncia/retratação", "Deseja prosseguir com o processo (representar)"])
    
    if st.button("📝 Gerar Termo / Decisão (Art. 16)"):
        with st.spinner("Estruturando o termo de audiência e a homologação..."):
            prompt_art16 = f"""
            {REGRAS_GLOBAIS}
            Redija um Termo de Audiência c/c Decisão Homologatória referente ao Art. 16 da Lei Maria da Penha.
            Crime: {crime_imputado}.
            Decisão da Vítima: {decisao_vitima}.
            
            Instrução:
            - Se o crime for Lesão Corporal, inclua um despacho cancelando a audiência ou anulando a retratação com base na Súmula 542 do STJ (Ação Incondicionada).
            - Se for Ameaça e houve retratação, gere a decisão de extinção da punibilidade.
            - Se ela desejou prosseguir, gere o termo determinando remessa ao MP para denúncia.
            """
            st.markdown(model.generate_content(prompt_art16).text)

# ==========================================
# ABA 3: SENTENÇA DE MÉRITO E DANOS MORAIS
# ==========================================
with aba_sentenca:
    st.header("Sentença Condenatória Especializada")
    
    fatos_sentenca = st.text_area("Síntese da Instrução (Depoimentos e Provas):", height=150)
    pedido_danos = st.checkbox("Houve pedido expresso de Danos Morais pelo MP/Assistente?")
    
    if st.button("⚖️ Compilar Sentença de VD"):
        if fatos_sentenca:
            with st.spinner("Subsumindo tipicidade com perspectiva de gênero..."):
                prompt_sent_vd = f"""
                {REGRAS_GLOBAIS}
                Redija uma Sentença Penal de mérito envolvendo Violência Doméstica.
                Provas: {fatos_sentenca}.
                Pedido de Danos Morais na Inicial: {pedido_danos}.
                
                Instruções:
                - Afaste explicitamente teses incompatíveis, como o Princípio da Insignificância ou a ausência de testemunhas visuais (Súmula 589 STJ).
                - Se {pedido_danos} for True (Verdadeiro), é OBRIGATÓRIA a fixação de valor mínimo de indenização por dano moral no dispositivo (Tema 983 STJ), dispensando dilação probatória sobre o dano.
                """
                st.markdown(model.generate_content(prompt_sent_vd).text)
        else:
            st.error("Descreva as provas produzidas na instrução.")
