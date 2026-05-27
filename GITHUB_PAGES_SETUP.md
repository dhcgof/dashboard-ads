# 🚀 GUIA DE DEPLOYMENT — GITHUB PAGES

## 📋 Pré-requisitos

- Conta GitHub (gratuita)
- Git instalado localmente
- Usuário GitHub criado

---

## ✅ PASSO 1: Criar repositório no GitHub

### Opção A: Via GitHub CLI (Automático)
```bash
cd /home/claude/dashboard-repo
gh repo create dashboard-auth --public --source=. --remote=origin --push
```

### Opção B: Via GitHub Web (Manual)
1. Acesse https://github.com/new
2. Nome: `dashboard-auth`
3. Descrição: "Dashboard com Autenticação — MDL + Cantinho da Girafa"
4. Escolha: **Public**
5. Clique em "Create repository"

---

## 📤 PASSO 2: Fazer Push do Código

Se usou Opção A, pule para Passo 3.

Se usou Opção B, execute:

```bash
cd /home/claude/dashboard-repo

# Configure seu usuário Git (primeira vez)
git config user.name "Seu Nome"
git config user.email "seu@email.com"

# Adicionar remote (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/dashboard-auth.git

# Renomear branch
git branch -M main

# Fazer push
git push -u origin main
```

---

## 🌐 PASSO 3: Ativar GitHub Pages

1. Vá para: https://github.com/SEU_USUARIO/dashboard-auth/settings
2. Na esquerda, clique em **"Pages"**
3. Em "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main** / **(root)**
4. Clique em **Save**
5. Aguarde ~1 minuto
6. Você verá: ✅ "Your site is live at https://SEU_USUARIO.github.io/dashboard-auth/"

---

## 🔑 PASSO 4: Acessar o Dashboard

### URL do Login:
```
https://SEU_USUARIO.github.io/dashboard-auth/dashboard_login.html
```

### Usuários de Demo:
- **Admin:** `admin@example.com` / `admin123`
- **User:** `user@example.com` / `user123`

---

## 📝 PASSO 5: Personalizar (Opcional)

### Mudar URL Base
Se quiser um domínio customizado, adicione ao repositório:

1. Crie arquivo `CNAME`:
```
seu-dominio.com.br
```

2. Faça push:
```bash
git add CNAME
git commit -m "Adicionar domínio customizado"
git push
```

3. Configure DNS:
   - Adicione CNAME: `seu-dominio.com.br` → `seu-usuario.github.io`

---

## 🔄 PASSO 6: Atualizar o Dashboard

Sempre que fizer mudanças:

```bash
cd /home/claude/dashboard-repo

# 1. Ver mudanças
git status

# 2. Adicionar arquivos
git add -A

# 3. Commitar
git commit -m "Descrição das mudanças"

# 4. Fazer push
git push
```

Seu site atualiza automaticamente em ~2 minutos.

---

## 🎯 Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Código feito push (main branch)
- [ ] GitHub Pages ativado
- [ ] Site está live em `https://seu-usuario.github.io/dashboard-auth/`
- [ ] Login funciona com credenciais de demo
- [ ] Dashboard carrega corretamente
- [ ] Painel Admin funciona

---

## 🆘 Troubleshooting

### "Erro: repositório já existe"
```bash
git remote remove origin
git remote add origin https://github.com/seu-usuario/dashboard-auth.git
git push -u origin main
```

### "Erro: Permission denied"
Você precisa:
1. Criar token no GitHub: https://github.com/settings/tokens
2. Usar como senha no push

### "Site não aparece após push"
1. Espere 2-5 minutos
2. Limpe cache (Ctrl+Shift+Delete no navegador)
3. Verifique Settings → Pages → se está em `Deploy from branch`

### "Login não funciona"
1. Abra console (F12)
2. Verifique se há erros
3. localStorage pode estar desabilitado
4. Tente em modo privado/incógnito

---

## 📚 Próximas Etapas

1. **Integrar Backend**: Configure Flask em Heroku/Railway
2. **Banco de Dados**: Mude de JSON para PostgreSQL
3. **Domínio Custom**: Configure seu domínio `.com.br`
4. **SSL/HTTPS**: GitHub Pages já inclui (gratuito)
5. **CI/CD**: Setup automático com GitHub Actions

---

## 📞 Links Úteis

- GitHub Pages: https://pages.github.com/
- Dashboard: `https://seu-usuario.github.io/dashboard-auth/`
- Admin Panel: `https://seu-usuario.github.io/dashboard-auth/dashboard_login.html` (aba Admin)
- Repositório: `https://github.com/seu-usuario/dashboard-auth`

---

**Criado em:** 27 de maio de 2026  
**Para:** Diego Cordeiro — MDL + Cantinho da Girafa  
**Status:** ✅ Pronto para produção
