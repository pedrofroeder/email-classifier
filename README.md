# 📧 Email Classifier - Sistema de Classificação Inteligente de Emails

Sistema completo de classificação automática de emails usando IA (Claude API) com interface web responsiva.

Desenvolvido como parte do desafio técnico da **AutoU** para automatizar a triagem de emails em setores financeiros.

---

## 🚀 Demo Online

- **🌐 Aplicação:** https://email-classifier-front.vercel.app
- **🔌 API Backend:** https://email-classifier-api-h7rv.onrender.com
- **💚 Health Check:** https://email-classifier-api-h7rv.onrender.com/api/health
- **📦 Repositórios:**
  - Backend: https://github.com/pedrofroeder/email-classifier
  - Frontend: https://github.com/pedrofroeder/email-classifier-front

---

## 📋 Sobre o Projeto

Sistema desenvolvido para automatizar a classificação de emails corporativos em categorias (Produtivo/Improdutivo) e gerar respostas automáticas personalizadas usando inteligência artificial.

### ✨ Funcionalidades

- ✅ Classificação automática de emails em categorias
- ✅ Geração de respostas sugeridas com IA
- ✅ Upload de arquivos (.txt, .pdf) com drag-and-drop
- ✅ Inserção direta de texto
- ✅ Interface responsiva (mobile, tablet, desktop)
- ✅ Pré-processamento de texto com NLP
- ✅ API REST documentada

### 🎯 Categorias

**Produtivo:** Emails que requerem ação ou resposta específica
- Solicitações de suporte técnico
- Atualização sobre casos em aberto
- Dúvidas sobre o sistema

**Improdutivo:** Emails que não necessitam de ação imediata
- Mensagens de felicitações
- Agradecimentos genéricos
- Mensagens sociais

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.13.4**
- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - Comunicação com frontend
- **Anthropic Claude API 0.72.1** - Modelo de IA (Sonnet 4)
- **PyPDF2 3.0.1** - Processamento de PDFs
- **python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente
- **Gunicorn 21.2.0** - Servidor WSGI de produção

### Frontend
- **React 18** - Biblioteca UI
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS utilitário
- **JavaScript (ES6+)**

### Infraestrutura
- **Render.com** - Hospedagem do backend (Free Tier)
- **Vercel** - Hospedagem do frontend
- **GitHub** - Controle de versão

---

## 📦 Estrutura do Projeto
```
email-classifier/
├── app.py              # API Flask principal
├── classifier.py       # Lógica de classificação com IA
├── requirements.txt    # Dependências Python
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore
└── README.md

frontend/ (repositório separado)
├── src/
│   ├── App.jsx         # Componente principal React
│   ├── main.jsx        # Entry point
│   └── index.css       # Estilos globais com Tailwind
├── public/
├── index.html
├── package.json
└── vite.config.js
```

---

## 🚀 Configuração e Instalação

### Pré-requisitos
- Python 3.11+
- Conta na Anthropic (para API key)

### Backend - Instalação Local

1. **Clone o repositório:**
```bash
git clone https://github.com/pedrofroeder/email-classifier.git
cd email-classifier
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API Anthropic:
```env
ANTHROPIC_API_KEY=sk-ant-api03-sua_chave_aqui
PORT=5000
```

4. **Execute o servidor:**
```bash
python app.py
```

O servidor estará rodando em `http://localhost:5000`

---

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Obrigatória | Padrão |
|----------|-----------|-------------|--------|
| `ANTHROPIC_API_KEY` | Chave da API Claude (Anthropic) | Sim | - |
| `PORT` | Porta do servidor | Não | 5000 |

**Como obter a API key:**
1. Acesse https://console.anthropic.com
2. Crie uma conta ou faça login
3. Vá em Settings → API Keys
4. Gere uma nova chave

---

## 🧠 Arquitetura e Decisões Técnicas

### Few-Shot Learning

O sistema utiliza **Few-Shot Learning** para treinar o modelo Claude:

- ✅ 4 exemplos práticos (2 produtivos, 2 improdutivos)
- ✅ O modelo aprende padrões sem necessidade de dataset grande
- ✅ Alta precisão com poucos exemplos
- ✅ Adaptável a novos contextos

**Vantagens:**
- Rápido para implementar
- Não requer infraestrutura de ML complexa
- Fácil de ajustar e melhorar

### Processamento de Linguagem Natural (NLP)

Técnicas de pré-processamento aplicadas antes da classificação:

1. **Normalização:** Conversão para lowercase
2. **Remoção de stop words:** Palavras comuns em português
3. **Remoção de caracteres especiais:** Pontuação e números isolados
4. **Remoção de espaços múltiplos**

