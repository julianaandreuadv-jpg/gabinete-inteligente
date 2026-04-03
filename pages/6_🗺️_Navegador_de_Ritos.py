import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Navegador de Ritos", page_icon="🗺️", layout="wide")
st.title("🗺️ Navegador Visual de Ritos Processuais (CNJ / 2026)")
st.markdown("Máquina de Estados: Visualize a cronologia, prazos fatais e opções hermenêuticas.")
st.markdown("---")

# 2. Cláusula de Guarda
if 'api_key' not in st.session_state:
    st.warning("⚠️ Atenção: Volte à página inicial e insira sua Chave API para ativar este módulo.")
    st.stop()

# 3. Nossos "Bancos de Dados" de Ritos (Dicionários)
# RITO 1: Maria da Penha (que construímos juntos)
rito_maria_da_penha = {
    "1. Fase Cautelar (Urgência)": {
        "status": "🔴 CRÍTICO", "prazo": "48 horas (Art. 18, I, LMP)",
        "acoes": ["Deferir MPU", "Indeferir MPU"],
        "alerta": "Súmula 589 STJ: Palavra da vítima tem especial relevância."
    },
    "2. Recebimento da Denúncia": {
        "status": "🟡 ALTO", "prazo": "Imediato",
        "acoes": ["Receber e Citar", "Rejeitar"],
        "alerta": "Súmula 542 STJ: Lesão corporal é ação incondicionada."
    },
    "3. Instrução e Sentença": {
        "status": "🟢 NORMAL", "prazo": "Após alegações finais",
        "acoes": ["Condenar e Fixar Danos Morais", "Absolver"],
        "alerta": "Tema 983 STJ: Obrigatório fixar dano moral se houver pedido."
    }
}

# RITO 2: Tribunal do Júri (Fase 1)
rito_juri = {
    "1. Recebimento e Resposta à Acusação": {
        "status": "🟢 NORMAL", "prazo": "10 dias para Defesa",
        "acoes": ["Absolvição Sumária Antecipada (Art. 397, CPP)", "Designar AIJ"],
        "alerta": "Verificar nulidades preliminares."
    },
    "2. Audiência de Instrução (AIJ)": {
        "status": "🟡 ALTO", "prazo": "Prazo em dobro se réu preso",
        "acoes": ["Ouvir testemunhas", "Interrogatório (Último ato)"],
        "alerta": "Cuidado com uso de algemas (Súmula Vinculante 11)."
    },
    "3. Decisão de Encerramento (Pronúncia)": {
        "status": "🔴 CRÍTICO", "prazo": "Logo após alegações finais",
        "acoes": ["Pronunciar (Art. 413)", "Impronunciar", "Desclassificar", "Absolver Sumariamente"],
        "alerta": "PROIBIDO excesso de eloquência. Avalie se qualificadoras são manifestamente improcedentes."
    }
}

# RITO 3: Execução Fiscal (Fazenda Pública)
rito_execucao_fiscal = {
    "1. Despacho Inicial e Citação": {
        "status": "🟢 NORMAL", "prazo": "Citação em 5 dias (Art. 8º, LEF)",
        "acoes": ["Citar, Pagar ou Garantir a Execução"],
        "alerta": "A citação interrompe a prescrição (Art. 174, CTN)."
    },
    "2. Garantia do Juízo / Penhora": {
        "status": "🟡 ALTO", "prazo": "Após citação sem pagamento",
        "acoes": ["Penhora via Sisbajud", "Penhora de Imóveis"],
        "alerta": "Ordem de preferência: Dinheiro em primeiro lugar (Art. 11, LEF)."
    },
    "3. Embargos à Execução Fiscal": {
        "status": "🔴 CRÍTICO", "prazo": "30 dias após garantia",
        "acoes": ["Receber Embargos (com ou sem efeito suspensivo)", "Rejeitar Liminarmente"],
        "alerta": "Sem garantia do juízo, não se admitem embargos (Art. 16, § 1º, LEF)."
    }
}

# 4. A Interface de Seleção
competencia = st.selectbox("Selecione o Rito Processual para Visualização:", [
    "Violência Doméstica (Maria da Penha)", 
    "Tribunal do Júri (Judicium Accusationis)", 
    "Execução Fiscal (LEF)"
])

# 5. O Motor de Renderização (Loop Dinâmico)
st.markdown("---")

if competencia == "Violência Doméstica (Maria da Penha)":
    dicionario_atual = rito_maria_da_penha
elif competencia == "Tribunal do Júri (Judicium Accusationis)":
    dicionario_atual = rito_juri
else:
    dicionario_atual = rito_execucao_fiscal

# Este 'for' varre o dicionário selecionado e desenha as caixas na tela
for fase, dados in dicionario_atual.items():
    if dados["status"] == "🔴 CRÍTICO":
        st.error(f"### {fase}")
    elif dados["status"] == "🟡 ALTO":
        st.warning(f"### {fase}")
    else:
        st.success(f"### {fase}")
        
    colA, colB = st.columns([1, 2])
    with colA:
        st.markdown(f"**Nível:** {dados['status']}")
        st.markdown(f"⏱️ **Prazo Legal:** {dados['prazo']}")
    with colB:
        st.markdown("**Ações do Juiz:**")
        for acao in dados["acoes"]:
            st.markdown(f"- {acao}")
        st.info(f"**Jurisprudência 2026:** {dados['alerta']}")
    
    st.markdown("---")
