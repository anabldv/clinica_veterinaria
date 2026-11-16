from datetime import datetime
from fastapi.testclient import TestClient
from app.main import (
    app,
    banco_usuarios,
    banco_tutores,
    banco_animais,
    banco_agendamentos,
    obter_identificador_plantao_atual,
)

client = TestClient(app)


def limpar_bancos():
    banco_usuarios.clear()
    banco_tutores.clear()
    banco_animais.clear()
    banco_agendamentos.clear()


def test_ct27_consistencia_imediata_dados():
    """História 10: Cadastro de tutor, animal vinculado e agendamento imediato sem atraso."""
    limpar_bancos()

    # 1. Cadastra Tutor
    res_tutor = client.post("/tutores", json={
        "nome": "Mariana Costa",
        "cpf": "12345678901",
        "telefone": "16988887777",
        "email": "mariana@email.com",
        "cidade": "Ribeirão Preto"
    })
    assert res_tutor.status_code == 201
    id_tutor = res_tutor.json()["tutor"]["id_tutor"]

    # 2. Cadastra Animal imediatamente usando o ID recém-gerado
    res_animal = client.post("/animais", json={
        "id_tutor": id_tutor,
        "nome": "Thor",
        "tipo_animal": "Cão",
        "raca": "Golden",
        "sexo": "M",
        "idade": 2
    })
    assert res_animal.status_code == 201
    id_animal = res_animal.json()["animal"]["id_animal"]

    # 3. Agenda consulta imediatamente com os IDs criados
    res_agenda = client.post("/agendamentos", json={
        "id_animal": id_animal,
        "id_tutor": id_tutor,
        "veterinario": "Dr. Carlos",
        "data_hora": "20/12/2026 14:00",
        "tipo_servico": "Consulta Clínica"
    })
    assert res_agenda.status_code == 201


def test_ct28_integridade_referencial_tutor_inexistente():
    """História 10: Bloqueio ao cadastrar animal para tutor inexistente (espelho FK Oracle)."""
    limpar_bancos()

    res = client.post("/animais", json={
        "id_tutor": 999,
        "nome": "Rex",
        "tipo_animal": "Cão"
    })
    assert res.status_code == 404


def test_ct29_disponibilidade_24_7_health():
    """História 11: Verificação do endpoint de disponibilidade contínua /health."""
    res = client.get("/health")
    assert res.status_code == 200
    dados = res.json()
    assert dados["status"] == "OPERACIONAL"
    assert dados["disponibilidade"] == "24/7"
    assert "turno_ativo" in dados


def test_ct30_operacao_plantao_noturno_madrugada():
    """História 11: Cálculo de turno durante madrugada (02:30) e horário diurno (14:00)."""
    dt_madrugada = datetime(2026, 11, 15, 2, 30)
    assert obter_identificador_plantao_atual(dt_madrugada) == "2026-11-14_NOTURNO"

    dt_diurno = datetime(2026, 11, 15, 14, 0)
    assert obter_identificador_plantao_atual(dt_diurno) == "2026-11-15_DIURNO"


def test_ct31_autenticacao_e_consulta_usuarios():
    """Validação de cadastro, listagem sem expor senha e login válido/inválido."""
    limpar_bancos()

    res_cad = client.post("/usuarios", json={
        "nome": "Alexandre Carvalho",
        "email": "alexandre@clinica.com",
        "senha": "senhaSegura123",
        "perfil": "Recepcao"
    })
    assert res_cad.status_code == 201
    assert "senha" not in res_cad.json()["usuario"]

    res_get = client.get("/usuarios")
    assert res_get.status_code == 200
    assert len(res_get.json()) == 1
    assert "senha" not in res_get.json()[0]

    res_login_ok = client.post("/login", json={
        "email": "alexandre@clinica.com",
        "senha": "senhaSegura123"
    })
    assert res_login_ok.status_code == 200

    res_login_erro = client.post("/login", json={
        "email": "alexandre@clinica.com",
        "senha": "senhaErrada"
    })
    assert res_login_erro.status_code == 401
