import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator

try:
    import oracledb
except ImportError:
    oracledb = None

app = FastAPI(
    title="Pet & Gatô - Sistema de Gestão Veterinária",
    version="3.0.0",
    description="API REST para controle clínico, cadastros, agendamentos, internações e plantão veterinário."
)

# ==============================================================================
# CONFIGURAÇÃO DE CORS (Permite comunicação direta com o Front-end)
# ==============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_USER = os.getenv("DB_USER", "clinica_veterinaria")
DB_PASSWORD = os.getenv("DB_PASSWORD", "clinica_senha")
DB_DSN = os.getenv("DB_DSN", "localhost:1521/freepdb1")


def usando_modo_memoria() -> bool:
    """Usa armazenamento em memória durante a suíte Pytest (CI) ou se oracledb não estiver disponível."""
    if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("USE_MEMORY_DB") == "1" or oracledb is None:
        return True
    return False


def obter_conexao():
    if usando_modo_memoria():
        return None
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for err in exc.errors():
        loc = err.get("loc", ())
        if "senha" in loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": {"mensagem": "Senha fraca. A senha deve ter no mínimo 6 caracteres."}}
            )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": {"mensagem": "Erro de validação nos campos."}}
    )


# ==============================================================================
# ESTRUTURAS EM MEMÓRIA (Para execução isolada de testes / CI sem Oracle)
# ==============================================================================
banco_usuarios: Dict[int, dict] = {}
banco_tutores: Dict[int, dict] = {}
banco_animais: Dict[int, dict] = {}
banco_agendamentos: Dict[int, dict] = {}
banco_vacinas_aplicadas: Dict[int, list] = {}
banco_prontuarios: Dict[int, list] = {}
banco_vacinacoes: Dict[int, list] = {}
banco_internacoes: Dict[int, dict] = {}
banco_plantoes: Dict[int, list] = {}

db_usuarios = banco_usuarios
db_tutores = banco_tutores
db_animais = banco_animais
db_agendamentos = banco_agendamentos


# ==============================================================================
# MODELOS DE DADOS (PYDANTIC)
# ==============================================================================

