#!/usr/bin/env python3
"""
Script que roda no GitHub Actions a cada 6 horas.
Busca dados ao vivo da Meta Marketing API e gera um arquivo JSON
que o dashboard HTML lê e renderiza.

Uso local (teste):
    python fetch_data.py
    # Cria: data/campaigndata.json

No GitHub Actions:
    - Token é passado como secret META_ACCESS_TOKEN
    - Script roda em schedule (cron)
    - JSON é commitado automaticamente
"""

import os
import json
import sys
from datetime import datetime, timezone
import requests

# Token vem do GitHub Secret
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# As duas contas
CONTAS = {
    "Lojas MDL": "1124246161345381",
    "Cantinho da Girafa": "811077953131064",
}

def _get(path, params=None):
    """Chamada GET à Graph API."""
    params = params or {}
    params["access_token"] = ACCESS_TOKEN
    try:
        r = requests.get(f"{BASE_URL}/{path}", params=params, timeout=30)
        data = r.json()
        if "error" in data:
            return {"_erro": data["error"].get("message", "erro desconhecido")}
        return data
    except Exception as e:
        return {"_erro": str(e)}

def buscar_campanhas(account_id, empresa):
    """Busca campanhas de uma conta."""
    saida = []
    campos = "id,name,status,effective_status,objective,daily_budget,lifetime_budget"
    camp = _get(f"act_{account_id}/campaigns", {
        "fields": campos,
        "limit": 50,
    })

    if "_erro" in camp:
        return [{
            "empresa": empresa,
            "erro": camp["_erro"],
            "nome": "(conta indisponível)",
            "status": "—",
        }]

    for c in camp.get("data", []):
        hoje = _get(f"{c['id']}/insights", {
            "date_preset": "today",
            "fields": "spend,impressions,reach,frequency,cpm,clicks,ctr,cpc",
        })
        semana = _get(f"{c['id']}/insights", {
            "date_preset": "last_7d",
            "fields": "spend,impressions,reach,frequency,cpm,clicks,ctr,cpc",
        })

        h = (hoje.get("data") or [{}])[0] if "_erro" not in hoje else {}
        s = (semana.get("data") or [{}])[0] if "_erro" not in semana else {}

        orcamento = c.get("daily_budget") or c.get("lifetime_budget") or "0"
        try:
            orcamento_reais = f"R$ {int(orcamento)/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            orcamento_reais = "—"

        saida.append({
            "empresa": empresa,
            "id": c["id"],
            "nome": c.get("name", "Sem nome"),
            "status": c.get("effective_status", c.get("status", "—")),
            "objetivo": _traduzir_objetivo(c.get("objective", "")),
            "orcamento": orcamento_reais,
            "gasto_hoje": _moeda(h.get("spend")),
            "impressoes_hoje": _num(h.get("impressions")),
            "alcance_hoje": _num(h.get("reach")),
            "frequencia_hoje": _freq(h.get("frequency")),
            "cpm_hoje": _moeda(h.get("cpm")),
            "cliques_hoje": _num(h.get("clicks")),
            "gasto_7d": _moeda(s.get("spend")),
            "alcance_7d": _num(s.get("reach")),
            "frequencia_7d": _freq(s.get("frequency")),
            "alerta": _gerar_alerta(h),
        })
    return saida

def _traduzir_objetivo(obj):
    mapa = {
        "OUTCOME_AWARENESS": "Alcance/Reconhecimento",
        "OUTCOME_TRAFFIC": "Tráfego",
        "OUTCOME_ENGAGEMENT": "Engajamento",
        "OUTCOME_LEADS": "Leads",
        "OUTCOME_SALES": "Vendas",
        "OUTCOME_APP_PROMOTION": "Promoção de App",
    }
    return mapa.get(obj, obj or "—")

def _moeda(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "—"

def _num(v):
    try:
        return f"{int(float(v)):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "—"

def _freq(v):
    try:
        return f"{float(v):.2f}x"
    except (ValueError, TypeError):
        return "—"

def _gerar_alerta(insights):
    """Gera alertas baseados em métricas."""
    alertas = []
    try:
        freq = float(insights.get("frequency", 0))
        if freq >= 5:
            alertas.append(("🔴", "Frequência alta — risco de saturação"))
        elif freq >= 4:
            alertas.append(("🟡", "Frequência subindo — fique de olho"))
    except (ValueError, TypeError):
        pass
    try:
        cpm = float(insights.get("cpm", 0))
        if cpm > 0 and cpm > 5:
            alertas.append(("🟡", f"CPM acima do histórico (R$ {cpm:.2f})"))
    except (ValueError, TypeError):
        pass
    return alertas

def main():
    if not ACCESS_TOKEN:
        print("❌ META_ACCESS_TOKEN não está definido")
        print("   No GitHub: adicione como Secret nas configurações do repositório")
        print("   Localmente: crie um arquivo .env com META_ACCESS_TOKEN=seu_token")
        sys.exit(1)

    print("🔄 Buscando dados das campanhas...")

    todas = []
    for empresa, account_id in CONTAS.items():
        print(f"   → {empresa}...", end=" ", flush=True)
        campanhas = buscar_campanhas(account_id, empresa)
        todas.extend(campanhas)
        print(f"OK ({len(campanhas)} campanhas)")

    # Consolidar totais
    total_gasto_hoje = 0.0
    total_campanhas_ativas = 0
    for c in todas:
        if "erro" not in c:
            total_campanhas_ativas += 1
            try:
                v = c.get("gasto_hoje", "0").replace("R$", "").replace(".", "").replace(",", ".").strip()
                total_gasto_hoje += float(v or 0)
            except (ValueError, AttributeError):
                pass

    dados = {
        "atualizado_em": datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y %H:%M:%S"),
        "campanhas": todas,
        "resumo": {
            "total_campanhas": total_campanhas_ativas,
            "gasto_hoje": f"R$ {total_gasto_hoje:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        }
    }

    # Garantir que a pasta data/ existe
    os.makedirs("data", exist_ok=True)

    # Salvar JSON
    with open("data/campaigndata.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Dados salvos em data/campaigndata.json")
    print(f"   Campanhas: {total_campanhas_ativas}")
    print(f"   Gasto hoje: {dados['resumo']['gasto_hoje']}")
    print(f"   Última atualização: {dados['atualizado_em']}")

if __name__ == "__main__":
    main()
