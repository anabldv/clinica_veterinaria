import re
import oracledb 
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI(
    title="Pet & Gatô - Sistema de Gestão Veterinária",
    version="3.0.0",
    description="API REST para controle clínico, cadastros, agendamentos, internações e plantão veterinário."
)

DB_USER = "clinica_veterinaria"
DB_PASSWORD = "clinica_senha"
DB_DSN = "localhost:1521/freepdb1"

def obter_conexao():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

# Converte erros de validação Pydantic no padrão esperado pelo CT02
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
# BANCO DE DADOS EM MEMÓRIA (Dicionários indexados por ID)
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

# Atalhos de compatibilidade
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
    crmv: int
    matricula: int
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
    id_tutor: int
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
    nivel_gravidade: str  # 'Baixa', 'Medio', 'Alta', 'Critica'
    motivo: str
    observacoes: Optional[str] = None


class StatusInternacaoUpdate(BaseModel):
    status_internacao: str  # 'Internado', 'Em Observação', 'Alta Médica', 'Óbito'
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
    """
    Define o plantão do dia:
    - Diurno: 07:00 às 18:59:59 ('YYYY-MM-DD_DIURNO')
    - Noturno: 19:00 às 06:59:59 do dia seguinte ('YYYY-MM-DD_NOTURNO')
    """
    data_str = dt.strftime("%Y-%m-%d")
    if 7 <= dt.hour < 19:
        return f"{data_str}_DIURNO"
    if dt.hour < 7:
        ontem = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
        return f"{ontem}_NOTURNO"
    return f"{data_str}_NOTURNO"


# ==============================================================================
# ROTAS - SPRINT 1
# ==============================================================================

@app.post("/usuarios", status_code=status.HTTP_201_CREATED, tags=["Usuários"])
def cadastrar_usuario(usuario: UsuarioCadastro):
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
        return {"usuario": {"id_usuario": novo_id, "nome": usuario.nome, "email": usuario.email, "perfil": usuario.perfil}, "mensagem": "Usuário criado com sucesso"}
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.post("/tutores", status_code=status.HTTP_201_CREATED, tags=["Tutores"])
def cadastrar_tutor(tutor: TutorCadastro):
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
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_tutor, nome_tutor, cpf_tutor, email_tutor, telefone, observacoes FROM tb_tutor")
        colunas = [col[0].lower() for col in cursor.description]
        tutores = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        return tutores
    finally:
        cursor.close()
        conexao.close()


@app.get("/tutores/{id_tutor}", status_code=status.HTTP_200_OK, tags=["Tutores"])
def buscar_tutor(id_tutor: int):
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
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_animal, id_tutor, nome_animal, tipo_animal, raca, sexo FROM tb_animal")
        colunas = [col[0].lower() for col in cursor.description]
        animais = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        return animais
    finally:
        cursor.close()
        conexao.close()


# ==============================================================================
# ROTAS - SPRINT 2
# ==============================================================================

