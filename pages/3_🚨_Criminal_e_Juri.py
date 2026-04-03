import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Criminal e Júri", page_icon="🚨", layout="wide")
st.title("🚨 Motor Criminal, Cautelares e Tribunal do Júri")
st.markdown("Redação rigorosa de prisões processuais, sentenças penais (dosimetria trifásica) e decisões do Júri.")
st.markdown("---")

# 2. Cláusula de Guarda (Segurança)
if 'api_key' not in st.session_state:
    st.warning("⚠️ Atenção: Volte à página inicial e insira sua Chave API para ativar este módulo.")
    st.stop()

# Conecta o cérebro da IA
genai.configure(api_key=st.session_state['api_key'])
model = genai.GenerativeModel('gemini-1.5-pro')

# Regras Globais do Kernel (Linguagem Simples + ABNT)
REGRAS_GLOBAIS = """
- Aplique o Pacto pela Linguagem Simples (CNJ). Seja direto, evite gerúndios e adjetivação excessiva.
- Estruture a decisão em tópicos visuais (Markdown).
- Fundamente com base no STJ/STF (vigência 2026), evitando "fundamentação per relationem" genérica.
"""

# 3. Organização Visual em Abas (Tabs)
aba_cautelares, aba_sentenca, aba_juri = st.tabs([
    "🔒 Prisões e Cautelares", 
    "⚖️ Sentença e Dosimetria", 
    "🔨 Tribunal do Júri (Fase 1)"
])

# ==========================================
# ABA 1: PRISÕES PROCESSUAIS E CAUTELARES
# ==========================================
with aba_cautelares:
    st.header("Análise de Cautelares e Prova Digital")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_cautelar = st.selectbox("Tipo de Medida:", [
            "Prisão Preventiva (Art. 312, CPP)", 
            "Prisão Temporária (Lei 7.960/89)", 
            "Busca e Apreensão Domiciliar",
            "Interceptação Telefônica / Quebra de Sigilo Telemático"
        ])
    with col2:
        alvo_medida = st.text_input("Nome do Investigado/Réu:")
        
    fumus = st.text_area("Fumus Comissi Delicti (Indícios de autoria e materialidade):", height=100)
    periculum = st.text_area("Periculum Libertatis (Fundamentos da urgência/risco):", height=100)
    
    if st.button("🔒 Gerar Decisão Cautelar"):
        if fumus and periculum:
            with st.spinner("Analisando pressupostos cautelares processuais penais..."):
                prompt_cautelar = f"""
                {REGRAS_GLOBAIS}
                Redija uma decisão criminal de natureza cautelar.
                Tipo: {tipo_cautelar}. Investigado: {alvo_medida}.
                Materialidade e Indícios (Fumus): {fumus}
                Risco e Urgência (Periculum): {periculum}
                
                Instruções:
                - Se for prisão, justifique a INADEQUAÇÃO das medidas cautelares diversas (Art. 319, CPP). A prisão é a ultima ratio.
                - Se for Prova Digital (Busca ou Interceptação), mencione a garantia da cadeia de custódia (Art. 158-A, CPP) e a LGPD criminal.
                """
                st.markdown(model.generate_content(prompt_cautelar).text)
        else:
            st.error("Preencha o Fumus e o Periculum para a análise.")

# ==========================================
# ABA 2: SENTENÇA PENAL E DOSIMETRIA (Motor Trifásico)
# ==========================================
with aba_sentenca:
    st.header("Sentença Condenatória e Dosimetria da Pena")
    st.markdown("Preencha as fases para garantir a fundamentação exauriente e individualizada.")
    
    fatos_crime = st.text_area("Resumo da Imputação (Tipificação) e Provas Produzidas:", height=100)
    
    st.subheader("Cálculo da Dosimetria (Art. 68, CP)")
    colA, colB, colC = st.columns(3)
    
    with colA:
        fase1 = st.text_input("1ª Fase (Art. 59 - Pena-base):", placeholder="Ex: Culpabilidade elevada, maus antecedentes...")
    with colB:
        fase2 = st.text_input("2ª Fase (Agravantes/Atenuantes):", placeholder="Ex: Confissão espontânea, reincidência...")
    with colC:
        fase3 = st.text_input("3ª Fase (Majorantes/Minorantes):", placeholder="Ex: Emprego de arma, tentativa...")
        
    if st.button("⚖️ Compilar Sentença e Dosimetria"):
        if fatos_crime:
            with st.spinner("Subsumindo tipicidade, ilicitude e calculando a pena..."):
                prompt_sentenca = f"""
                {REGRAS_GLOBAIS}
                Redija uma Sentença Penal Condenatória.
                Fatos e Tipificação: {fatos_crime}
                
                Execute a Dosimetria da Pena rigorosamente nos moldes do sistema trifásico:
                1ª Fase (Art. 59): {fase1}. Fundamente o distanciamento do mínimo legal, se houver.
                2ª Fase: {fase2}. Aplique a Súmula 231 do STJ (nunca reduza aquém do mínimo).
                3ª Fase: {fase3}. Aplique frações legais.
                
                Estrutura exigida:
                I - RELATÓRIO
                II - FUNDAMENTAÇÃO (Materialidade, Autoria, Tipicidade)
                III - DOSIMETRIA DA PENA (Dividida em 1ª, 2ª e 3ª Fases claras)
                IV - DISPOSITIVO (Fixando regime inicial e detração do art. 387, § 2º, CPP).
                """
                st.markdown(model.generate_content(prompt_sentenca).text)
        else:
            st.error("Descreva a imputação e as provas.")

# ==========================================
# ABA 3: TRIBUNAL DO JÚRI (Fase de Pronúncia)
# ==========================================
with aba_juri:
    st.header("Judicium Accusationis (Decisões de Encerramento)")
    
    decisao_juri = st.selectbox("Tipo de Decisão (Fase Sumária):", [
        "Pronúncia (Art. 413, CPP)", 
        "Impronúncia (Art. 414, CPP)", 
        "Absolvição Sumária (Art. 415, CPP)",
        "Desclassificação (Art. 419, CPP)"
    ])
    
    materialidade_indicios = st.text_area("Análise das Provas (Materialidade e Indícios suficientes de autoria):", height=150)
    qualificadoras = st.text_input("Qualificadoras sustentadas pelo MP (Para admissão ou decote):")
    
    if st.button("🔨 Gerar Decisão do Júri"):
        if materialidade_indicios:
            with st.spinner("Estruturando decisão sem excesso de linguagem..."):
                prompt_juri = f"""
                {REGRAS_GLOBAIS}
                Redija uma decisão de encerramento da primeira fase do rito do Tribunal do Júri.
                Decisão escolhida: {decisao_juri}.
                Provas analisadas: {materialidade_indicios}
                Qualificadoras: {qualificadoras}
                
                Instrução Crítica:
                Se for PRONÚNCIA, é ESTRITAMENTE PROIBIDO o excesso de eloquência (excesso de linguagem) para não influenciar os jurados (nulidade absoluta). Use termos como "há indícios", "a prova pericial aponta", limitando-se à admissibilidade da acusação.
                Analise se as qualificadoras são manifestamente improcedentes para decotá-las, ou se devem ir a plenário.
                """
                st.markdown(model.generate_content(prompt_juri).text)
        else:
            st.error("Preencha a análise das provas.")
