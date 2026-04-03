import google.generativeai as genai
import streamlit as st
from core.prompts_globais import REGRAS_ABNT_E_CNJ

def configurar_gemini(api_key):
    """Inicializa a conexão com o Google Gemini."""
    genai.configure(api_key=api_key)
    # Utilizamos o modelo pro para tarefas complexas de raciocínio jurídico
    return genai.GenerativeModel('gemini-1.5-pro')

def gerar_peca_juridica(modelo, instrucao_especifica, fatos):
    """Função central que junta a instrução da página com as regras globais."""
    prompt_completo = f"""
    {REGRAS_ABNT_E_CNJ}
    
    INSTRUÇÕES ESPECÍFICAS DESTA TAREFA:
    {instrucao_especifica}
    
    DADOS DO CASO CONCRETO:
    {fatos}
    """
    
    resposta = modelo.generate_content(prompt_completo)
    return resposta.text
