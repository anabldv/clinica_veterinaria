document.addEventListener("DOMContentLoaded", function() {
    const API_URL = "http://127.0.0.1:8000";

    // 1. ESTADO DA SESSÃO
    let usuarioLogado = JSON.parse(localStorage.getItem("petgato_usuario")) || null;
    let perfilLogado = usuarioLogado ? normalizarPerfil(usuarioLogado.perfil) : "";
    let animalSelecionadoProntuario = null;

    function normalizarPerfil(perfil) {
        if (!perfil) return "";
        const p = perfil.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        return p.includes("vet") ? "veterinario" : "recepcionista";
    }

    // Referência de todas as telas do sistema
    const telas = {
        login: document.getElementById("tela-login"),
        // Telas Recepcionista
        dashboardRec: document.getElementById("tela-dashboard"),
        cadastroRec: document.getElementById("tela-cadastro"),
        agendamentosRec: document.getElementById("tela-agendamentos"),
        configuracoesRec: document.getElementById("tela-configuracoes"),
        // Telas Veterinário
        dashboardVet: document.getElementById("tela-dashboard-vet"),
        agendamentosVet: document.getElementById("tela-agendamentos-vet"),
        configuracoesVet: document.getElementById("tela-configuracoes-vet"),
        internacoesVet: document.getElementById("tela-internacoes-vet"),
        prontuariosVet: document.getElementById("tela-prontuarios-vet"),
        plantaoVet: document.getElementById("tela-plantao-vet")
    };

    function atualizarNomeSidebar() {
        const spans = document.querySelectorAll(".nome-usuario-logado");
        spans.forEach(span => {
            if (usuarioLogado && usuarioLogado.nome) {
                span.innerText = usuarioLogado.nome;
            } else {
                span.innerText = perfilLogado === "veterinario" ? "Veterinário" : "Recepcionista";
            }
        });
    }

    // Função central para trocar as telas e disparar carregamento da API
    function mostrarTela(telaNome) {
        Object.values(telas).forEach(tela => {
            if (tela) tela.style.display = "none";
        });
        if (telas[telaNome]) {
            telas[telaNome].style.display = "flex";
        }
        atualizarNomeSidebar();

        // Carregamento automático de dados ao abrir cada tela
        if (telaNome === "dashboardRec" || telaNome === "dashboardVet") {
            carregarDashboard();
        } else if (telaNome === "cadastroRec") {
            carregarSelectTutores();
        } else if (telaNome === "agendamentosRec" || telaNome === "agendamentosVet") {
            carregarAgendamentos();
            carregarSelectAnimais("select-agend-animal");
        } else if (telaNome === "internacoesVet") {
            carregarInternacoes();
        } else if (telaNome === "prontuariosVet") {
            carregarListaPacientesProntuario();
        } else if (telaNome === "plantaoVet") {
            carregarSelectAnimais("select-plantao-animal-filtro");
            carregarSelectAnimais("select-plantao-animal");
        }
    }

    // Helper para extrair mensagens de erro do FastAPI
    function extrairMensagemErro(erroData, fallback) {
        if (!erroData) return fallback;
        if (typeof erroData.detail === "string") return erroData.detail;
        if (erroData.detail && erroData.detail.mensagem) return erroData.detail.mensagem;
        return fallback;
    }

    // Se já houver sessão salva, restaura a tela inicial
    if (usuarioLogado) {
        mostrarTela(perfilLogado === "veterinario" ? "dashboardVet" : "dashboardRec");
    }

    // ================= 2. SISTEMA DE LOGIN (POST /login) =================
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function(event) {
            event.preventDefault();

            const email = document.getElementById("login").value.trim();
            const senha = document.getElementById("senha").value;

            try {
                const resposta = await fetch(`${API_URL}/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, senha })
                });

                const dados = await resposta.json();

                if (!resposta.ok) {
                    alert(extrairMensagemErro(dados, "E-mail ou senha incorretos."));
                    return;
                }

                usuarioLogado = dados.usuario;
                perfilLogado = normalizarPerfil(usuarioLogado.perfil);
                localStorage.setItem("petgato_usuario", JSON.stringify(usuarioLogado));

                mostrarTela(perfilLogado === "veterinario" ? "dashboardVet" : "dashboardRec");
            } catch (erro) {
                console.error("Erro no login:", erro);
                alert("Não foi possível conectar ao servidor da API. Verifique se o FastAPI está rodando na porta 8000.");
            }
        });
    }

    // ================= 3. NAVEGAÇÃO DO MENU LATERAL =================
    const menuItems = document.querySelectorAll(".menu-item");
    menuItems.forEach(item => {
        item.addEventListener("click", function(e) {
            e.preventDefault();
            const textoBotao = this.innerText.trim();

            if (textoBotao === "Pagina inicial") {
                mostrarTela(perfilLogado === "veterinario" ? "dashboardVet" : "dashboardRec");
            } else if (textoBotao === "Cadastro") {
                if (perfilLogado === "recepcionista") mostrarTela("cadastroRec");
            } else if (textoBotao === "Agendamentos") {
                mostrarTela(perfilLogado === "veterinario" ? "agendamentosVet" : "agendamentosRec");
            } else if (textoBotao === "Configurações") {
                mostrarTela(perfilLogado === "veterinario" ? "configuracoesVet" : "configuracoesRec");
            } else if (textoBotao === "Internações") {
                if (perfilLogado === "veterinario") mostrarTela("internacoesVet");
            } else if (textoBotao === "Plantão") {
                if (perfilLogado === "veterinario") mostrarTela("plantaoVet");
            }
        });
    });

    const btnProntuarios = document.querySelector(".btn-prontuarios");
    if (btnProntuarios) {
        btnProntuarios.addEventListener("click", function(e) {
            e.preventDefault();
            if (perfilLogado === "veterinario") mostrarTela("prontuariosVet");
        });
    }

    // ================= 4. SAIR DA CONTA =================
    function sairDaConta(e) {
        e.preventDefault();
        localStorage.removeItem("petgato_usuario");
        usuarioLogado = null;
        perfilLogado = "";
        document.getElementById("login").value = "";
        document.getElementById("senha").value = "";
        mostrarTela("login");
    }

    ["btn-sair-conta", "btn-sair-conta-vet", "btn-trocar-conta-rec", "btn-trocar-conta-vet"].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.addEventListener("click", sairDaConta);
    });

    // ================= 5. DASHBOARD (GET /dashboard) =================
    async function carregarDashboard() {
        try {
            const resp = await fetch(`${API_URL}/dashboard`);
            if (!resp.ok) return;
            const dados = await resp.json();

            const sufixo = perfilLogado === "veterinario" ? "vet" : "rec";
            const elTutores = document.getElementById(`dash-tutores-${sufixo}`);
            const elAnimais = document.getElementById(`dash-animais-${sufixo}`);
            const elInternacoes = document.getElementById(`dash-internacoes-${sufixo}`);
            const elAgendamentos = document.getElementById(`dash-agendamentos-${sufixo}`);

            if (elTutores) elTutores.innerText = dados.total_tutores ?? 0;
            if (elAnimais) elAnimais.innerText = dados.total_animais ?? 0;
            if (elInternacoes) elInternacoes.innerText = dados.total_internacoes_ativas ?? 0;
            if (elAgendamentos) elAgendamentos.innerText = dados.total_agendamentos ?? 0;
        } catch (err) {
            console.error("Erro ao carregar dashboard:", err);
        }
    }

    // ================= 6. CADASTROS (TUTOR E ANIMAL) =================
    async function carregarSelectTutores() {
        const select = document.getElementById("animal-id-tutor");
        if (!select) return;
        try {
            const resp = await fetch(`${API_URL}/tutores`);
            const tutores = await resp.json();
            select.innerHTML = '<option value="">Selecione um tutor...</option>';
            tutores.forEach(t => {
                const nome = t.nome_tutor || t.nome;
                const opt = document.createElement("option");
                opt.value = t.id_tutor;
                opt.innerText = `${t.id_tutor} - ${nome} (CPF: ${t.cpf_tutor || t.cpf})`;
                select.appendChild(opt);
            });
        } catch (err) {
            console.error("Erro ao carregar tutores:", err);
        }
    }

    async function carregarRegistros(tipo) {
        const lista = document.getElementById("lista-registros-dashboard");
        if (!lista) return;

        const rotas = {
            tutores: "/tutores",
            animais: "/animais",
            internacoes: "/internacoes",
            agendamentos: "/agendamentos"
        };

        const titulos = {
            tutores: "Tutores cadastrados",
            animais: "Animais cadastrados",
            internacoes: "Internações registradas",
            agendamentos: "Agendamentos realizados"
        };

        lista.innerHTML = "<p>Carregando registros...</p>";

        try {
            const resp = await fetch(`${API_URL}${rotas[tipo]}`);
            if (!resp.ok) throw new Error("Erro ao buscar registros.");

            const registros = await resp.json();

            const colunas = registros.length
                ? [...new Set(registros.flatMap(r => Object.keys(r)))]
                : ["Nenhum registro cadastrado"];

            const escapar = valor => String(valor ?? "-")
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");

            lista.style.display = "flex";

            lista.innerHTML = `
                <button id="btn-voltar-registros" class="btn-voltar-registros">
                    ← Voltar
                </button>

                <h2>${titulos[tipo]}</h2>

                ${!registros.length ? "<p>Nenhum registro encontrado.</p>" : `
                    <table class="tabela-registros">
                        <thead>
                            <tr>
                                ${colunas.map(c => `<th>${escapar(c.replace(/_/g, " "))}</th>`).join("")}
                            </tr>
                        </thead>
                        <tbody>
                            ${registros.map(r => `
                                <tr>
                                    ${colunas.map(c => `<td>${escapar(r[c])}</td>`).join("")}
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                `}
            `;

            document.querySelectorAll(".cards-grid").forEach(grid => {
                grid.style.display = "none";
            });

            document.getElementById("btn-voltar-registros").addEventListener("click", () => {
                lista.style.display = "none";

                document.querySelectorAll(".cards-grid").forEach(grid => {
                    grid.style.display = "";
                });
            });
            
        } catch (err) {
            console.error("Erro ao carregar registros:", err);
            lista.innerHTML = "<p>Não foi possível carregar os registros.</p>";
        }
    }

    document.querySelectorAll(".cards-grid .card").forEach(card => {
        card.addEventListener("click", function() {
            carregarRegistros(this.dataset.tipo);
        });
    });

    const formTutor = document.getElementById("form-cadastro-tutor");
    if (formTutor) {
        formTutor.addEventListener("submit", async function(e) {
            e.preventDefault();
            const payload = {
                nome: document.getElementById("tutor-nome").value.trim(),
                cpf: document.getElementById("tutor-cpf").value.trim(),
                email: document.getElementById("tutor-email").value.trim(),
                telefone: document.getElementById("tutor-telefone").value.trim(),
                observacoes: document.getElementById("tutor-obs").value.trim() || null
            };

            try {
                const resp = await fetch(`${API_URL}/tutores`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const dados = await resp.json();
                if (!resp.ok) {
                    alert(extrairMensagemErro(dados, "Erro ao cadastrar tutor."));
                    return;
                }
                alert("Tutor cadastrado com sucesso!");
                formTutor.reset();
                carregarSelectTutores();
            } catch (err) {
                alert("Falha de comunicação ao cadastrar tutor.");
            }
        });
    }

    const formAnimal = document.getElementById("form-cadastro-animal");
    if (formAnimal) {
        formAnimal.addEventListener("submit", async function(e) {
            e.preventDefault();
            const idTutor = parseInt(document.getElementById("animal-id-tutor").value, 10);
            if (!idTutor) {
                alert("Selecione um tutor válido.");
                return;
            }

            const payload = {
                id_tutor: idTutor,
                nome: document.getElementById("animal-nome").value.trim(),
                tipo_animal: document.getElementById("animal-tipo").value.trim(),
                raca: document.getElementById("animal-raca").value.trim() || null,
                sexo: document.getElementById("animal-sexo").value,
                data_nascimento: document.getElementById("animal-nasc").value || null
            };

            try {
                const resp = await fetch(`${API_URL}/animais`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const dados = await resp.json();
                if (!resp.ok) {
                    alert(extrairMensagemErro(dados, "Erro ao cadastrar animal."));
                    return;
                }
                alert("Animal cadastrado com sucesso!");
                formAnimal.reset();
            } catch (err) {
                alert("Falha de comunicação ao cadastrar animal.");
            }
        });
    }

    // Helper para popular selects de animais
    async function carregarSelectAnimais(selectId) {
        const select = document.getElementById(selectId);
        if (!select) return;
        try {
            const resp = await fetch(`${API_URL}/animais`);
            const animais = await resp.json();
            select.innerHTML = '<option value="">Selecione o animal...</option>';
            animais.forEach(a => {
                const nome = a.nome_animal || a.nome;
                const tipo = a.tipo_animal || "";
                const opt = document.createElement("option");
                opt.value = a.id_animal;
                opt.innerText = `${a.id_animal} - ${nome} (${tipo})`;
                select.appendChild(opt);
            });
        } catch (err) {
            console.error("Erro ao listar animais:", err);
        }
    }

    // ================= 7. AGENDAMENTOS (GET & POST /agendamentos) =================
    const btnAbrirAgend = document.getElementById("btn-abrir-agendamento");
    const modalAgend = document.getElementById("modal-agendamento");
    const btnCancelarAgend = document.getElementById("btn-cancelar-agend");
    const btnSalvarAgend = document.getElementById("btn-salvar-agend");

    if (btnAbrirAgend) {
        btnAbrirAgend.addEventListener("click", () => modalAgend.style.display = "flex");
    }
    if (btnCancelarAgend) {
        btnCancelarAgend.addEventListener("click", () => modalAgend.style.display = "none");
    }

    async function carregarAgendamentos() {
        const prefixo = perfilLogado === "veterinario" ? "vet-" : "";
        const mesesMap = {
            "08": { id: `${prefixo}coluna-agosto`, titulo: "Agosto" },
            "09": { id: `${prefixo}coluna-setembro`, titulo: "Setembro" },
            "10": { id: `${prefixo}coluna-outubro`, titulo: "Outubro" },
            "11": { id: `${prefixo}coluna-novembro`, titulo: "Novembro" }
        };

        // Limpa colunas mantendo o título
        Object.values(mesesMap).forEach(m => {
            const col = document.getElementById(m.id);
            if (col) col.innerHTML = `<div class="mes-titulo">${m.titulo}</div>`;
        });

        try {
            const resp = await fetch(`${API_URL}/agendamentos`);
            if (!resp.ok) return;
            const lista = await resp.json();

            lista.forEach(ag => {
                const dataRaw = ag.hora_agendamento || ag.data_hora;
                if (!dataRaw) return;
                const dt = new Date(dataRaw);
                const mes = String(dt.getMonth() + 1).padStart(2, "0");
                const dia = String(dt.getDate()).padStart(2, "0");
                const hora = `${String(dt.getHours()).padStart(2, "0")}:${String(dt.getMinutes()).padStart(2, "0")}`;

                const alvo = mesesMap[mes];
                if (!alvo) return;

                const col = document.getElementById(alvo.id);
                if (!col) return;

                const isVacina = (ag.tipo_servico || "").toLowerCase().includes("vacina");
                const cor = isVacina ? "vermelho" : "cinza";
                const nomeAnimal = ag.nome_animal || `Animal #${ag.id_animal}`;

                const bloco = document.createElement("div");
                bloco.className = `bloco ${cor} bloco-com-texto`;
                bloco.innerHTML = `
                    <span>${nomeAnimal}</span>
                    <span class="bloco-data-hora">Dia ${dia} às ${hora}</span>
                `;
                col.appendChild(bloco);
            });
        } catch (err) {
            console.error("Erro ao carregar agendamentos:", err);
        }
    }

    if (btnSalvarAgend) {
        btnSalvarAgend.addEventListener("click", async function() {
            const idAnimal = parseInt(document.getElementById("select-agend-animal").value, 10);
            const diaValor = document.getElementById("input-agend-dia").value;
            const horario = document.getElementById("input-agend-horario").value;
            const tipoServico = document.getElementById("select-agend-tipo").value;
            const crmv = parseInt(document.getElementById("input-agend-crmv").value, 10);
            const matricula = parseInt(document.getElementById("input-agend-matricula").value, 10);

            if (!idAnimal || !diaValor || !horario) {
                alert("Preencha o animal, a data e o horário.");
                return;
            }

            const payload = {
                id_animal: idAnimal,
                crmv: crmv,
                matricula: matricula,
                data_hora: `${diaValor} ${horario}`,
                tipo_servico: tipoServico
            };

            try {
                const resp = await fetch(`${API_URL}/agendamentos`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const dados = await resp.json();
                if (!resp.ok) {
                    alert(extrairMensagemErro(dados, "Erro ao criar agendamento."));
                    return;
                }

                alert("Agendamento realizado com sucesso!");
                modalAgend.style.display = "none";
                carregarAgendamentos();
            } catch (err) {
                alert("Falha de comunicação ao agendar.");
            }
        });
    }

    // ================= 8. INTERNAÇÕES (GET /internacoes) =================
    async function carregarInternacoes() {
        const grid = document.getElementById("grid-internacoes-lista");
        if (!grid) return;

        try {
            const resp = await fetch(`${API_URL}/internacoes`);
            const lista = await resp.json();

            if (!lista.length) {
                grid.innerHTML = '<p style="font-size: 26px; color: #666;">Nenhum animal internado no momento.</p>';
                return;
            }

            grid.innerHTML = "";
            lista.forEach(item => {
                const grav = (item.nivel_gravidade || "Baixa").toLowerCase();
                let classeCor = "verde";
                if (grav.includes("med")) classeCor = "amarela";
                else if (grav.includes("alt")) classeCor = "vermelha";
                else if (grav.includes("crit")) classeCor = "roxa";

                const nome = item.animal_nome || `Animal #${item.id_animal}`;
                const card = document.createElement("div");
                card.className = "card-animal";
                card.innerHTML = `
                    <span>${nome}</span>
                    <div class="status-pilula ${classeCor}">${item.nivel_gravidade}</div>
                `;
                grid.appendChild(card);
            });
        } catch (err) {
            console.error("Erro ao carregar internações:", err);
        }
    }

    // ================= 9. PRONTUÁRIOS (VETERINÁRIO) =================
    const btnNovoProntuario = document.getElementById("btn-novo-prontuario");
    const formNovoProntuario = document.getElementById("form-novo-prontuario");
    const btnCancelarProntuario = document.getElementById("btn-cancelar-prontuario");
    const btnSalvarProntuario = document.getElementById("btn-salvar-prontuario");

    if (btnNovoProntuario) {
        btnNovoProntuario.addEventListener("click", () => {
            if (!animalSelecionadoProntuario) {
                alert("Selecione primeiro um paciente na lista à esquerda.");
                return;
            }
            formNovoProntuario.style.display = "flex";
        });
    }

    if (btnCancelarProntuario) {
        btnCancelarProntuario.addEventListener("click", () => {
            formNovoProntuario.style.display = "none";
        });
    }

    async function carregarListaPacientesProntuario() {
        const ul = document.getElementById("lista-pacientes-prontuario");
        if (!ul) return;

        try {
            const resp = await fetch(`${API_URL}/animais`);
            const animais = await resp.json();
            ul.innerHTML = "";

            if (!animais.length) {
                ul.innerHTML = '<li style="font-size: 20px; color: #666;">Nenhum paciente cadastrado.</li>';
                return;
            }

            animais.forEach(a => {
                const nome = a.nome_animal || a.nome;
                const li = document.createElement("li");
                li.className = "li-animal";
                li.innerText = `${nome} (#${a.id_animal})`;
                li.addEventListener("click", () => {
                    document.querySelectorAll("#lista-pacientes-prontuario .li-animal").forEach(el => el.classList.remove("ativo"));
                    li.classList.add("ativo");
                    animalSelecionadoProntuario = { id_animal: a.id_animal, nome };
                    document.getElementById("titulo-prontuario-animal").innerText = `${nome} - Histórico Clínico`;
                    carregarProntuariosDoAnimal(a.id_animal);
                });
                ul.appendChild(li);
            });
        } catch (err) {
            console.error("Erro ao listar pacientes:", err);
        }
    }

    async function carregarProntuariosDoAnimal(idAnimal) {
        const container = document.getElementById("lista-registros-prontuario");
        if (!container) return;

        try {
            const resp = await fetch(`${API_URL}/animais/${idAnimal}/prontuarios`);
            const dados = await resp.json();
            const prontuarios = dados.prontuarios || [];

            if (!prontuarios.length) {
                container.innerHTML = `
                    <div class="card-plantao vazio">
                        <div class="notas-plantao">Nenhum histórico clínico registrado para este paciente. Clique em "+ Novo Prontuário" para adicionar.</div>
                    </div>`;
                return;
            }

            container.innerHTML = "";
            prontuarios.reverse().forEach(p => {
                const dataStr = p.data_abertura ? new Date(p.data_abertura).toLocaleDateString("pt-BR") : "Registro Clínico";
                const card = document.createElement("div");
                card.className = "card-plantao";
                card.innerHTML = `
                    <div class="data-plantao">${dataStr} — Peso: ${p.peso_atual} kg (CRMV: ${p.crmv})</div>
                    <div class="notas-plantao">
                        <p><strong>Queixa:</strong> ${p.queixa}</p>
                        <p><strong>Diagnóstico:</strong> ${p.diagnostico}</p>
                        <p><strong>Receita:</strong> ${p.receita || "Nenhuma"}</p>
                        ${p.vacina ? `<p><strong>Vacina:</strong> ${p.vacina}</p>` : ""}
                    </div>
                `;
                container.appendChild(card);
            });
        } catch (err) {
            console.error("Erro ao carregar prontuários:", err);
        }
    }

    if (btnSalvarProntuario) {
        btnSalvarProntuario.addEventListener("click", async function() {
            if (!animalSelecionadoProntuario) return;

            const payload = {
                crmv: parseInt(document.getElementById("input-pront-crmv").value, 10),
                id_animal: animalSelecionadoProntuario.id_animal,
                peso_atual: parseFloat(document.getElementById("input-pront-peso").value),
                queixa: document.getElementById("input-pront-queixa").value.trim(),
                diagnostico: document.getElementById("input-pront-diagnostico").value.trim(),
                receita: document.getElementById("input-pront-receita").value.trim() || null,
                vacina: document.getElementById("input-pront-vacinas").value.trim() || null
            };

            if (!payload.peso_atual || !payload.queixa || !payload.diagnostico) {
                alert("Preencha peso, queixa e diagnóstico.");
                return;
            }

            try {
                const resp = await fetch(`${API_URL}/prontuarios`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-perfil": "veterinario"
                    },
                    body: JSON.stringify(payload)
                });
                const dados = await resp.json();
                if (!resp.ok) {
                    alert(extrairMensagemErro(dados, "Erro ao salvar prontuário."));
                    return;
                }

                alert("Prontuário salvo com sucesso!");
                formNovoProntuario.style.display = "none";
                carregarProntuariosDoAnimal(animalSelecionadoProntuario.id_animal);
            } catch (err) {
                alert("Falha ao comunicar com a API.");
            }
        });
    }

    // ================= 10. PLANTÃO (VETERINÁRIO) =================
    const btnAbrirPlantao = document.getElementById("btn-abrir-plantao");
    const blocoNotasPlantao = document.getElementById("bloco-notas-plantao");
    const btnCancelarPlantao = document.getElementById("btn-cancelar-plantao");
    const btnSalvarPlantao = document.getElementById("btn-salvar-plantao");
    const filtroPlantaoAnimal = document.getElementById("select-plantao-animal-filtro");

    if (btnAbrirPlantao) {
        btnAbrirPlantao.addEventListener("click", () => blocoNotasPlantao.style.display = "flex");
    }
    if (btnCancelarPlantao) {
        btnCancelarPlantao.addEventListener("click", () => blocoNotasPlantao.style.display = "none");
    }
    if (filtroPlantaoAnimal) {
        filtroPlantaoAnimal.addEventListener("change", function() {
            if (this.value) carregarPlantoesAnimal(parseInt(this.value, 10));
        });
    }

    async function carregarPlantoesAnimal(idAnimal) {
        const lista = document.getElementById("lista-plantoes");
        if (!lista) return;

        try {
            const resp = await fetch(`${API_URL}/plantao/${idAnimal}`);
            const registros = await resp.json();

            if (!registros.length) {
                lista.innerHTML = `
                    <div class="card-plantao vazio">
                        <div class="notas-plantao">Nenhum registro de plantão encontrado para este animal.</div>
                    </div>`;
                return;
            }

            lista.innerHTML = "";
            registros.reverse().forEach(r => {
                const dt = r.chegada_plantao ? new Date(r.chegada_plantao).toLocaleString("pt-BR") : "Plantão";
                const card = document.createElement("div");
                card.className = "card-plantao";
                card.innerHTML = `
                    <div class="data-plantao">${dt} — CRMV: ${r.crmv} (${r.status_plantao})</div>
                    <div class="notas-plantao">${r.evolucao_plantao || ""}</div>
                `;
                lista.appendChild(card);
            });
        } catch (err) {
            console.error("Erro ao carregar plantões:", err);
        }
    }

    if (btnSalvarPlantao) {
        btnSalvarPlantao.addEventListener("click", async function() {
            const idAnimal = parseInt(document.getElementById("select-plantao-animal").value, 10);
            const crmv = parseInt(document.getElementById("input-plantao-crmv").value, 10);
            const evolucao = document.getElementById("input-info-plantao").value.trim();

            if (!idAnimal || !evolucao) {
                alert("Selecione o animal e preencha a evolução do plantão.");
                return;
            }

            try {
                const resp = await fetch(`${API_URL}/plantao`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-perfil": "veterinario"
                    },
                    body: JSON.stringify({
                        id_animal: idAnimal,
                        crmv: crmv,
                        evolucao_plantao: evolucao
                    })
                });
                const dados = await resp.json();
                if (!resp.ok) {
                    alert(extrairMensagemErro(dados, "Erro ao registrar plantão."));
                    return;
                }

                alert("Registro de plantão salvo!");
                blocoNotasPlantao.style.display = "none";
                document.getElementById("input-info-plantao").value = "";
                if (filtroPlantaoAnimal) filtroPlantaoAnimal.value = idAnimal;
                carregarPlantoesAnimal(idAnimal);
            } catch (err) {
                alert("Falha de comunicação ao salvar plantão.");
            }
        });
    }
});