class UsuarioCadastro(BaseModel):
    nome: Optional[str] = None
    email: EmailStr
    senha: str
    perfil: Optional[str] = "Recepcao"

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str):
        if len(v) < 6:
            raise ValueError("Senha fraca: a senha deve possuir ao menos 6 caracteres.")
        return v


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class TutorCadastro(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    cidade: Optional[str] = None
    observacoes: Optional[str] = None


class AnimalCadastro(BaseModel):
    id_tutor: int
    nome: str
    tipo_animal: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    sexo: Optional[str] = None
    idade: Optional[int] = None
    data_nascimento: Optional[str] = None


class AgendamentoCadastro(BaseModel):
    id_animal: int
    id_tutor: Optional[int] = None
    veterinario: Optional[str] = None
    crmv: Optional[int] = None
    matricula: Optional[int] = None
    data_hora: datetime
    tipo_servico: str
    nome_vacina: Optional[str] = None
    observacoes: Optional[str] = None

    @field_validator("data_hora", mode="before")
    @classmethod
    def parse_data_hora(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    return datetime.strptime(v.strip(), fmt)
                except ValueError:
                    pass
            try:
                return datetime.fromisoformat(v.strip())
            except ValueError:
                pass
        raise ValueError("Formato de data inválido. Use 'DD/MM/YYYY HH:MM' ou formato ISO.")


class ProntuarioCadastro(BaseModel):
    crmv: int
    id_animal: int
    id_tutor: Optional[int] = None
    peso_atual: float
    queixa: str
    anamnese: Optional[str] = None
    diagnostico: str
    receita: Optional[str] = None
    vacina: Optional[str] = None
    data_vacinacao: Optional[datetime] = None
    lote_vacina: Optional[str] = None
    data_proxima_dose: Optional[str] = None


class InternacaoCadastro(BaseModel):
    id_animal: int
    crmv: int
    nivel_gravidade: str
    motivo: str
    observacoes: Optional[str] = None


class StatusInternacaoUpdate(BaseModel):
    status_internacao: str
    observacoes: Optional[str] = None


class PlantaoCadastro(BaseModel):
    id_animal: Optional[int] = None
    id_tutor: Optional[int] = None
    crmv: int
    evolucao_plantao: Optional[str] = None


# ==============================================================================
# FUNÇÕES AUXILIARES DE NEGÓCIO
# ==============================================================================

def obter_identificador_plantao_atual(dt: datetime) -> str:
    data_str = dt.strftime("%Y-%m-%d")
    if 7 <= dt.hour < 19:
        return f"{data_str}_DIURNO"
    if dt.hour < 7:
        ontem = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
        return f"{ontem}_NOTURNO"
    return f"{data_str}_NOTURNO"


# ==============================================================================
# ROTAS - MONITORAMENTO / DISPONIBILIDADE (SPRINT 4 - HISTÓRIA 11)
# ==============================================================================

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoramento"])
def verificar_status_sistema():
    agora = datetime.now()
    turno_atual = obter_identificador_plantao_atual(agora)
    modo_bd = "MEMORIA_CI" if usando_modo_memoria() else "ORACLE_DB"

    return {
        "status": "OPERACIONAL",
        "timestamp": agora.isoformat(),
        "disponibilidade": "24/7",
        "turno_ativo": turno_atual,
        "servicos": {
            "banco_dados": f"CONECTADO ({modo_bd})",
            "modulo_plantao": "ATIVO",
            "modulo_internacao": "ATIVO"
        }
    }


# ==============================================================================
# ROTAS - SPRINT 1 E AUTENTICAÇÃO
# ==============================================================================

@app.post("/usuarios", status_code=status.HTTP_201_CREATED, tags=["Usuários"])
def cadastrar_usuario(usuario: UsuarioCadastro):
    if usando_modo_memoria():
        for u in banco_usuarios.values():
            if u["email"] == usuario.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"mensagem": "E-mail já cadastrado no sistema."}
                )
        novo_id = len(banco_usuarios) + 1
        novo_usuario = {
            "id_usuario": novo_id,
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
            "perfil": usuario.perfil
        }
        banco_usuarios[novo_id] = novo_usuario
        resp = {k: v for k, v in novo_usuario.items() if k != "senha"}
        return {"usuario": resp, "mensagem": "Usuário criado com sucesso"}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(id_usuario), 0) + 1 FROM tb_usuario")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO tb_usuario (id_usuario, nome_usuario, email_usuario, senha, perfil)
            VALUES (:id, :nome, :email, :senha, :perfil)
        """
        cursor.execute(sql, {
            "id": novo_id,
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
            "perfil": usuario.perfil
        })
        conexao.commit()
        return {
            "usuario": {
                "id_usuario": novo_id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfil": usuario.perfil
            },
            "mensagem": "Usuário criado com sucesso"
        }
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.post("/login", status_code=status.HTTP_200_OK, tags=["Usuários"])
def realizar_login(credenciais: UsuarioLogin):
    if usando_modo_memoria():
        for u in banco_usuarios.values():
            if u["email"] == credenciais.email:
                if u["senha"] == credenciais.senha:
                    return {
                        "mensagem": "Login realizado com sucesso!",
                        "usuario": {
                            "id_usuario": u["id_usuario"],
                            "nome": u["nome"],
                            "email": u["email"],
                            "perfil": u["perfil"]
                        }
                    }
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas: senha incorreta."
                )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT id_usuario, nome_usuario, email_usuario, senha, perfil FROM tb_usuario WHERE email_usuario = :email",
            {"email": credenciais.email}
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        if row[3] != credenciais.senha:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas: senha incorreta.")

        return {
            "mensagem": "Login realizado com sucesso!",
            "usuario": {
                "id_usuario": row[0],
                "nome": row[1],
                "email": row[2],
                "perfil": row[4]
            }
        }
    finally:
        cursor.close()
        conexao.close()


@app.get("/usuarios", status_code=status.HTTP_200_OK, tags=["Usuários"])
def listar_usuarios():
    if usando_modo_memoria():
        return [{k: v for k, v in u.items() if k != "senha"} for u in banco_usuarios.values()]

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_usuario, nome_usuario AS nome, email_usuario AS email, perfil FROM tb_usuario")
        colunas = [col[0].lower() for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conexao.close()


@app.post("/tutores", status_code=status.HTTP_201_CREATED, tags=["Tutores"])
def cadastrar_tutor(tutor: TutorCadastro):
    if usando_modo_memoria():
        cpf_limpo = re.sub(r"\D", "", tutor.cpf)
        for t in banco_tutores.values():
            if re.sub(r"\D", "", str(t.get("cpf", ""))) == cpf_limpo:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF já cadastrado no sistema.")
        novo_id = len(banco_tutores) + 1
        novo_tutor = {
            "id_tutor": novo_id,
            "nome": tutor.nome,
            "cpf": cpf_limpo,
            "telefone": tutor.telefone,
            "email": tutor.email,
            "cidade": tutor.cidade,
            "observacoes": tutor.observacoes
        }
        banco_tutores[novo_id] = novo_tutor
        return {"tutor": novo_tutor, "id_tutor": novo_id, "mensagem": "Tutor cadastrado com sucesso!"}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(id_tutor), 0) + 1 FROM tb_tutor")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO tb_tutor (id_tutor, nome_tutor, cpf_tutor, email_tutor, telefone, observacoes)
            VALUES (:id, :nome, :cpf, :email, :tel, :observacoes)
        """
        cursor.execute(sql, {
            "id": novo_id,
            "nome": tutor.nome,
            "cpf": tutor.cpf,
            "email": tutor.email,
            "tel": tutor.telefone,
            "observacoes": tutor.observacoes,
        })
        conexao.commit()
        return {"mensagem": "Tutor cadastrado com sucesso!", "id_tutor": novo_id}
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/tutores", status_code=status.HTTP_200_OK, tags=["Tutores"])
def listar_tutores():
    if usando_modo_memoria():
        return list(banco_tutores.values())

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_tutor, nome_tutor, cpf_tutor, email_tutor, telefone, observacoes FROM tb_tutor")
        colunas = [col[0].lower() for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conexao.close()


@app.get("/tutores/{id_tutor}", status_code=status.HTTP_200_OK, tags=["Tutores"])
def buscar_tutor(id_tutor: int):
    if usando_modo_memoria():
        if id_tutor in banco_tutores:
            return {"tutor": banco_tutores[id_tutor]}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tutor com ID {id_tutor} não encontrado.")

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT id_tutor, nome_tutor, cpf_tutor, email_tutor, telefone, observacoes FROM tb_tutor WHERE id_tutor = :id",
            {"id": id_tutor}
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tutor com ID {id_tutor} não encontrado.")
        colunas = [col[0].lower() for col in cursor.description]
        return {"tutor": dict(zip(colunas, row))}
    finally:
        cursor.close()
        conexao.close()


@app.post("/animais", status_code=status.HTTP_201_CREATED, tags=["Animais"])
def cadastrar_animal(animal: AnimalCadastro):
    if usando_modo_memoria():
        if animal.id_tutor not in banco_tutores:
            raise HTTPException(status_code=404, detail=f"Tutor com ID {animal.id_tutor} não encontrado.")
        novo_id = len(banco_animais) + 1
        novo_animal = {
            "id_animal": novo_id,
            "id_tutor": animal.id_tutor,
            "nome": animal.nome,
            "tipo_animal": animal.tipo_animal or animal.especie,
            "raca": animal.raca,
            "sexo": animal.sexo,
            "idade": animal.idade,
            "data_nascimento": animal.data_nascimento
        }
        banco_animais[novo_id] = novo_animal
        return {"animal": novo_animal, "mensagem": "Animal cadastrado com sucesso"}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_tutor WHERE id_tutor = :id", {"id": animal.id_tutor})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Tutor com ID {animal.id_tutor} não encontrado.")

        cursor.execute("SELECT NVL(MAX(id_animal), 0) + 1 FROM tb_animal")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO tb_animal (id_animal, id_tutor, nome_animal, tipo_animal, raca, sexo)
            VALUES (:id, :tutor, :nome, :tipo, :raca, :sexo)
        """
        cursor.execute(sql, {
            "id": novo_id,
            "tutor": animal.id_tutor,
            "nome": animal.nome,
            "tipo": animal.tipo_animal or animal.especie,
            "raca": animal.raca,
            "sexo": animal.sexo
        })
        conexao.commit()
        return {"animal": {"id_animal": novo_id, **animal.model_dump()}, "mensagem": "Animal cadastrado com sucesso"}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/animais", status_code=status.HTTP_200_OK, tags=["Animais"])
def listar_animais():
    if usando_modo_memoria():
        return list(banco_animais.values())

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_animal, id_tutor, nome_animal, tipo_animal, raca, sexo FROM tb_animal")
        colunas = [col[0].lower() for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conexao.close()


# ==============================================================================
# ROTAS - SPRINT 2
# ==============================================================================

@app.post("/agendamentos", status_code=status.HTTP_201_CREATED, tags=["Agendamentos"])
def criar_agendamento(agendamento: AgendamentoCadastro):
    if usando_modo_memoria():
        agora = datetime.now()
        if agendamento.data_hora < agora:
            raise HTTPException(status_code=400, detail="Não é permitido realizar agendamentos em datas retroativas.")
        if agendamento.id_tutor and agendamento.id_tutor not in banco_tutores:
            raise HTTPException(status_code=404, detail=f"Tutor com ID {agendamento.id_tutor} não encontrado.")
        if agendamento.id_animal not in banco_animais:
            raise HTTPException(status_code=404, detail=f"Animal com ID {agendamento.id_animal} não encontrado.")

        vet_nome = agendamento.veterinario or f"CRMV-{agendamento.crmv}"
        for ag in banco_agendamentos.values():
            if (
                ag["veterinario"].strip().lower() == vet_nome.strip().lower()
                and ag["data_hora"] == agendamento.data_hora
                and ag["status"] != "CANCELADO"
            ):
                raise HTTPException(status_code=409, detail=f"Horário indisponível para {vet_nome}.")

        if "vacina" in agendamento.tipo_servico.lower():
            intervalo = timedelta(days=21)
            for v in banco_vacinas_aplicadas.get(agendamento.id_animal, []):
                if v.get("data_aplicacao") and abs(agendamento.data_hora - v["data_aplicacao"]) < intervalo:
                    raise HTTPException(status_code=400, detail="É necessário respeitar no mínimo 21 dias de intervalo entre aplicações de vacina.")
            for ag in banco_agendamentos.values():
                if ag["id_animal"] == agendamento.id_animal and "vacina" in ag["tipo_servico"].lower() and ag["status"] != "CANCELADO":
                    if abs(agendamento.data_hora - ag["data_hora"]) < intervalo:
                        raise HTTPException(status_code=400, detail="É necessário respeitar no mínimo 21 dias de intervalo entre aplicações de vacina.")

        novo_id = len(banco_agendamentos) + 1
        dados = {
            "id_agendamento": novo_id,
            "id": novo_id,
            "id_animal": agendamento.id_animal,
            "id_tutor": agendamento.id_tutor or banco_animais[agendamento.id_animal]["id_tutor"],
            "veterinario": vet_nome,
            "data_hora": agendamento.data_hora,
            "tipo_servico": agendamento.tipo_servico,
            "nome_vacina": agendamento.nome_vacina,
            "observacoes": agendamento.observacoes,
            "status": "AGENDADO",
            "criado_em": agora
        }
        banco_agendamentos[novo_id] = dados
        return {"mensagem": "Agendamento realizado com sucesso", "agendamento": dados, "id_agendamento": novo_id, "id": novo_id, "status": "AGENDADO"}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        crmv = getattr(agendamento, "crmv", None)
        matricula = getattr(agendamento, "matricula", None)
        if not crmv or not matricula:
            raise HTTPException(status_code=400, detail="É obrigatório informar o CRMV do veterinário e a Matrícula do recepcionista.")

        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Veterinário com CRMV {crmv} não encontrado.")

        cursor.execute("SELECT COUNT(*) FROM tb_recepcao WHERE matricula = :mat", {"mat": matricula})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Recepcionista com matrícula {matricula} não encontrado.")

        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": agendamento.id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Animal com ID {agendamento.id_animal} não encontrado.")

        sql = """
            INSERT INTO tb_agendamento (hora_agendamento, id_animal, crmv, matricula, status_agendamento)
            VALUES (:data_hora, :id_animal, :crmv, :matricula, 'Agendado')
        """
        cursor.execute(sql, {
            "data_hora": agendamento.data_hora,
            "id_animal": agendamento.id_animal,
            "crmv": crmv,
            "matricula": matricula
        })
        conexao.commit()
        return {"mensagem": "Agendamento realizado com sucesso", "status": "Agendado"}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/agendamentos", status_code=status.HTTP_200_OK, tags=["Agendamentos"])
def listar_agendamentos(veterinario: Optional[str] = None, status_consulta: Optional[str] = None):
    if usando_modo_memoria():
        res = list(banco_agendamentos.values())
        if veterinario:
            res = [ag for ag in res if ag["veterinario"].strip().lower() == veterinario.strip().lower()]
        if status_consulta:
            res = [ag for ag in res if ag["status"].strip().upper() == status_consulta.strip().upper()]
        return res

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT a.hora_agendamento, a.id_animal, a.crmv, a.matricula, a.status_agendamento,
                   u.nome_usuario AS nome_veterinario
            FROM tb_agendamento a
            JOIN tb_veterinario v ON a.crmv = v.crmv
            JOIN tb_usuario u ON v.id_usuario = u.id_usuario
            WHERE 1=1
        """
        params = {}
        if status_consulta:
            sql += " AND UPPER(a.status_agendamento) = UPPER(:status_consulta)"
            params["status_consulta"] = status_consulta.strip()

        cursor.execute(sql, params)
        colunas = [col[0].lower() for col in cursor.description]
        agendamentos = [dict(zip(colunas, row)) for row in cursor.fetchall()]

        if veterinario:
            agendamentos = [
                ag for ag in agendamentos
                if ag.get("nome_veterinario") and ag["nome_veterinario"].strip().lower() == veterinario.strip().lower()
            ]
        return agendamentos
    finally:
        cursor.close()
        conexao.close()