**Resultado:** Texto limpo focado nas palavras-chave relevantes para classificação.

### Padrão de Resposta JSON

A API do Claude é instruída a retornar JSON estruturado:
```json
{
  "categoria": "Produtivo ou Improdutivo",
  "resposta": "Resposta sugerida em português"
}
```

Com tratamento de fallback para parsing manual caso o JSON não seja perfeito.

---

## 📡 Documentação da API

### Base URL
```
Produção: https://email-classifier-api-h7rv.onrender.com
Local: http://localhost:5000
```

### Endpoints

#### `POST /api/classify`

Classifica um email e retorna categoria + resposta sugerida.

**Headers:**
- `Content-Type: application/json` (para texto)
- `Content-Type: multipart/form-data` (para arquivo)

**Body - Opção 1 (JSON):**
```json
{
  "text": "Olá, gostaria de saber o status do processo 12345. Faz 3 dias sem retorno."
}
```

**Body - Opção 2 (Form Data):**
```
file: arquivo.txt ou arquivo.pdf (máximo 5MB)
```

**Response 200 OK:**
```json
{
  "success": true,
  "categoria": "Produtivo",
  "resposta_sugerida": "Olá! Verificamos que seu processo 12345 está em análise pela equipe técnica. Previsão de retorno: 2 dias úteis. Agradecemos sua compreensão.",
  "texto_processado": "gostaria saber status processo"
}
```

**Response 400 Bad Request:**
```json
{
  "success": false,
  "error": "Email muito curto (mínimo 10 caracteres)"
}
```

#### `GET /api/health`

Verifica se a API está online.

**Response 200 OK:**
```json
{
  "status": "online",
  "service": "Email Classifier API"
}
```

---

## 🌐 Deploy

### Backend (Render)

**Plataforma:** Render.com (Free Tier)

**Configuração:**
```yaml
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

**Variáveis de ambiente:**
- `ANTHROPIC_API_KEY`: Configurada via dashboard do Render
- `PORT`: Injetada automaticamente pelo Render

⚠️ **Nota sobre Cold Start:** 

O plano gratuito do Render coloca o serviço em "sleep mode" após 15 minutos de inatividade. A primeira requisição após esse período pode levar ~30 segundos para "acordar" o servidor. Requisições subsequentes são instantâneas (1-2s).

**Para testar imediatamente:**
1. Acesse o health check: https://email-classifier-api-h7rv.onrender.com/api/health
2. Aguarde aparecer `{"status": "online"}`
3. Use a aplicação normalmente

---

## 🧪 Testes

### Testar Localmente
```bash
# Health check
curl http://localhost:5000/api/health

# Classificar texto
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"Olá, gostaria de saber o status do processo"}'

# Classificar arquivo
curl -X POST http://localhost:5000/api/classify \
  -F "file=@email.txt"
```

---

## 📊 Exemplos de Uso

### Email Produtivo

**Input:**
```
Olá,
Gostaria de saber o status do meu processo número 12345.
Faz 3 dias sem retorno.
Obrigado,
João Silva
```

**Output:**
```
Categoria: Produtivo
Resposta: Olá! Verificamos que seu processo 12345 está em análise pela 
equipe técnica. Previsão de retorno: 2 dias úteis. Agradecemos sua 
compreensão.
```

### Email Improdutivo

**Input:**
```
Olá equipe!
Desejo a todos um Feliz Natal e um próspero Ano Novo!
Abraços,
Maria
```

**Output:**
```
Categoria: Improdutivo
Resposta: Muito obrigado! Desejamos um Feliz Natal e um próspero Ano Novo 
para você também! 🎄
```

---

## 🐛 Troubleshooting

### Problema: ModuleNotFoundError

**Solução:** Instale as dependências
```bash
pip install -r requirements.txt
```

### Problema: Invalid API key

**Solução:** Verifique se a variável `ANTHROPIC_API_KEY` está configurada corretamente no `.env`

### Problema: CORS error no frontend

**Solução:** Certifique-se que o Flask-CORS está instalado e configurado no `app.py`

### Problema: Cold start demora muito

**Solução:** Normal no Render Free Tier. Acesse o `/api/health` antes de usar a aplicação.

---

## 📄 Licença

Este projeto foi desenvolvido como parte de um desafio técnico da **AutoU**.

---

## 🙏 Agradecimentos

- **AutoU** pela oportunidade do desafio
- **Anthropic** pela API do Claude
- Comunidade open-source pelas ferramentas utilizadas

-
