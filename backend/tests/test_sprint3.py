import sys
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import (
    app,
    banco_tutores,
    banco_animais,
    banco_agendamentos,
    banco_vacinas_aplicadas,
    banco_internacoes,
    banco_plantoes,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_dados_teste():
    """Configura um estado limpo e controlado antes de cada teste."""
    banco_tutores.clear()
    banco_animais.clear()
    banco_agendamentos.clear()
    banco_vacinas_aplicadas.clear()
    banco_internacoes.clear()
    banco_plantoes.clear()

    # Criação de um Tutor base (ID: 1)
    banco_tutores[1] = {
        "id_tutor": 1,
        "nome": "Carlos Eduardo",
        "cpf": "12345678901",
        "cidade": "Ribeirão Preto",
        "email": "carlos@teste.com",
        "telefone": "16999998888",
    }

    # Criação de um Animal base (ID: 1)
    banco_animais[1] = {
        "id_animal": 1,
        "id_tutor": 1,
        "nome": "Bidu",
        "tipo_animal": "Cão",
        "raca": "SRD",
        "sexo": "M",
        "idade": 4,
    }


def test_ct19_entrada_internacao_sucesso():
    res = client.post("/internacoes", json={
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Alta",
        "motivo": "Pós-operatório ortopédico",
        "observacoes": "Monitorar sinais vitais a cada 2h"
    })
    assert res.status_code == 201
    dados = res.json()["internacao"]
    assert dados["animal_nome"] == "Bidu"
    assert dados["tutor_nome"] == "Carlos Eduardo"
    assert dados["status_internacao"] == "Internado"


def test_ct20_validacao_gravidade_invalida():
    res = client.post("/internacoes", json={
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Extrema",
        "motivo": "Trauma"
    })
    assert res.status_code == 400


def test_ct21_bloqueio_internacao_duplicada():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Medio",
        "motivo": "Observação clínica"
    }
    res1 = client.post("/internacoes", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/internacoes", json=payload)
    assert res2.status_code == 409


def test_ct22_listagem_e_filtros_internacao():
    client.post("/internacoes", json={
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Critica",
        "motivo": "Intoxicação aguda"
    })

    res = client.get("/internacoes?nivel_gravidade=Critica&status_internacao=Internado")
    assert res.status_code == 200
    lista = res.json()
    assert len(lista) == 1
    assert lista[0]["nivel_gravidade"] == "Critica"


def test_ct23_detalhamento_caso_clinico():
    res_criacao = client.post("/internacoes", json={
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Alta",
        "motivo": "Desidratação severa"
    })
    id_internacao = res_criacao.json()["internacao"]["id_internacao"]

    res = client.get(f"/internacoes/{id_internacao}")
    assert res.status_code == 200
    dados = res.json()
    assert "internacao" in dados
    assert dados["detalhes_animal"]["nome"] == "Bidu"
    assert "historico_evolucoes_plantao" in dados


def test_ct24_evolucao_plantao_sucesso():
    res = client.post(
        "/plantao",
        headers={"x-perfil": "veterinario"},
        json={
            "id_animal": 1,
            "crmv": 12345,
            "evolucao_plantao": "Paciente estável, aceitando alimentação pastosa."
        }
    )
    assert res.status_code == 201
    plantao = res.json()["plantao"]
    assert "_DIURNO" in plantao["turno_plantao"] or "_NOTURNO" in plantao["turno_plantao"]


def test_ct25_bloqueio_evolucao_plantao_duplicada():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "evolucao_plantao": "Primeira evolução do turno."
    }
    res1 = client.post("/plantao", headers={"x-perfil": "veterinario"}, json=payload)
    assert res1.status_code == 201

    res2 = client.post("/plantao", headers={"x-perfil": "veterinario"}, json=payload)
    assert res2.status_code == 409


def test_ct26_resumo_tempo_real_dashboard():
    client.post("/internacoes", json={
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Critica",
        "motivo": "Emergência"
    })

    res = client.get("/dashboard")
    assert res.status_code == 200
    dados = res.json()
    assert dados["total_tutores"] == 1
    assert dados["total_animais"] == 1
    assert dados["total_internacoes_ativas"] == 1
    assert dados["resumo_gravidade_internacoes"]["Critica"] == 1