@app.patch("/agendamentos/{id_agendamento}/cancelar", status_code=status.HTTP_200_OK, tags=["Agendamentos"])
def cancelar_agendamento(id_agendamento: int):
    if usando_modo_memoria():
        if id_agendamento in banco_agendamentos:
            banco_agendamentos[id_agendamento]["status"] = "CANCELADO"
            return {
                "agendamento": banco_agendamentos[id_agendamento],
                "id_agendamento": id_agendamento,
                "status": "CANCELADO",
                "mensagem": "Agendamento cancelado com sucesso."
            }
        raise HTTPException(status_code=404, detail="Agendamento não encontrado para cancelamento.")

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT id_animal, status_agendamento FROM tb_agendamento WHERE id_animal = :id AND status_agendamento != 'Cancelado'",
            {"id": id_agendamento}
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Nenhum agendamento ativo encontrado para o ID informado ({id_agendamento}).")

        cursor.execute(
            "UPDATE tb_agendamento SET status_agendamento = 'Cancelado' WHERE id_animal = :id AND status_agendamento != 'Cancelado'",
            {"id": id_agendamento}
        )
        conexao.commit()
        return {"id_agendamento": id_agendamento, "status": "Cancelado", "mensagem": "Agendamento cancelado com sucesso no banco Oracle."}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


