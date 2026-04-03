import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Orquestrador CNJ", page_icon="📊", layout="wide")
st.title("📊 Orquestrador Diário e Metas CNJ")
st.markdown("Módulo de triagem estratégica de acervo e emissão de atos formais automatizados.")
st.markdown("---")

# 2. Verificação de Segurança (Garante que a API Key foi inserida na página inicial)
if 'api_key' not in st.session_state:
    st.warning("⚠️ Atenção: Volte à página inicial e insira sua Chave API para ativar este módulo.")
    st.stop() # Interrompe a execução da página se não houver chave

# Configura o motor da IA
genai.configure(api_key=st.session_state['api_key'])
model = genai.GenerativeModel('gemini-1.5-pro')

# 3. Criação de Abas (Tabs) para organizar a tela
aba_triagem, aba_atos_formais = st.tabs(["📑 Triagem e KPIs (Painel CNJ)", "✉️ Gerador de Atos Formais"])

# ==========================================
# ABA 1: TRIAGEM E KPIs (Gestão de Acervo)
# ==========================================
with aba_triagem:
    st.header("Classificação Estratégica de Pendências")
    st.markdown("Cole sua lista de processos conclusos. O sistema aplicará a taxonomia do CNJ e destacará urgências.")
    
    lista_bruta = st.text_area("Lista de Processos (Copie do PJe/e-SAJ/Projudi):", height=200)
    
    if st.button("🚀 Processar Triagem e Metas"):
        if lista_bruta:
            with st.spinner("Analisando acervo à luz das Metas Nacionais do CNJ..."):
                prompt_triagem = f"""
                Atue como gestor de gabinete de alta performance. 
                Sua tarefa é analisar a seguinte lista de processos pendentes:
                {lista_bruta}
                
                1. Classifique cada um de acordo com as Tabelas Processuais Unificadas (TPU) do CNJ (Classe e Assunto).
                2. Identifique processos que possivelmente impactam as Metas Nacionais do CNJ (ex: processos antigos, improbidade, feminicídio).
                3. Crie uma tabela Markdown visualmente limpa com as colunas: 
                   | Nível de Urgência (🔴/🟡/🟢) | Classe/Assunto (CNJ) | Processo | Ação Necessária | Alerta de Meta CNJ |
                """
                resposta_triagem = model.generate_content(prompt_triagem)
                st.success("Triagem concluída!")
                st.markdown(resposta_triagem.text)
        else:
            st.error("Insira a lista de processos primeiro.")

# ==========================================
# ABA 2: GERADOR DE ATOS FORMAIS
# ==========================================
with aba_atos_formais:
    st.header("Automação de Comunicação Judicial")
    st.markdown("Geração de documentos rápidos seguindo os Manuais de Redação Oficial e ABNT.")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_ato = st.selectbox(
            "Tipo de Documento:", 
            ["Despacho Mero Expediente", "Ofício Externo", "Termo de Audiência (TA)"]
        )
        destinatario = st.text_input("Destinatário / Partes:")
    with col2:
        contexto_ato = st.text_area("Resumo do Ato (ex: 'Solicitar prontuário médico ao hospital', 'Designar audiência'):", height=100)
        
    if st.button("📝 Gerar Ato Formal"):
        if contexto_ato:
            with st.spinner("Redigindo documento em linguagem simples e padrão ABNT..."):
                prompt_ato = f"""
                Atue como Assessor Jurídico redigindo um {tipo_ato}.
                Destinatário/Partes: {destinatario}
                Contexto/Determinação: {contexto_ato}
                
                Regras Estritas:
                - Use formatação Markdown.
                - Aplique os padrões do Manual de Redação da Presidência da República e CNJ.
                - Seja direto, conciso e elimine qualquer "juridiquês" sem função.
                - Se for ofício, inclua cabeçalho, vocativo adequado e fecho padrão.
                """
                resposta_ato = model.generate_content(prompt_ato)
                st.markdown("### Documento Gerado:")
                st.markdown(resposta_ato.text)
        else:
            st.error("Descreva o contexto do ato para gerar o documento.")
