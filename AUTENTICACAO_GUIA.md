# 🔐 Sistema de Login — Dashboard MDL + Cantinho da Girafa

## 📋 Overview

Sistema completo de autenticação com **3 níveis de acesso**:
- **👑 Admin** — Gerencia usuários e visualiza dados completos
- **👤 User** — Visualiza dashboard (sem gerenciar usuários)
- **🔒 Login Obrigatório** — Acesso restrito apenas a usuários cadastrados

---

## 🚀 Como Usar

### **1. Acessar o Dashboard**

1. Abra `dashboard_login.html` no navegador
2. Faça login com suas credenciais
3. Será redirecionado automaticamente para `dashboard_consolidado.html`

### **2. Usuários de Demo (pré-cadastrados)**

**Admin:**
- Email: `admin@example.com`
- Senha: `admin123`
- Acesso: Completo (gerenciar usuários + dashboard)

**Usuário Comum:**
- Email: `user@example.com`
- Senha: `user123`
- Acesso: Apenas visualizar dashboard

---

## 📝 Funcionalidades

### **Aba de Login**
- Login com email e senha
- Validação de credenciais
- Mensagens de erro/sucesso
- Botão para mostrar/ocultar senha

### **Aba de Cadastro**
- Criar nova conta (aberto para qualquer pessoa)
- Validação de email
- Verificação de força de senha (mín. 6 caracteres)
- Confirmação de senha
- Prevenção de duplicatas

### **Aba Admin**
- Listar todos os usuários cadastrados
- Ver papel (Admin/User) de cada usuário
- Deletar usuários individualmente
- Botão para resetar para usuários de demo
- Apenas admins podem acessar

### **Dashboard Protegido**
- Exibe nome do usuário conectado no canto superior direito
- Botão "Sair" para fazer logout
- Redireciona para login se sessão expirar
- Dados consolidados MDL + Cantinho da Girafa

---

## 🔒 Segurança

### **Implementado:**
- ✅ Hash de senha (SHA-256 local)
- ✅ Validação de email
- ✅ Sessão via `sessionStorage` (expira ao fechar aba)
- ✅ Proteção de rota (redireciona para login se não autenticado)
- ✅ Isolamento por papel (Admin/User)

### **⚠️ Notas de Segurança:**

> **Para uso em PRODUÇÃO, você DEVE:**
>
> 1. **Mover autenticação para backend** (Node.js, Python, PHP)
> 2. **Usar bcrypt ou Argon2** para hash de senha (não SHA-256)
> 3. **Implementar JWT tokens** em vez de sessionStorage
> 4. **Usar HTTPS** obrigatoriamente
> 5. **Implementar rate limiting** contra força bruta
> 6. **Nunca armazenar senhas em localStorage/sessionStorage**

Atualmente, este sistema é **seguro para uso local/intranet**, mas não para produção pública.

---

## 📁 Arquivos

| Arquivo | Função |
|---------|--------|
| `dashboard_login.html` | 🔐 Login, cadastro e painel admin |
| `dashboard_consolidado.html` | 📊 Dashboard protegido (requer login) |
| `dashboard_consolidated_data.json` | 📈 Dados em JSON (metadata) |

---

## 🔄 Fluxo de Autenticação

```
┌─────────────────────────────────────────────────┐
│  Acessar dashboard_consolidado.html              │
└────────────────┬────────────────────────────────┘
                 │
        Verificar sessionStorage
                 │
         ┌───────┴────────┐
         │                │
    ✅ Autenticado?  ❌ Não autenticado?
         │                │
    Exibir Dashboard  Redirecionar para Login
         │                │
    ┌────────────┐    ┌──────────────┐
    │ Login ✓    │    │ Login Page   │
    │ Dashboard  │    │ + Cadastro   │
    │ Dados      │    │ + Admin      │
    └────────────┘    └──────────────┘
```

---

## 🛠️ Como Adicionar Usuários Manualmente

### **Opção 1: Via Painel Admin (Recomendado)**
1. Acesse `dashboard_login.html`
2. Aba "Admin"
3. Faça login como admin
4. Novo usuário se cadastra normalmente
5. Admin gerencia na aba "Admin"

### **Opção 2: Console do Navegador (Dev)**
```javascript
// Abra o console (F12 → Console)
const users = JSON.parse(localStorage.getItem('users') || '[]');
const newUser = {
    id: Math.max(...users.map(u => u.id), 0) + 1,
    name: 'Seu Nome',
    email: 'seu@email.com',
    password: '1a2b3c4d', // Hash SHA-256 (use hashPassword('sua_senha') para gerar)
    role: 'user',
    createdAt: new Date().toISOString()
};
users.push(newUser);
localStorage.setItem('users', JSON.stringify(users));
```

---

## 🎯 Próximos Passos para Produção

### **1. Backend Básico (Node.js + Express)**
```javascript
// exemplo de rota de login
app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    const validPassword = await bcrypt.compare(password, user.password);
    
    if (validPassword) {
        const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
        res.json({ token });
    }
});
```

### **2. Banco de Dados**
- MongoDB, PostgreSQL ou MySQL
- Tabela `users` com: id, name, email, password_hash, role, created_at

### **3. Implantação**
- GitHub Pages (frontend)
- Heroku, Railway, Vercel (backend)
- Domínio customizado com HTTPS

---

## 📱 Compatibilidade

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Mobile (iOS Safari, Chrome Android)
- ✅ Sem dependências externas (vanilla JS)
- ✅ Funciona offline (localStorage)

---

## ❓ Dúvidas Frequentes

**P: A senha está realmente segura?**
R: Localmente, sim (hash SHA-256). Em produção, use bcrypt no backend.

**P: O que acontece se fechar o navegador?**
R: A sessão expira (sessionStorage é deletada). Precisa fazer login novamente.

**P: Posso resetar um usuário?**
R: Sim, admin acessa aba "Admin" → "Resetar para Demo" (deleta todos e restaura demo).

**P: Como faço backup dos usuários?**
R: `localStorage.getItem('users')` exporta JSON. Cole em um arquivo .json.

---

## 📞 Suporte

Para problemas:
1. Abra Console (F12)
2. Verifique se há erros
3. Limpe localStorage: `localStorage.clear()`
4. Reinicialize a página

---

**Criado em:** 26 de maio de 2026
**Versão:** 1.0 (Local/Intranet)
**Última atualização:** Dashboard consolidado + Windsor.ai
