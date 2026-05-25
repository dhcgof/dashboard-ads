# 📊 Dashboard de Campanhas — GitHub Pages

Painel online hospedado no GitHub Pages que monitora campanhas Meta Ads das duas empresas (Lojas MDL + Cantinho da Girafa). **Completamente automático**: GitHub Actions roda a cada 6 horas, busca os dados ao vivo e atualiza o painel.

## Como funciona

1. **GitHub Actions** roda um script Python a cada 6 horas
2. O script busca dados da Meta Marketing API
3. Gera um arquivo JSON com os dados (`data/campaigndata.json`)
4. Faz commit automático no repositório
5. **GitHub Pages** hospeda o `index.html` que lê esse JSON
6. Dashboard fica acessível em: `https://seu-usuario.github.io/dashboard-ads`

## Setup (25 minutos)

### 1. Criar repositório GitHub
```bash
# Clone este projeto ou crie um novo repo
git clone <seu-repo> dashboard-ads
cd dashboard-ads
```

### 2. Adicionar o token como Secret
No GitHub, vá em:
- **Settings** → **Secrets and variables** → **Actions**
- Clique em **New repository secret**
- Nome: `META_ACCESS_TOKEN`
- Valor: Cole seu System User Token do Meta
- Salve

### 3. Ativar GitHub Pages
- **Settings** → **Pages**
- Source: **Deploy from a branch**
- Branch: **main** (ou master)
- Pasta: **/(root)**
- Salve

### 4. Testar
- Vá em **Actions** → **Atualizar Dashboard** → **Run workflow**
- Aguarde terminar (~30 seg)
- Confira se o arquivo `data/campaigndata.json` foi criado
- Abra `https://seu-usuario.github.io/seu-repo-name/`

## Acessar o dashboard

```
https://seu-usuario.github.io/dashboard-ads/
```

Substituir `seu-usuario` pelo seu username GitHub.

## Personalizar

**Mudar frequência de atualização** (padrão: 6 em 6 horas):
- Edite `.github/workflows/update-dashboard.yml`
- Linha `- cron: '0 0,6,12,18 * * *'`
- Exemplos:
  - `'0 * * * *'` = a cada hora
  - `'0 0 * * *'` = uma vez por dia (meia-noite UTC)
  - [Gerador cron](https://crontab.guru/)

**Adicionar/remover contas**:
- Edite `fetch_data.py`, dicionário `CONTAS`

## O que mostra

Por campanha:
- Status (no ar / pausada)
- Gasto do dia + últimos 7 dias
- Alcance, impressões, frequência, CPM, cliques
- Alertas automáticos (frequência alta, CPM acima do histórico)

Resumo consolidado das duas empresas no topo.

## Troubleshooting

**Painel vazio / "Carregando...":**
- O arquivo `data/campaigndata.json` ainda não foi criado
- Execute manualmente o workflow em **Actions**
- Aguarde ~30 segundos

**Erro "HTTP 401" no Actions:**
- Token inválido ou expirado
- Gere um novo System User Token no Meta Business Manager
- Atualize o secret `META_ACCESS_TOKEN` no GitHub

**Dados antigos:**
- GitHub Pages pode levar até 5 minutos para atualizar
- Force refresh no navegador: `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)

## Notas

- Totalmente gratuito (GitHub Pages + GitHub Actions)
- Dados públicos? Não — o repositório é privado, painel privado
- Se quiser painel público, a URL fica acessível a qualquer um com o link
