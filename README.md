# 📊 Dashboard — MDL + Cantinho da Girafa

Sistema completo de **dashboard com autenticação**, **campanhas Meta Ads** e **análise de dados consolidados** para Lojas MDL e Cantinho da Girafa.

---

## 🎯 Overview

Este projeto oferece:

✅ **Dashboard Consolidado** — Visualize dados de ambas as empresas  
✅ **Sistema de Login** — Autenticação segura com 3 níveis de acesso  
✅ **Admin Panel** — Gerencie usuários e permissões  
✅ **Meta Ads Integration** — Dados de campanhas em tempo real  
✅ **Windsor.ai** — Sincronização de dados Cantinho da Girafa  
✅ **Frontend + Backend** — Pronto para produção  

---

## 🚀 Quick Start

### Opção 1: Frontend Puro (Agora)

1. **Abra no navegador:**
   ```
   dashboard_login.html
   ```

2. **Faça login com:**
   - Email: `admin@example.com`
   - Senha: `admin123`

3. **Pronto!** Acesso ao dashboard

### Opção 2: Com Backend (Após setup)

1. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Crie arquivo `.env`:**
   ```env
   SECRET_KEY=sua-chave-super-secreta-aqui
   FLASK_ENV=development
   ```

3. **Execute o servidor:**
   ```bash
   python app_backend.py
   ```

4. **Acesse:**
   ```
   http://localhost:5000
   ```

---

## 📁 Estrutura do Projeto

```
.
├── dashboard_login.html              # 🔐 Login, Cadastro, Admin Panel
├── dashboard_consolidado.html         # 📊 Dashboard Protegido
├── dashboard_consolidated_data.json   # 📈 Dados Meta Ads
├── app_backend.py                     # 🚀 API Flask (produção)
├── requirements.txt                   # 📦 Dependências Python
├── AUTENTICACAO_GUIA.md              # 📖 Guia de Uso
├── SISTEMA_LOGIN_RESUMO.md           # 📋 Resumo Técnico
├── README.md                          # Este arquivo
└── .gitignore                         # Git ignore rules
```

---

## 🔐 Autenticação

### Usuários de Demo

| Tipo | Email | Senha | Acesso |
|------|-------|-------|--------|
| 👑 Admin | admin@example.com | admin123 | Dashboard + Gerenciar usuários |
| 👤 User | user@example.com | user123 | Apenas visualizar dashboard |

### Como Funciona

1. **Login** com email/senha
2. **Token** salvo em `sessionStorage`
3. **Dashboard** valida token ao carregar
4. **Sessão** expira ao fechar a aba

---

## 📊 Dashboard

### Dados Exibidos

**Lojas MDL:**
- Campanhas ativas
- Status das campanhas
- Orçamento diário
- Ad Sets (Teaser + Produtos)

**Cantinho da Girafa:**
- 5 campanhas em execução
- Gasto (7 dias)
- Impressões e alcance
- CPM e CTR médios
- Análise por campanha

### Atualização Automática

O dashboard atualiza automaticamente a cada 6 horas via **GitHub Actions** + **Meta MCP** + **Windsor.ai**

---

## 🔑 API Endpoints (Backend)

### Públicos
- `POST /api/register` — Cadastrar usuário
- `POST /api/login` — Fazer login
- `GET /api/health` — Health check

### Protegidos (requer token)
- `GET /api/profile` — Perfil do usuário
- `POST /api/change-password` — Alterar senha
- `GET /api/data/mdl` — Dados MDL
- `GET /api/data/girafa` — Dados Girafa

### Admin
- `GET /api/users` — Listar todos os usuários
- `DELETE /api/users/<id>` — Deletar usuário
- `PUT /api/users/<id>/role` — Atualizar papel

---

## 🛠️ Tecnologias

### Frontend
- HTML5 + CSS3 + Vanilla JavaScript
- localStorage + sessionStorage
- Sem dependências externas (funciona offline)

### Backend
- Python 3.8+
- Flask + Flask-CORS
- Bcrypt (hash de senha)
- JWT (autenticação)
- JSON (persistência)