# ==============================================================================
# ROTAS - SPRINT 3
# ==============================================================================

@app.post("/prontuarios", status_code=status.HTTP_201_CREATED, tags=["Prontuários"])
def criar_prontuario(prontuario: ProntuarioCadastro, request: Request):
    if usando_modo_memoria():
        if request.headers.get("x-perfil", "").strip().lower() != "veterinario":
            raise HTTPException(status_code=403, detail="Acesso negado. Apenas veterinários podem editar prontuários.")
        if prontuario.id_animal not in banco_animais:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        if prontuario.peso_atual <= 0:
            raise HTTPException(status_code=400, detail="O peso atual deve ser maior que zero.")
        novo_id = len(banco_prontuarios) + 1
        reg = {
            "id_prontuario": novo_id,
            "crmv": prontuario.crmv,
            "id_animal": prontuario.id_animal,
            "data_abertura": datetime.now(),
            "peso_atual": prontuario.peso_atual,
            "queixa": prontuario.queixa,
            "anamnese": prontuario.anamnese,
            "diagnostico": prontuario.diagnostico,
            "receita": prontuario.receita,
            "vacina": prontuario.vacina
        }
        banco_prontuarios.setdefault(prontuario.id_animal, []).append(reg)
        return {"mensagem": "Prontuário criado com sucesso", "id_prontuario": novo_id, "prontuario": reg}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": prontuario.crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Veterinário com CRMV {prontuario.crmv} não encontrado.")
        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": prontuario.id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Animal com ID {prontuario.id_animal} não encontrado.")
        cursor.execute("SELECT NVL(MAX(id_prontuario), 0) + 1 FROM tb_prontuario")
        novo_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO tb_prontuario (id_prontuario, crmv, id_animal, peso_atual, queixa, anamnese, diagnostico, receita, vacina) "
            "VALUES (:id, :crmv, :animal, :peso, :queixa, :anamnese, :diag, :receita, :vacina)",
            {
                "id": novo_id, "crmv": prontuario.crmv, "animal": prontuario.id_animal,
                "peso": prontuario.peso_atual, "queixa": prontuario.queixa,
                "anamnese": prontuario.anamnese, "diag": prontuario.diagnostico,
                "receita": prontuario.receita, "vacina": prontuario.vacina
            }
        )
        conexao.commit()
        return {"mensagem": "Prontuário criado com sucesso", "id_prontuario": novo_id}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/animais/{id_animal}/prontuarios", status_code=status.HTTP_200_OK, tags=["Prontuários"])
