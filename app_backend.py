"""
Flask Backend para Dashboard com Autenticação Segura
Instalar: pip install flask flask-cors bcrypt pyjwt python-dotenv
Executar: python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import jwt
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')
DB_FILE = 'users_db.json'  # Substituir por banco de dados real em produção

# ==================== UTILS ====================

def load_users():
    """Carrega usuários do arquivo JSON"""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Salva usuários no arquivo JSON"""
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash seguro de senha com bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verifica senha contra hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id, user_email, user_role):
    """Cria JWT token"""
    payload = {
        'user_id': user_id,
        'email': user_email,
        'role': user_role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Valida e decodifica JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator para rotas protegidas"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token ausente'}), 401
        
        # Remover "Bearer " se presente
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token inválido'}), 401
        
        request.user = payload
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator para rotas que requerem admin"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user.get('role') != 'admin':
            return jsonify({'error': 'Acesso apenas para admin'}), 403
        return f(*args, **kwargs)
    return decorated

# ==================== ROTAS PÚBLICAS ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Cadastrar novo usuário"""
    data = request.get_json()
    
    # Validações
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400
    
    if len(data.get('password', '')) < 6:
        return jsonify({'error': 'Senha deve ter mínimo 6 caracteres'}), 400
    
    # Verificar duplicata
    users = load_users()
    if any(u['email'] == data['email'] for u in users):
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Criar novo usuário
    new_user = {
        'id': max([u['id'] for u in users], default=0) + 1,
        'name': data['name'],
        'email': data['email'],
        'password': hash_password(data['password']),
        'role': 'user',
        'created_at': datetime.utcnow().isoformat()
    }
    
    users.append(new_user)
    save_users(users)
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'user': {
            'id': new_user['id'],
            'name': new_user['name'],
            'email': new_user['email'],
            'role': new_user['role']
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login com email e senha"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email e senha requeridos'}), 400
    
    users = load_users()
    user = next((u for u in users if u['email'] == data['email']), None)
    
    if not user or not verify_password(data['password'], user['password']):
        return jsonify({'error': 'Email ou senha inválidos'}), 401
    
    token = create_token(user['id'], user['email'], user['role'])
    
    return jsonify({
        'message': 'Login bem-sucedido',
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        }
    }), 200

# ==================== ROTAS PROTEGIDAS ====================

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    """Obter perfil do usuário autenticado"""
    users = load_users()
    user = next((u for u in users if u['id'] == request.user['user_id']), None)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'role': user['role'],
        'created_at': user['created_at']
    }), 200

@app.route('/api/change-password', methods=['POST'])
@token_required
def change_password():
    """Mudar senha do usuário autenticado"""
    data = request.get_json()
    
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Senhas requeridas'}), 400
    
    users = load_users()
    user = next((u for u in users if u['id'] == request.user['user_id']), None)
    
    if not user or not verify_password(data['old_password'], user['password']):
        return jsonify({'error': 'Senha atual inválida'}), 401
    
    # Atualizar senha
    user['password'] = hash_password(data['new_password'])
    save_users(users)
    
    return jsonify({'message': 'Senha atualizada com sucesso'}), 200

# ==================== ROTAS ADMIN ====================

@app.route('/api/users', methods=['GET'])
@admin_required
def list_users():
    """Listar todos os usuários (admin)"""
    users = load_users()
    return jsonify({
        'users': [
            {
                'id': u['id'],
                'name': u['name'],
                'email': u['email'],
                'role': u['role'],
                'created_at': u['created_at']
            }
            for u in users
        ]
    }), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Deletar usuário (admin)"""
    if user_id == request.user['user_id']:
        return jsonify({'error': 'Não pode deletar sua própria conta'}), 400
    
    users = load_users()
    users = [u for u in users if u['id'] != user_id]
    save_users(users)
    
    return jsonify({'message': 'Usuário deletado'}), 200

@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    """Atualizar papel de usuário (admin)"""
    data = request.get_json()
    role = data.get('role')
    
    if role not in ['admin', 'user']:
        return jsonify({'error': 'Papel inválido'}), 400
    
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    user['role'] = role
    save_users(users)
    
    return jsonify({'message': f'Papel atualizado para {role}'}), 200

# ==================== ROTAS ADMIN - DADOS ====================

@app.route('/api/data/mdl', methods=['GET'])
@token_required
def get_mdl_data():
    """Obter dados MDL (requer login)"""
    return jsonify({
        'account_id': '1124246161345381',
        'status': 'ATIVO (MCP)',
        'campaigns_active': 1,
        'campaign': '3 Dias de Loucura'
    }), 200

@app.route('/api/data/girafa', methods=['GET'])
@token_required
def get_girafa_data():
    """Obter dados Cantinho da Girafa (requer login)"""
    return jsonify({
        'account_id': '811077953131064',
        'status': 'ATIVO (Windsor)',
        'campaigns_active': 5,
        'spend_7d': 754.91,
        'impressions': 255171,
        'reach': 164514,
        'clicks': 851
    }), 200

# ==================== INICIALIZAR USUÁRIOS DE DEMO ====================

@app.route('/api/init-demo', methods=['POST'])
def init_demo():
    """Resetar para usuários de demo (dev only)"""
    demo_users = [
        {
            'id': 1,
            'name': 'Diego Cordeiro',
            'email': 'admin@example.com',
            'password': hash_password('admin123'),
            'role': 'admin',
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': 2,
            'name': 'Usuário Demo',
            'email': 'user@example.com',
            'password': hash_password('user123'),
            'role': 'user',
            'created_at': datetime.utcnow().isoformat()
        }
    ]
    save_users(demo_users)
    return jsonify({'message': 'Demo users criados'}), 200

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check do servidor"""
    return jsonify({'status': 'OK', 'timestamp': datetime.utcnow().isoformat()}), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Rota não encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Inicializar usuários de demo se não existirem
    if not os.path.exists(DB_FILE):
        init_demo()
    
    print("🚀 Backend Flask iniciado!")
    print("📍 Acesso: http://localhost:5000")
    print("📚 API Docs: http://localhost:5000/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