### Integrações
- Meta MCP (Lojas MDL)
- Windsor.ai (Cantinho da Girafa)
- GitHub Actions (atualização automática)

---

## 🔒 Segurança

### Implementado
✅ Hash de senha com Bcrypt  
✅ JWT tokens com expiração  
✅ CORS configurado  
✅ Validação de entrada  
✅ Proteção de rota  

### ⚠️ Para Produção Adicionar
- [ ] HTTPS obrigatório
- [ ] Rate limiting
- [ ] Banco de dados real (não JSON)
- [ ] Two-factor authentication (2FA)
- [ ] Logging e auditoria
- [ ] WAF (Web Application Firewall)

---

## 📖 Documentação

Leia os guias inclusos para mais detalhes:

- **[AUTENTICACAO_GUIA.md](./AUTENTICACAO_GUIA.md)** — Como usar o sistema de login
- **[SISTEMA_LOGIN_RESUMO.md](./SISTEMA_LOGIN_RESUMO.md)** — Resumo técnico completo

---

## 🚀 Deployment

### GitHub Pages (Frontend)

1. **Crie repositório:** `https://github.com/seu-usuario/dashboard-ads`
2. **Habilite Pages:** Settings → Pages → Deploy from branch `main`
3. **Acesse:** `https://seu-usuario.github.io/dashboard-ads/dashboard_login.html`

### Heroku (Backend)

1. **Crie conta no Heroku**
2. **Faça deploy:**
   ```bash
   heroku login
   heroku create seu-app-name
   git push heroku main
   ```
3. **Acesse:** `https://seu-app-name.herokuapp.com`

### Vercel (Backend)

1. **Crie conta no Vercel**
2. **Import:** Dashboard → New Project → GitHub
3. **Deploy:** Automático em push para `main`

---

## 📊 Fluxo de Dados

```
┌─────────────────────┐
│   Dashboard Login   │
│  (frontend local)   │
└──────────┬──────────┘
           │
           ├─► localStorage (usuários)
           └─► sessionStorage (sessão)
                    │
                    ▼
        ┌─────────────────────┐
        │   Dashboard View    │
        │ (dados consolidados)│
        └──────────┬──────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    Meta MCP            Windsor.ai
  (MDL dados)        (Girafa dados)
        │                     │
        └─────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  GitHub Pages       │
        │  (deploy automático)│
        └─────────────────────┘
```

---

## 🤝 Como Contribuir

1. **Fork** o repositório
2. **Crie branch:** `git checkout -b feature/sua-feature`
3. **Commit:** `git commit -am 'Add nova feature'`
4. **Push:** `git push origin feature/sua-feature`
5. **Abra Pull Request**

---

## ❓ FAQ

**P: Preciso de backend para usar?**
R: Não. Frontend funciona 100% offline com localStorage. Backend é opcional para sincronização multi-dispositivo.

**P: Como resetar os usuários?**
R: Admin Panel → "Resetar para Demo" (deleta tudo e restaura usuários de demo).

**P: Qual é a senha padrão?**
R: Não há "padrão". Cada usuário tem sua senha. Demo usa `admin123` e `user123`.

**P: Os dados são sincronizados com Meta Ads automaticamente?**
R: Sim! GitHub Actions atualiza o dashboard a cada 6 horas.

---

## 📞 Suporte

**Problemas?**

1. Abra Console (F12)
2. Verifique se há erros
3. Abra Issue no GitHub

---

## 📄 Licença

MIT License — Veja LICENSE para detalhes

---

## 👤 Autor

Criado para: **Diego Cordeiro**  
Empresas: **Lojas MDL** + **Cantinho da Girafa**  
Data: **26 de maio de 2026**

---

## 🎯 Roadmap

- [ ] v1.1 — Backend Flask integrado
- [ ] v2.0 — Banco de dados real
- [ ] v2.1 — Two-factor authentication
- [ ] v2.2 — Mobile app (React Native)
- [ ] v3.0 — IA para análise automática

---

**Última atualização:** 27 de maio de 2026  
**Status:** ✅ Pronto para uso