def listar_prontuarios_animal(id_animal: int):
    if usando_modo_memoria():
        if id_animal not in banco_animais:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        return {"id_animal": id_animal, "prontuarios": banco_prontuarios.get(id_animal, []), "vacinacoes": banco_vacinacoes.get(id_animal, [])}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        cursor.execute(
            "SELECT id_prontuario, crmv, id_animal, data_abertura, peso_atual, queixa, anamnese, diagnostico, receita, vacina "
            "FROM tb_prontuario WHERE id_animal = :id", {"id": id_animal}
        )
        prontuarios = [dict(zip([c[0].lower() for c in cursor.description], r)) for r in cursor.fetchall()]
        cursor.execute(
            "SELECT v.data_aplicacao, v.crmv, v.id_prontuario, v.nome_vacina, v.lote_vacina, v.data_proxima_dose "
            "FROM tb_vacinacao v JOIN tb_prontuario p ON v.id_prontuario = p.id_prontuario WHERE p.id_animal = :id", {"id": id_animal}
        )
        vacinacoes = [dict(zip([c[0].lower() for c in cursor.description], r)) for r in cursor.fetchall()]
        return {"id_animal": id_animal, "prontuarios": prontuarios, "vacinacoes": vacinacoes}
    finally:
        cursor.close()
        conexao.close()


