document.addEventListener("DOMContentLoaded", function() {
    
    // 1. VARIÁVEIS PRINCIPAIS
    const loginForm = document.getElementById('loginForm');
    let perfilLogado = ''; 

    // Referência de todas as telas do sistema
    const telas = {
        login: document.getElementById('tela-login'),
        // Telas Recepcionista
        dashboardRec: document.getElementById('tela-dashboard'),
        cadastroRec: document.getElementById('tela-cadastro'),
        agendamentosRec: document.getElementById('tela-agendamentos'),
        configuracoesRec: document.getElementById('tela-configuracoes'),
        // Telas Veterinário
        dashboardVet: document.getElementById('tela-dashboard-vet'),
        agendamentosVet: document.getElementById('tela-agendamentos-vet'),
        configuracoesVet: document.getElementById('tela-configuracoes-vet'),
        internacoesVet: document.getElementById('tela-internacoes-vet'),
        prontuariosVet: document.getElementById('tela-prontuarios-vet'),
        plantaoVet: document.getElementById('tela-plantao-vet')
    };

    // Função central para trocar as telas
    function mostrarTela(telaNome) {
        Object.values(telas).forEach(tela => {
            if (tela) tela.style.display = 'none';
        });
        if (telas[telaNome]) telas[telaNome].style.display = 'flex';
    }

    // ================= 2. SISTEMA DE LOGIN =================
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Impede a página de recarregar
            
            const loginValue = document.getElementById('login').value.toLowerCase();
            const senhaValue = document.getElementById('senha').value;

            if (loginValue === 'recepcionista' && senhaValue === '123') {
                perfilLogado = 'recepcionista';
                mostrarTela('dashboardRec');
            } else if (loginValue === 'veterinario' && senhaValue === '123') {
                perfilLogado = 'veterinario';
                mostrarTela('dashboardVet');
            } else {
                alert('Login ou senha incorretos.');
            }
        });
    }

    // ================= 3. NAVEGAÇÃO DO MENU LATERAL =================
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const textoBotao = this.innerText.trim();
            
            if (textoBotao === 'Pagina inicial') {
                mostrarTela(perfilLogado === 'veterinario' ? 'dashboardVet' : 'dashboardRec');
            } else if (textoBotao === 'Cadastro') {
                if (perfilLogado === 'recepcionista') mostrarTela('cadastroRec');
            } else if (textoBotao === 'Agendamentos') {
                mostrarTela(perfilLogado === 'veterinario' ? 'agendamentosVet' : 'agendamentosRec');
            } else if (textoBotao === 'Configurações') {
                mostrarTela(perfilLogado === 'veterinario' ? 'configuracoesVet' : 'configuracoesRec');
            } else if (textoBotao === 'Internações') {
                if (perfilLogado === 'veterinario') mostrarTela('internacoesVet');
            } else if (textoBotao === 'Plantão') {
                if (perfilLogado === 'veterinario') mostrarTela('plantaoVet');
            }
        });
    });

    // Botão de Prontuários (dentro de Internações)
    const btnProntuarios = document.querySelector('.btn-prontuarios');
    if (btnProntuarios) {
        btnProntuarios.addEventListener('click', function(e) {
            e.preventDefault();
            if (perfilLogado === 'veterinario') mostrarTela('prontuariosVet');
        });
    }

    // ================= 4. SAIR DA CONTA =================
    function sairDaConta(e) {
        e.preventDefault();
        document.getElementById('login').value = '';
        document.getElementById('senha').value = '';
        perfilLogado = ''; 
        mostrarTela('login');
    }

    const btnSairRec = document.getElementById('btn-sair-conta');
    const btnSairVet = document.getElementById('btn-sair-conta-vet');
    if (btnSairRec) btnSairRec.addEventListener('click', sairDaConta);
    if (btnSairVet) btnSairVet.addEventListener('click', sairDaConta);

    // ================= 5. NOVO AGENDAMENTO (RECEPCIONISTA) =================
    const btnAbrirAgend = document.getElementById('btn-abrir-agendamento');
    const modalAgend = document.getElementById('modal-agendamento');
    const btnCancelarAgend = document.getElementById('btn-cancelar-agend');
    const btnSalvarAgend = document.getElementById('btn-salvar-agend');

    if (btnAbrirAgend) {
        btnAbrirAgend.addEventListener('click', () => modalAgend.style.display = 'flex');
    }
    if (btnCancelarAgend) {
        btnCancelarAgend.addEventListener('click', function() {
            modalAgend.style.display = 'none';
            document.getElementById('input-agend-animal').value = '';
            document.getElementById('input-agend-dia').value = '';
            document.getElementById('input-agend-horario').value = '';
        });
    }
    if (btnSalvarAgend) {
        btnSalvarAgend.addEventListener('click', function() {
            const animal = document.getElementById('input-agend-animal').value;
            const tipoCor = document.getElementById('select-agend-tipo').value;
            const diaValor = document.getElementById('input-agend-dia').value;
            const horario = document.getElementById('input-agend-horario').value;

            if (animal.trim() === '' || diaValor === '' || horario === '') {
                alert('Preencha o nome, dia e horário.');
                return;
            }

            const partesData = diaValor.split('-');
            const mesNumero = partesData[1];
            const diaNumero = partesData[2];
            
            let colunaId = '';
            if (mesNumero === '08') colunaId = 'coluna-agosto';
            else if (mesNumero === '09') colunaId = 'coluna-setembro';
            else if (mesNumero === '10') colunaId = 'coluna-outubro';
            else if (mesNumero === '11') colunaId = 'coluna-novembro';
            else {
                alert('Escolha uma data entre Agosto e Novembro.');
                return;
            }

            const colunaMes = document.getElementById(colunaId);
            if (colunaMes) {
                const novoBloco = document.createElement('div');
                novoBloco.className = `bloco ${tipoCor} bloco-com-texto`; 
                novoBloco.innerHTML = `
                    <span>${animal}</span>
                    <span class="bloco-data-hora">Dia ${diaNumero} às ${horario}</span>
                `;
                colunaMes.insertBefore(novoBloco, colunaMes.children[1]);
            }

            modalAgend.style.display = 'none';
            document.getElementById('input-agend-animal').value = '';
            document.getElementById('input-agend-dia').value = '';
            document.getElementById('input-agend-horario').value = '';
        });
    }

    // ================= 6. PLANTÃO (VETERINÁRIO) =================
    const btnAdicionarPlantao = document.querySelector('.btn-adicionar-plantao');
    const blocoNotasPlantao = document.getElementById('bloco-notas-plantao');
    const btnCancelarPlantao = document.getElementById('btn-cancelar-plantao');
    const btnSalvarPlantao = document.getElementById('btn-salvar-plantao');
    const listaPlantoes = document.getElementById('lista-plantoes');
    const cardVazioPlantao = document.getElementById('card-plantao-vazio');

    if (btnAdicionarPlantao && blocoNotasPlantao) {
        btnAdicionarPlantao.addEventListener('click', () => blocoNotasPlantao.style.display = 'flex');
    }
    if (btnCancelarPlantao) {
        btnCancelarPlantao.addEventListener('click', function() {
            blocoNotasPlantao.style.display = 'none';
            document.getElementById('input-data-plantao').value = '';
            document.getElementById('input-info-plantao').value = '';
        });
    }
    if (btnSalvarPlantao) {
        btnSalvarPlantao.addEventListener('click', function() {
            const dataP = document.getElementById('input-data-plantao').value;
            const infoP = document.getElementById('input-info-plantao').value;

            if (dataP === '' || infoP === '') {
                alert('Preencha a data e as informações.');
                return;
            }
            if (cardVazioPlantao) cardVazioPlantao.style.display = 'none';

            const partesData = dataP.split('-');
            const dataFormatada = `${partesData[2]}/${partesData[1]}/${partesData[0]}`;

            const novoCard = document.createElement('div');
            novoCard.className = 'card-plantao';
            novoCard.innerHTML = `<div class="data-plantao">${dataFormatada}</div><div class="notas-plantao">${infoP}</div>`;
            listaPlantoes.prepend(novoCard);

            blocoNotasPlantao.style.display = 'none';
            document.getElementById('input-data-plantao').value = '';
            document.getElementById('input-info-plantao').value = '';
        });
    }

    // ================= 7. PRONTUÁRIOS (VETERINÁRIO) =================
    const btnNovoProntuario = document.getElementById('btn-novo-prontuario');
    const formNovoProntuario = document.getElementById('form-novo-prontuario');
    const btnCancelarProntuario = document.getElementById('btn-cancelar-prontuario');
    const btnSalvarProntuario = document.getElementById('btn-salvar-prontuario');
    const listaRegistrosProntuario = document.getElementById('lista-registros-prontuario');
    const cardProntuarioVazio = document.getElementById('card-prontuario-vazio');
    const listaPacientes = document.getElementById('lista-pacientes-prontuario');
    const avisoListaVazia = document.getElementById('aviso-lista-vazia');

    if (btnNovoProntuario && formNovoProntuario) {
        btnNovoProntuario.addEventListener('click', () => formNovoProntuario.style.display = 'flex');
    }

    function limparFormularioProntuario() {
        if(document.getElementById('input-pront-animal')) document.getElementById('input-pront-animal').value = '';
        if(document.getElementById('input-pront-tutor')) document.getElementById('input-pront-tutor').value = '';
        if(document.getElementById('input-pront-patologia')) document.getElementById('input-pront-patologia').value = '';
        if(document.getElementById('input-pront-exames')) document.getElementById('input-pront-exames').value = '';
        if(document.getElementById('input-pront-vacinas')) document.getElementById('input-pront-vacinas').value = '';
    }

    if (btnCancelarProntuario) {
        btnCancelarProntuario.addEventListener('click', function() {
            formNovoProntuario.style.display = 'none';
            limparFormularioProntuario();
        });
    }

    if (btnSalvarProntuario) {
        btnSalvarProntuario.addEventListener('click', function() {
            const animal = document.getElementById('input-pront-animal').value.trim();
            const tutor = document.getElementById('input-pront-tutor').value.trim();
            const patologia = document.getElementById('input-pront-patologia').value.trim();
            const exames = document.getElementById('input-pront-exames').value.trim();
            const vacinas = document.getElementById('input-pront-vacinas').value.trim();

            if (animal === '' || tutor === '') {
                alert('O nome do animal e o nome do tutor são obrigatórios!');
                return;
            }

            if (cardProntuarioVazio) cardProntuarioVazio.style.display = 'none';
            if (avisoListaVazia) avisoListaVazia.style.display = 'none';

            let animalJaExiste = false;
            if(listaPacientes) {
                const itensExistentes = listaPacientes.querySelectorAll('.li-animal');
                itensExistentes.forEach(li => {
                    li.classList.remove('ativo');
                    if (li.innerText.toLowerCase() === animal.toLowerCase()) {
                        animalJaExiste = true;
                        li.classList.add('ativo'); 
                    }
                });

                if (!animalJaExiste) {
                    const novoItemLateral = document.createElement('li');
                    novoItemLateral.className = 'li-animal ativo';
                    novoItemLateral.innerText = animal;
                    listaPacientes.appendChild(novoItemLateral);
                }
            }

            if(document.getElementById('titulo-prontuario-animal')) {
                document.getElementById('titulo-prontuario-animal').innerText = animal + ' - Histórico Clínico';
            }

            const dataHoje = new Date().toLocaleDateString('pt-BR'); 
            const novoCard = document.createElement('div');
            novoCard.className = 'card-plantao'; 
            novoCard.innerHTML = `
                <div class="data-plantao">${animal} <span style="font-size: 20px; font-weight: normal;">(Tutor: ${tutor})</span> - <span style="font-size: 20px; color: #666;">${dataHoje}</span></div>
                <div class="notas-plantao">
                    <p style="margin-bottom: 10px;"><strong>Patologia / Estado:</strong> ${patologia || 'Não informado'}</p>
                    <p style="margin-bottom: 10px;"><strong>Exames:</strong> ${exames || 'Nenhum exame'}</p>
                    <p><strong>Vacinações:</strong> ${vacinas || 'Não informado'}</p>
                </div>
            `;
            
            if(listaRegistrosProntuario) listaRegistrosProntuario.prepend(novoCard);

            formNovoProntuario.style.display = 'none';
            limparFormularioProntuario();
        });
    }

}); // Fim do documento