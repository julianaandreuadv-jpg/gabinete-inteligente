import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Cível e Fazenda", page_icon="⚖️", layout="wide")
st.title("⚖️ Motor Cível, Família e Fazenda Pública")
st.markdown("Redação técnica de tutelas, sentenças e atos de execução (CPC/15, JEC e Leis Especiais).")
st.markdown("---")

# 2. Cláusula de Guarda (Segurança)
if 'api_key' not in st.session_state:
    st.warning("⚠️ Atenção: Volte à página inicial e insira sua Chave API para ativar este módulo.")
    st.stop()

# Conecta o cérebro da IA
genai.configure(api_key=st.session_state['api_key'])
model = genai.GenerativeModel('gemini-1.5-pro')

# Importação simulada das nossas regras de ouro (Kernel)
REGRAS_GLOBAIS = """
- Aplique o Pacto pela Linguagem Simples (CNJ). Zero "juridiquês" arcaico.
- Estruture em ABNT (Uso de Markdown, negritos para cabeçalhos e listas para o dispositivo).
- Ancore a fundamentação em jurisprudência atualizada do STJ (2026).
"""

# 3. Organização Visual em Abas (Tabs)
aba_tutelas, aba_sentenca, aba_execucao = st.tabs([
    "🚨 Tutelas de Urgência/Evidência", 
    "📜 Sentenças de Mérito", 
    "💰 Execução e Cumprimento"
])

# ==========================================
# ABA 1: TUTELAS (Liminares e Interlocutórias)
# ==========================================
with aba_tutelas:
    st.header("Análise de Tutelas Provisórias")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_tutela = st.selectbox("Natureza do Pedido:", [
            "Urgência Antecipada (Art. 300)", 
            "Urgência Cautelar (Art. 305)", 
            "Evidência (Art. 311)",
            "Liminar contra Fazenda Pública (Leis 8.437/92 e 9.494/97)"
        ])
    with col2:
        polo_passivo = st.text_input("Qualificação do Réu (Tem Fazenda Pública?):")
        
    fatos_tutela = st.text_area("Síntese do Pedido Liminar e Fatos:", height=150)
    
    if st.button("⚖️ Gerar Decisão Interlocutória (Tutela)"):
        if fatos_tutela:
            with st.spinner("Analisando Fumus Boni Iuris e Periculum in Mora..."):
                prompt_tutela = f"""
                {REGRAS_GLOBAIS}
                Atue como Juiz/Assessor. Redija uma decisão interlocutória analisando pedido de tutela.
                Tipo: {tipo_tutela}. Réu: {polo_passivo}.
                Fatos narrados: {fatos_tutela}.
                
                Instruções Específicas:
                - Se for contra a Fazenda Pública, inclua a análise OBRIGATÓRIA das vedações legais para concessão de liminares contra o poder público.
                - Diferencie tecnicamente probabilidade do direito e perigo de dano.
                - Finalize com dispositivo imperativo (CONCEDO ou INDEFIRO).
                """
                st.markdown(model.generate_content(prompt_tutela).text)
        else:
            st.error("Descreva os fatos e o pedido liminar.")

# ==========================================
# ABA 2: SENTENÇAS DE MÉRITO (O Coração do Módulo)
# ==========================================
with aba_sentenca:
    st.header("Elaboração de Sentenças Cíveis e Especiais")
    
    area_direito = st.radio("Selecione a Área Específica:", [
        "Cível Comum / Contratos", 
        "JEC (Lei 9.099/95 - Sem Relatório)", 
        "Direito de Família (Alimentos/Guarda)", 
        "Sucessões (Inventário/Partilha)",
        "Fazenda Pública (JEFAZ / Ordinária)"
    ], horizontal=True)
    
    colA, colB = st.columns(2)
    with colA:
        preliminares = st.text_input("Há preliminares? (ex: Prescrição, Ilegitimidade, Nulidade):")
    with colB:
        fase_probatória = st.text_input("Provas produzidas (ex: Testemunhal, Perícia, Revelia):")
        
    merito_fatos = st.text_area("Síntese do Mérito e Pontos Controvertidos (Art. 489, CPC):", height=200)
    
    if st.button("📜 Compilar Sentença"):
        if merito_fatos:
            with st.spinner("Subsumindo fatos à norma e estruturando sentença..."):
                prompt_sentenca = f"""
                {REGRAS_GLOBAIS}
                Redija uma Sentença Judicial completa.
                Área: {area_direito}.
                Preliminares a enfrentar: {preliminares}.
                Provas: {fase_probatória}.
                Mérito/Fatos: {merito_fatos}.
                
                Instruções Específicas:
                - Se JEC, aplique o art. 38 da Lei 9.099/95 e dispense relatório formal.
                - Se Família (Alimentos), aplique o binômio necessidade-possibilidade.
                - Se Fazenda Pública, analise a necessidade de Remessa Necessária (Art. 496, CPC).
                - Estrutura: I - RELATÓRIO (se couber), II - FUNDAMENTAÇÃO (com tópicos para preliminares), III - DISPOSITIVO.
                """
                st.markdown(model.generate_content(prompt_sentenca).text)
        else:
            st.error("Descreva o mérito para elaboração da sentença.")

# ==========================================
# ABA 3: EXECUÇÃO E CUMPRIMENTO DE SENTENÇA
# ==========================================
with aba_execucao:
    st.header("Atos de Expropriação e Medidas Coercitivas")
    
    fase_execucao = st.selectbox("Ato Processual Solicitado:", [
        "Despacho Inicial de Penhora (Sisbajud/Renajud)", 
        "Decisão de Impugnação ao Cumprimento", 
        "Reconhecimento de Fraude à Execução",
        "Medidas Atípicas (Art. 139, IV, CPC - Apreensão CNH/Passaporte)"
    ])
    
    detalhes_execucao = st.text_area("Detalhes do caso (ex: bens ocultos, valor da dívida, alegações do devedor):", height=150)
    
    if st.button("💰 Gerar Ato Executório"):
        if detalhes_execucao:
            with st.spinner("Mapeando ordem de penhora e jurisprudência STJ..."):
                prompt_execucao = f"""
                {REGRAS_GLOBAIS}
                Redija um ato judicial na fase de execução.
                Fase/Ato: {fase_execucao}
                Detalhes: {detalhes_execucao}
                
                Instruções Específicas:
                - Se for Medida Atípica (Art. 139, IV), fundamente na jurisprudência do STJ sobre subsidiariedade, proporcionalidade e esgotamento das vias típicas.
                - Se for Fraude à Execução, analise os requisitos da Súmula 375 do STJ (registro da penhora ou má-fé).
                - Seja contundente, técnico e voltado à satisfação do crédito respeitando a menor onerosidade.
                """
                st.markdown(model.generate_content(prompt_execucao).text)
        else:
            st.error("Forneça os detalhes da execução.")