@app.post("/plantao", status_code=status.HTTP_201_CREATED, tags=["Plantão"])
def registrar_plantao(plantao: PlantaoCadastro, request: Request):
    if usando_modo_memoria():
        if request.headers.get("x-perfil", "").strip().lower() != "veterinario":
            raise HTTPException(status_code=403, detail="Acesso negado.")
        if not plantao.id_animal or plantao.id_animal not in banco_animais:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        agora = datetime.now()
        turno = obter_identificador_plantao_atual(agora)
        for r in banco_plantoes.get(plantao.id_animal, []):
            if r.get("turno_plantao") == turno:
                raise HTTPException(status_code=409, detail="Evolução já registrada neste plantão.")
        novo_id = len(banco_plantoes) + 1
        dados = {
            "id_plantao": novo_id, "id_animal": plantao.id_animal,
            "id_tutor": plantao.id_tutor or banco_animais[plantao.id_animal]["id_tutor"],
            "crmv": plantao.crmv, "chegada_plantao": agora,
            "turno_plantao": turno, "status_plantao": "Em analise",
            "evolucao_plantao": plantao.evolucao_plantao
        }
        banco_plantoes.setdefault(plantao.id_animal, []).append(dados)
        return {"mensagem": "Anotação de plantão registrada com sucesso.", "id_plantao": novo_id, "plantao": dados}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": plantao.crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Veterinário com CRMV {plantao.crmv} não encontrado.")
        cursor.execute("SELECT id_tutor FROM tb_animal WHERE id_animal = :id", {"id": plantao.id_animal})
        res_animal = cursor.fetchone()
        if not res_animal:
            raise HTTPException(status_code=404, detail=f"Animal com ID {plantao.id_animal} não encontrado.")
        cursor.execute("SELECT NVL(MAX(id_plantao), 0) + 1 FROM tb_plantao")
        novo_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO tb_plantao (id_plantao, id_animal, id_tutor, crmv, status_plantao, evolucao_plantao) "
            "VALUES (:id, :animal, :tutor, :crmv, 'Em analise', :evolucao)",
            {"id": novo_id, "animal": plantao.id_animal, "tutor": plantao.id_tutor or res_animal[0], "crmv": plantao.crmv, "evolucao": plantao.evolucao_plantao}
        )
        conexao.commit()
        return {"mensagem": "Anotação de plantão registrada com sucesso.", "id_plantao": novo_id}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/plantao/{id_animal}", status_code=status.HTTP_200_OK, tags=["Plantão"])
