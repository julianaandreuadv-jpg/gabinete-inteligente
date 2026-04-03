import streamlit as st
import google.generativeai as genai
from datetime import timedelta

# 1. Configuração da Página
st.set_page_config(page_title="Infância e ECA", page_icon="👶", layout="wide")
st.title("👶 Motor da Infância e Juventude (Infracional)")
st.markdown("Gestão de internações provisórias, sentenças socioeducativas e execução (ECA).")
st.markdown("---")

# 2. Cláusula de Guarda (Segurança)
if 'api_key' not in st.session_state:
    st.warning("⚠️ Atenção: Volte à página inicial e insira sua Chave API para ativar este módulo.")
    st.stop()

# Conecta o cérebro da IA
genai.configure(api_key=st.session_state['api_key'])
model = genai.GenerativeModel('gemini-1.5-pro')

# Regras Globais do Kernel + Terminologia do ECA
REGRAS_GLOBAIS = """
- Aplique o Pacto pela Linguagem Simples (CNJ).
- Use terminologia estrita do ECA: "Representação" (não denúncia), "Ato Infracional" (não crime), "Adolescente" (não réu), "Internação/Medida Socioeducativa" (não prisão/pena).
- Aplique o Princípio da Proteção Integral e Prioridade Absoluta.
"""

# 3. Organização Visual em Abas (Tabs)
aba_cautelar, aba_sentenca, aba_execucao = st.tabs([
    "🔒 Internação Provisória", 
    "📜 Sentença de Conhecimento", 
    "⚙️ Execução de MSE e PIA"
])

# ==========================================
# ABA 1: INTERNAÇÃO PROVISÓRIA (Fase Inicial)
# ==========================================
with aba_cautelar:
    st.header("Decisão de Internação Provisória (Art. 108, ECA)")
    
    col1, col2 = st.columns(2)
    with col1:
        adolescente = st.text_input("Iniciais do Adolescente (Preserve a identidade - Art. 143, ECA):")
        ato_infracional = st.text_input("Ato Infracional análogo a:")
    with col2:
        data_apreensao = st.date_input("Data da Apreensão:")
        # Calcula automaticamente o prazo fatal (45 dias)
        prazo_fatal = data_apreensao + timedelta(days=45)
        st.error(f"⏳ Prazo Máximo de Internação: {prazo_fatal.strftime('%d/%m/%Y')}")
        
    fatos_internacao = st.text_area("Fundamentos (Grave ameaça/violência, reiteração ou descumprimento de medida anterior):", height=100)
    
    if st.button("🔒 Gerar Decisão Cautelar (ECA)"):
        if fatos_internacao:
            with st.spinner("Analisando requisitos estritos do Art. 122 do ECA..."):
                prompt_internacao = f"""
                {REGRAS_GLOBAIS}
                Redija decisão interlocutória sobre Internação Provisória de adolescente infrator.
                Adolescente: {adolescente}. Ato Infracional: {ato_infracional}.
                Fundamentos: {fatos_internacao}.
                
                Instruções Críticas:
                - A internação é medida excepcional. Fundamente estritamente nas hipóteses taxativas do Art. 122 do ECA.
                - No dispositivo, decrete a internação provisória consignando o prazo MÁXIMO IMPRORROGÁVEL de 45 dias, determinando a expedição da guia respectiva.
                """
                st.markdown(model.generate_content(prompt_internacao).text)
        else:
            st.error("Insira os fundamentos para a decisão.")

# ==========================================
# ABA 2: SENTENÇA SOCIOEDUCATIVA
# ==========================================
with aba_sentenca:
    st.header("Sentença e Aplicação de Medida Socioeducativa (MSE)")
    
    fatos_sentenca = st.text_area("Síntese da Instrução e Provas:", height=100)
    mse_aplicada = st.selectbox("Medida Socioeducativa a ser aplicada:", [
        "Advertência (Art. 115)", 
        "Reparação do Dano (Art. 116)", 
        "Prestação de Serviços à Comunidade - PSC (Art. 117)", 
        "Liberdade Assistida - LA (Art. 118)", 
        "Semiliberdade (Art. 120)", 
        "Internação (Art. 121)"
    ])
    
    if st.button("⚖️ Compilar Sentença ECA"):
        if fatos_sentenca:
            with st.spinner("Estruturando sentença e avaliando proporcionalidade da medida..."):
                prompt_sentenca = f"""
                {REGRAS_GLOBAIS}
                Redija Sentença julgando procedente a representação para aplicar medida socioeducativa.
                Provas e Fatos: {fatos_sentenca}.
                MSE escolhida pelo magistrado: {mse_aplicada}.
                
                Instruções:
                - Fundamente a escolha da medida com base na capacidade de cumpri-la, nas circunstâncias e na gravidade da infração (Art. 112, §1º, ECA).
                - Estrutura ABNT: I - Relatório Histórico, II - Fundamentação (Materialidade e Autoria), III - Aplicação da Medida (Proporcionalidade), IV - Dispositivo.
                """
                st.markdown(model.generate_content(prompt_sentenca).text)
        else:
            st.error("Descreva a instrução processual.")

# ==========================================
# ABA 3: EXECUÇÃO SOCIOEDUCATIVA E PIA
# ==========================================
with aba_execucao:
    st.header("Vara de Execução de MSE (Avaliação do PIA)")
    
    decisao_execucao = st.selectbox("Natureza da Decisão na Execução:", [
        "Aprovação do Plano Individual de Atendimento (PIA)",
        "Progressão de Medida (ex: Internação para LA)",
        "Regressão de Medida (Descumprimento reiterado)",
        "Extinção da Medida (Cumprimento, Maioridade ou Prescrição)"
    ])
    
    relatorio_tecnico = st.text_area("Resumo do Relatório Técnico da Equipe Multidisciplinar:", height=120)
    
    if st.button("⚙️ Gerar Decisão de Execução"):
        if relatorio_tecnico:
            with st.spinner("Aplicando regras de execução e jurisprudência (Súmula 338 STJ)..."):
                prompt_execucao = f"""
                {REGRAS_GLOBAIS}
                Redija uma decisão em sede de Execução de Medida Socioeducativa.
                Decisão: {decisao_execucao}.
                Relatório da Equipe Técnica: {relatorio_tecnico}.
                
                Instruções Críticas:
                - Se envolver prescrição, aplique obrigatoriamente a Súmula 338 do STJ (a prescrição penal é aplicável às medidas socioeducativas).
                - A base da decisão deve ser o Princípio da Brevidade e Excepcionalidade.
                - Refira-se à importância do trabalho da equipe técnica (psicólogos/assistentes sociais) na evolução do socioeducando.
                """
                st.markdown(model.generate_content(prompt_execucao).text)
        else:
            st.error("Cole o resumo do relatório da equipe técnica.")