@app.post("/agendamentos", status_code=status.HTTP_201_CREATED, tags=["Agendamentos"])
def criar_agendamento(agendamento: AgendamentoCadastro):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        crmv = getattr(agendamento, "crmv", None)
        matricula = getattr(agendamento, "matricula", None)

        if not crmv or not matricula:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É obrigatório informar o CRMV do veterinário e a Matrícula do recepcionista."
            )

        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Veterinário com CRMV {crmv} não encontrado.")

        cursor.execute("SELECT COUNT(*) FROM tb_recepcao WHERE matricula = :mat", {"mat": matricula})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recepcionista com matrícula {matricula} não encontrado.")

        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": agendamento.id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal com ID {agendamento.id_animal} não encontrado.")

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
def listar_agendamentos(
    veterinario: Optional[str] = None,
    status_consulta: Optional[str] = None
):
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
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id_animal, status_agendamento 
            FROM tb_agendamento 
            WHERE id_animal = :id AND status_agendamento != 'Cancelado'
        """, {"id": id_agendamento})
        
        registro = cursor.fetchone()
        if not registro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhum agendamento ativo encontrado para o ID informado ({id_agendamento})."
            )

        sql = """
            UPDATE tb_agendamento 
            SET status_agendamento = 'Cancelado' 
            WHERE id_animal = :id AND status_agendamento != 'Cancelado'
        """
        cursor.execute(sql, {"id": id_agendamento})
        conexao.commit()

        return {
            "id_agendamento": id_agendamento,
            "status": "Cancelado",
            "mensagem": "Agendamento cancelado com sucesso no banco Oracle."
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


# ==============================================================================
# ROTAS - SPRINT 3
# ==============================================================================

@app.post("/prontuarios", status_code=status.HTTP_201_CREATED, tags=["Prontuários"])
def criar_prontuario(prontuario: ProntuarioCadastro, request: Request):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": prontuario.crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Veterinário com CRMV {prontuario.crmv} não encontrado.")

        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": prontuario.id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal com ID {prontuario.id_animal} não encontrado.")

        cursor.execute("SELECT NVL(MAX(id_prontuario), 0) + 1 FROM tb_prontuario")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO tb_prontuario (id_prontuario, crmv, id_animal, peso_atual, queixa, anamnese, diagnostico, receita, vacina)
            VALUES (:id, :crmv, :animal, :peso, :queixa, :anamnese, :diag, :receita, :vacina)
        """
        cursor.execute(sql, {
            "id": novo_id,
            "crmv": prontuario.crmv,
            "animal": prontuario.id_animal,
            "peso": prontuario.peso_atual,
            "queixa": prontuario.queixa,
            "anamnese": prontuario.anamnese,
            "diag": prontuario.diagnostico,
            "receita": prontuario.receita,
            "vacina": prontuario.vacina
        })
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
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado.")

        cursor.execute(
            "SELECT id_prontuario, crmv, id_animal, data_abertura, peso_atual, queixa, anamnese, diagnostico, receita, vacina "
            "FROM tb_prontuario WHERE id_animal = :id",
            {"id": id_animal}
        )
        colunas_pront = [col[0].lower() for col in cursor.description]
        prontuarios = [dict(zip(colunas_pront, row)) for row in cursor.fetchall()]

        cursor.execute(
            "SELECT v.data_aplicacao, v.crmv, v.id_prontuario, v.nome_vacina, v.lote_vacina, v.data_proxima_dose "
            "FROM tb_vacinacao v "
            "JOIN tb_prontuario p ON v.id_prontuario = p.id_prontuario "
            "WHERE p.id_animal = :id",
            {"id": id_animal}
        )
        colunas_vac = [col[0].lower() for col in cursor.description]
        vacinacoes = [dict(zip(colunas_vac, row)) for row in cursor.fetchall()]

        return {
            "id_animal": id_animal,
            "prontuarios": prontuarios,
            "vacinacoes": vacinacoes
        }
    finally:
        cursor.close()
        conexao.close()


