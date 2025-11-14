import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from classifier import classify_email
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extrai texto de um arquivo PDF"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


@app.route('/api/classify', methods=['POST'])
def classify():
    """
    Endpoint que recebe email e retorna classificação
    
    Aceita:
    - Arquivo TXT ou PDF
    - Texto direto via JSON
    """
    try:
        email_text = ""
        
        # Verifica se veio um arquivo
        if 'file' in request.files:
            file = request.files['file']
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Extrai texto dependendo do formato
                if filename.endswith('.pdf'):
                    email_text = extract_text_from_pdf(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        email_text = f.read()
                
                # Remove o arquivo temporário
                os.remove(file_path)
            else:
                return jsonify({
                    'success': False,
                    'error': 'Arquivo inválido. Use .txt ou .pdf'
                }), 400
        
        # Se não veio arquivo, verifica se veio texto
        elif request.is_json and 'text' in request.json:
            email_text = request.json['text']
        
        # Se não tem email, retorna erro
        if not email_text:
            return jsonify({
                'success': False,
                'error': 'Nenhum email fornecido'
            }), 400
        
        # Validação básica de tamanho
        if len(email_text.strip()) < 10:
            return jsonify({
                'success': False,
                'error': 'Email muito curto (mínimo 10 caracteres)'
            }), 400
        
        # Classifica o email
        resultado = classify_email(email_text)
        
        # Retorna o resultado
        return jsonify({
            'success': True,
            'categoria': resultado['categoria'],
            'resposta_sugerida': resultado['resposta_sugerida'],
            'texto_processado': resultado['texto_processado']
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'service': 'Email Classifier API'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    print("🚀 Servidor iniciado!")
    print(f"📡 Rodando na porta: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)