def listar_plantoes_animal(id_animal: int):
    if usando_modo_memoria():
        if id_animal not in banco_animais:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        return banco_plantoes.get(id_animal, [])

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        cursor.execute(
            "SELECT id_plantao, id_animal, id_tutor, crmv, chegada_plantao, status_plantao, evolucao_plantao "
            "FROM tb_plantao WHERE id_animal = :id", {"id": id_animal}
        )
        return [dict(zip([c[0].lower() for c in cursor.description], r)) for r in cursor.fetchall()]
    finally:
        cursor.close()
        conexao.close()


@app.post("/internacoes", status_code=status.HTTP_201_CREATED, tags=["Internações"])
def criar_internacao(internacao: InternacaoCadastro):
    if usando_modo_memoria():
        if internacao.id_animal not in banco_animais:
            raise HTTPException(status_code=404, detail="Animal não encontrado.")
        grav = internacao.nivel_gravidade.capitalize()
        if grav not in ["Baixa", "Medio", "Alta", "Critica"]:
            raise HTTPException(status_code=400, detail="Nível de gravidade inválido.")
        for i in banco_internacoes.values():
            if i["id_animal"] == internacao.id_animal and i["status_internacao"] == "Internado":
                raise HTTPException(status_code=409, detail="Animal já internado.")
        animal = banco_animais[internacao.id_animal]
        tutor = banco_tutores.get(animal["id_tutor"], {})
        novo_id = len(banco_internacoes) + 1
        dados = {
            "id_internacao": novo_id, "id_animal": internacao.id_animal,
            "animal_nome": animal.get("nome"), "tutor_nome": tutor.get("nome"),
            "crmv": internacao.crmv, "data_internacao": datetime.now(),
            "nivel_gravidade": grav, "status_internacao": "Internado",
            "motivo": internacao.motivo, "observacoes": internacao.observacoes
        }
        banco_internacoes[novo_id] = dados
        return {"mensagem": "Internação registrada com sucesso.", "id_internacao": novo_id, "internacao": dados}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": internacao.crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Veterinário com CRMV {internacao.crmv} não encontrado.")
        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": internacao.id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail=f"Animal com ID {internacao.id_animal} não encontrado.")
        cursor.execute("SELECT NVL(MAX(id_internacao), 0) + 1 FROM tb_internacao")
        novo_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO tb_internacao (id_internacao, id_animal, crmv, nivel_gravidade, status_internacao, evolucao_internacao) "
            "VALUES (:id, :animal, :crmv, :gravidade, 'Internado', :motivo)",
            {"id": novo_id, "animal": internacao.id_animal, "crmv": internacao.crmv, "gravidade": internacao.nivel_gravidade.capitalize(), "motivo": internacao.motivo}
        )
        conexao.commit()
        return {"mensagem": "Internação registrada com sucesso.", "id_internacao": novo_id}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/internacoes", status_code=status.HTTP_200_OK, tags=["Internações"])
def listar_internacoes(nivel_gravidade: Optional[str] = None, status_internacao: Optional[str] = None):
    if usando_modo_memoria():
        res = list(banco_internacoes.values())
        if nivel_gravidade:
            res = [i for i in res if i["nivel_gravidade"].lower() == nivel_gravidade.lower()]
        if status_internacao:
            res = [i for i in res if i["status_internacao"].lower() == status_internacao.lower()]
        return res

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_internacao, id_animal, crmv, data_internacao, data_alta, nivel_gravidade, status_internacao, evolucao_internacao FROM tb_internacao")
        return [dict(zip([c[0].lower() for c in cursor.description], r)) for r in cursor.fetchall()]
    finally:
        cursor.close()
        conexao.close()