@app.post("/plantao", status_code=status.HTTP_201_CREATED, tags=["Plantão"])
def registrar_plantao(plantao: PlantaoCadastro, request: Request):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": plantao.crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Veterinário com CRMV {plantao.crmv} não encontrado.")

        cursor.execute("SELECT id_tutor FROM tb_animal WHERE id_animal = :id", {"id": plantao.id_animal})
        res_animal = cursor.fetchone()
        if not res_animal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal com ID {plantao.id_animal} não encontrado.")

        id_tutor_final = plantao.id_tutor or res_animal[0]

        cursor.execute("SELECT NVL(MAX(id_plantao), 0) + 1 FROM tb_plantao")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO tb_plantao (id_plantao, id_animal, id_tutor, crmv, status_plantao, evolucao_plantao)
            VALUES (:id, :animal, :tutor, :crmv, 'Em analise', :evolucao)
        """
        cursor.execute(sql, {
            "id": novo_id,
            "animal": plantao.id_animal,
            "tutor": id_tutor_final,
            "crmv": plantao.crmv,
            "evolucao": plantao.evolucao_plantao
        })
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
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado.")

        cursor.execute(
            "SELECT id_plantao, id_animal, id_tutor, crmv, chegada_plantao, status_plantao, evolucao_plantao "
            "FROM tb_plantao WHERE id_animal = :id",
            {"id": id_animal}
        )
        colunas = [col[0].lower() for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conexao.close()


@app.post("/internacoes", status_code=status.HTTP_201_CREATED, tags=["Internações"])
def criar_internacao(internacao: InternacaoCadastro):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tb_veterinario WHERE crmv = :crmv", {"crmv": internacao.crmv})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Veterinário com CRMV {internacao.crmv} não encontrado.")

        cursor.execute("SELECT COUNT(*) FROM tb_animal WHERE id_animal = :id", {"id": internacao.id_animal})
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal com ID {internacao.id_animal} não encontrado.")

        cursor.execute("SELECT NVL(MAX(id_internacao), 0) + 1 FROM tb_internacao")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO tb_internacao (id_internacao, id_animal, crmv, nivel_gravidade, status_internacao, evolucao_internacao)
            VALUES (:id, :animal, :crmv, :gravidade, 'Internado', :motivo)
        """
        cursor.execute(sql, {
            "id": novo_id,
            "animal": internacao.id_animal,
            "crmv": internacao.crmv,
            "gravidade": internacao.nivel_gravidade.capitalize(),
            "motivo": internacao.motivo
        })
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
def listar_internacoes():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT id_internacao, id_animal, crmv, data_internacao, data_alta, 
                   nivel_gravidade, status_internacao, evolucao_internacao 
            FROM tb_internacao
        """)
        colunas = [col[0].lower() for col in cursor.description]
        internacoes = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        return internacoes
    finally:
        cursor.close()
        conexao.close()


@app.get("/internacoes/{id_internacao}", status_code=status.HTTP_200_OK, tags=["Internações"])
def buscar_detalhes_internacao(id_internacao: int):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT id_internacao, id_animal, crmv, data_internacao, data_alta, "
            "nivel_gravidade, status_internacao, evolucao_internacao "
            "FROM tb_internacao WHERE id_internacao = :id",
            {"id": id_internacao}
        )
        row_int = cursor.fetchone()
        if not row_int:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internação não encontrada.")
        
        colunas_int = [col[0].lower() for col in cursor.description]
        internacao = dict(zip(colunas_int, row_int))
        id_animal = internacao["id_animal"]

        cursor.execute(
            "SELECT id_animal, id_tutor, nome_animal, tipo_animal, raca, sexo FROM tb_animal WHERE id_animal = :id",
            {"id": id_animal}
        )
        row_anim = cursor.fetchone()
        detalhes_animal = dict(zip([col[0].lower() for col in cursor.description], row_anim)) if row_anim else {}

        cursor.execute(
            "SELECT id_plantao, id_animal, crmv, chegada_plantao, status_plantao, evolucao_plantao "
            "FROM tb_plantao WHERE id_animal = :id",
            {"id": id_animal}
        )
        colunas_pl = [col[0].lower() for col in cursor.description]
        evolucoes = [dict(zip(colunas_pl, row)) for row in cursor.fetchall()]

        return {
            "internacao": internacao,
            "detalhes_animal": detalhes_animal,
            "historico_evolucoes_plantao": evolucoes
        }
    finally:
        cursor.close()
        conexao.close()


@app.patch("/internacoes/{id_internacao}/status", status_code=status.HTTP_200_OK, tags=["Internações"])
def atualizar_status_internacao(id_internacao: int, dados: StatusInternacaoUpdate):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        status_map = {
            "internado": "Internado",
            "em observação": "Internado",
            "alta médica": "Alta",
            "alta": "Alta",
            "óbito": "Obito",
            "obito": "Obito"
        }
        
        status_normalizado = status_map.get(dados.status_internacao.strip().lower())
        if not status_normalizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status de internação inválido. Valores aceitos: 'Internado', 'Alta', 'Obito'."
            )

        cursor.execute("SELECT id_internacao FROM tb_internacao WHERE id_internacao = :id", {"id": id_internacao})
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Internação com ID {id_internacao} não encontrada."
            )

        if dados.observacoes:
            sql = """
                UPDATE tb_internacao 
                SET status_internacao = :status, evolucao_internacao = :obs 
                WHERE id_internacao = :id
            """
            cursor.execute(sql, {"status": status_normalizado, "obs": dados.observacoes, "id": id_internacao})
        else:
            sql = """
                UPDATE tb_internacao 
                SET status_internacao = :status 
                WHERE id_internacao = :id
            """
            cursor.execute(sql, {"status": status_normalizado, "id": id_internacao})

        conexao.commit()

        return {
            "mensagem": "Status da internação atualizado com sucesso no Oracle.",
            "id_internacao": id_internacao,
            "status_internacao": status_normalizado
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        conexao.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        cursor.close()
        conexao.close()


@app.get("/dashboard", status_code=status.HTTP_200_OK, tags=["Dashboard"])
def obter_dashboard():
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
