import os
import re
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def preprocess_text(text):
    """
    Pré-processa o texto do email usando técnicas de NLP.
    """
    stop_words = {
        'a', 'o', 'e', 'é', 'de', 'da', 'do', 'em', 'um', 'uma', 'os', 'as', 
        'dos', 'das', 'para', 'com', 'por', 'ao', 'aos', 'à', 'às', 'no', 'na',
        'nos', 'nas', 'se', 'que', 'ou', 'mais', 'muito', 'já', 'também', 
        'só', 'pelo', 'pela', 'até', 'isso', 'esse', 'essa', 'este', 'esta',
        'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas', 'meu', 'minha',
        'seu', 'sua', 'nosso', 'nossa', 'sem', 'sob', 'sobre', 'então'
    }
    
    text_lower = text.lower()
    
    text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
    
    text_clean = re.sub(r'\b\d+\b', '', text_clean)
    
    words = text_clean.split()
    filtered_words = [word for word in words if word and word not in stop_words]
    
    processed_text = ' '.join(filtered_words)
    
    return processed_text


def classify_email(email_text):
    """
    Classifica o email usando Claude AI com técnicas de Few-Shot Learning.
    
    Returns:
        dict: Contém categoria, resposta sugerida e texto processado
    """
    
    if not email_text or len(email_text.strip()) < 10:
        raise ValueError("Email muito curto. Mínimo de 10 caracteres.")
    
    processed_text = preprocess_text(email_text)
    
    prompt = f"""
Você é um assistente especializado em classificar emails de uma empresa financeira.

=== EXEMPLOS DE TREINAMENTO (Few-Shot Learning) ===

EXEMPLO 1 - Email Improdutivo:
Email: "Olá equipe! Desejo um Feliz Natal a todos e um próspero Ano Novo! Abraços."
CATEGORIA: Improdutivo
RESPOSTA: Muito obrigado! Desejamos um Feliz Natal e um próspero Ano Novo para você também! 🎄

EXEMPLO 2 - Email Produtivo:
Email: "Bom dia, gostaria de saber o status do processo 12345. Já faz 5 dias sem retorno."
CATEGORIA: Produtivo
RESPOSTA: Olá! Verificamos que seu processo 12345 está em análise pela equipe técnica. Previsão de retorno: 2 dias úteis. Agradecemos sua compreensão.

EXEMPLO 3 - Email Improdutivo:
Email: "Muito obrigado pela ajuda de ontem! Vocês são ótimos!"
CATEGORIA: Improdutivo
RESPOSTA: Ficamos felizes em ajudar! Estamos à disposição sempre que precisar. 😊

EXEMPLO 4 - Email Produtivo:
Email: "Preciso urgentemente alterar meu endereço de cobrança. Como proceder?"
CATEGORIA: Produtivo
RESPOSTA: Olá! Para alterar seu endereço, acesse sua conta no sistema ou responda este email com: nome completo, CPF e novo endereço completo. Processaremos em até 24h.

=== AGORA ANALISE ESTE EMAIL ===

EMAIL ORIGINAL:
{email_text}

TEXTO PRÉ-PROCESSADO (após NLP):
{processed_text}

=== INSTRUÇÕES ===

Baseado nos exemplos acima, classifique como:

- PRODUTIVO: Requer ação, resposta específica, suporte técnico, atualização de status, dúvidas, solicitações
- IMPRODUTIVO: Apenas felicitação, agradecimento genérico, mensagem social, sem necessidade de ação

Responda APENAS com JSON neste formato (sem texto extra):
{{
  "categoria": "Produtivo ou Improdutivo",
  "resposta": "sua resposta sugerida em português, profissional e cordial"
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    response_text = response_text.replace('```json', '').replace('```', '').strip()
    
    try:
        resultado = json.loads(response_text)
        categoria = resultado.get('categoria', 'Desconhecido')
        resposta_sugerida = resultado.get('resposta', 'Resposta não disponível')
    except:
        categoria_match = re.search(r'"categoria":\s*"([^"]+)"', response_text)
        resposta_match = re.search(r'"resposta":\s*"([^"]+)"', response_text)
        
        if categoria_match and resposta_match:
            categoria = categoria_match.group(1)
            resposta_sugerida = resposta_match.group(1)
        else:
            categoria = "Desconhecido"
            resposta_sugerida = "Não foi possível gerar resposta automática."
    
    return {
        "categoria": categoria,
        "resposta_sugerida": resposta_sugerida,
        "texto_processado": processed_text
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO SISTEMA DE CLASSIFICAÇÃO")
    print("=" * 60)
    
    # Teste 1: Email Produtivo
    email_teste_1 = """
    Olá,
    Gostaria de saber o status do meu processo número 12345.
    Faz 3 dias sem retorno.
    Obrigado,
    João Silva
    """
    
    print("\n📧 TESTE 1 (Produtivo):")
    print(email_teste_1)
    
    resultado_1 = classify_email(email_teste_1)
    print(f"\n✅ Categoria: {resultado_1['categoria']}")
    print(f"💬 Resposta: {resultado_1['resposta_sugerida']}")
    
    print("\n" + "=" * 60)
    
    # Teste 2: Email Improdutivo
    email_teste_2 = """
    Olá equipe!
    Desejo a todos um Feliz Natal!
    Abraços,
    Maria
    """
    
    print("\n📧 TESTE 2 (Improdutivo):")
    print(email_teste_2)
    
    resultado_2 = classify_email(email_teste_2)
    print(f"\n✅ Categoria: {resultado_2['categoria']}")
    print(f"💬 Resposta: {resultado_2['resposta_sugerida']}")
    
    print("\n" + "=" * 60)