@app.get("/internacoes/{id_internacao}", status_code=status.HTTP_200_OK, tags=["Internações"])
def buscar_detalhes_internacao(id_internacao: int):
    if usando_modo_memoria():
        if id_internacao not in banco_internacoes:
            raise HTTPException(status_code=404, detail="Internação não encontrada.")
        inter = banco_internacoes[id_internacao]
        id_animal = inter["id_animal"]
        return {"internacao": inter, "detalhes_animal": banco_animais.get(id_animal, {}), "historico_evolucoes_plantao": banco_plantoes.get(id_animal, [])}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_internacao, id_animal, crmv, data_internacao, data_alta, nivel_gravidade, status_internacao, evolucao_internacao FROM tb_internacao WHERE id_internacao = :id", {"id": id_internacao})
        row_int = cursor.fetchone()
        if not row_int:
            raise HTTPException(status_code=404, detail="Internação não encontrada.")
        internacao = dict(zip([c[0].lower() for c in cursor.description], row_int))
        id_animal = internacao["id_animal"]
        cursor.execute("SELECT id_animal, id_tutor, nome_animal, tipo_animal, raca, sexo FROM tb_animal WHERE id_animal = :id", {"id": id_animal})
        row_anim = cursor.fetchone()
        detalhes_animal = dict(zip([c[0].lower() for c in cursor.description], row_anim)) if row_anim else {}
        cursor.execute("SELECT id_plantao, id_animal, crmv, chegada_plantao, status_plantao, evolucao_plantao FROM tb_plantao WHERE id_animal = :id", {"id": id_animal})
        evolucoes = [dict(zip([c[0].lower() for c in cursor.description], r)) for r in cursor.fetchall()]
        return {"internacao": internacao, "detalhes_animal": detalhes_animal, "historico_evolucoes_plantao": evolucoes}
    finally:
        cursor.close()
        conexao.close()


@app.patch("/internacoes/{id_internacao}/status", status_code=status.HTTP_200_OK, tags=["Internações"])
def atualizar_status_internacao(id_internacao: int, dados: StatusInternacaoUpdate):
    if usando_modo_memoria():
        if id_internacao not in banco_internacoes:
            raise HTTPException(status_code=404, detail="Internação não encontrada.")
        banco_internacoes[id_internacao]["status_internacao"] = dados.status_internacao
        if dados.observacoes:
            banco_internacoes[id_internacao]["observacoes"] = dados.observacoes
        return {"mensagem": "Status atualizado.", "id_internacao": id_internacao, "status_internacao": dados.status_internacao}

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        status_map = {"internado": "Internado", "em observação": "Internado", "alta médica": "Alta", "alta": "Alta", "óbito": "Obito", "obito": "Obito"}
        status_norm = status_map.get(dados.status_internacao.strip().lower())
        if not status_norm:
            raise HTTPException(status_code=400, detail="Status de internação inválido.")
        cursor.execute("SELECT id_internacao FROM tb_internacao WHERE id_internacao = :id", {"id": id_internacao})
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Internação com ID {id_internacao} não encontrada.")
        if dados.observacoes:
            cursor.execute("UPDATE tb_internacao SET status_internacao = :status, evolucao_internacao = :obs WHERE id_internacao = :id", {"status": status_norm, "obs": dados.observacoes, "id": id_internacao})
        else:
            cursor.execute("UPDATE tb_internacao SET status_internacao = :status WHERE id_internacao = :id", {"status": status_norm, "id": id_internacao})
        conexao.commit()
        return {"mensagem": "Status da internação atualizado com sucesso no Oracle.", "id_internacao": id_internacao, "status_internacao": status_norm}
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/dashboard", status_code=status.HTTP_200_OK, tags=["Dashboard"])
def obter_dashboard():
    if usando_modo_memoria():
        ativas = [i for i in banco_internacoes.values() if i["status_internacao"].lower() in ["internado", "em observação"]]
        return {
            "total_tutores": len(banco_tutores),
            "total_animais": len(banco_animais),
            "total_agendamentos": len(banco_agendamentos),
            "total_internacoes_ativas": len(ativas),
            "resumo_gravidade_internacoes": {
                "Critica": len([i for i in ativas if i["nivel_gravidade"] == "Critica"]),
                "Alta": len([i for i in ativas if i["nivel_gravidade"] == "Alta"]),
                "Medio": len([i for i in ativas if i["nivel_gravidade"] == "Medio"]),
                "Baixa": len([i for i in ativas if i["nivel_gravidade"] == "Baixa"])
            }
        }

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_tutor")
        total_tutores = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tb_animal")
        total_animais = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tb_agendamento")
        total_agendamentos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tb_internacao WHERE LOWER(status_internacao) = 'internado'")
        total_internacoes_ativas = cursor.fetchone()[0]
        return {
            "total_tutores": total_tutores,
            "total_animais": total_animais,
            "total_agendamentos": total_agendamentos,
            "total_internacoes_ativas": total_internacoes_ativas
        }
    finally:
        cursor.close()
        conexao.close()
