# ARQUIVO: data/dicionario_ritos.py

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

# Adicione aqui os demais ritos (Júri, Execução Fiscal, ECA) no futuro.
