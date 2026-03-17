const API = "http://localhost:5000"
let agendamentoEmEdicao = null

async function criarCliente() {
    const nome = document.getElementById("cliente_nome").value
    const telefone = document.getElementById("cliente_telefone").value

    const res = await fetch(`${API}/clientes`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome,
            telefone
        })
    }) 

    const dados = await res.json()

    alert(dados.mensagem)
}


async function carregarServicos() {
    const res = await fetch(`${API}/servicos`)

    const dados = await res.json()

    const container = document.getElementById("servicos_checkbox")

    container.innerHTML = ""

    dados.dados.forEach(servico => {
        container.innerHTML += `
            <label>
                <input type="checkbox" value="${servico.id}">
                ${servico.nome} - R$ ${servico.preco}
            </label><br>
        `
    })
}

async function criarAgendamento() {
    const clienteNome = document.getElementById("agendamento_cliente_nome").value
    const dataAgendamento = document.getElementById("data_agendamento").value
    const checkboxes = document.querySelectorAll("#servicos_checkbox input[type='checkbox']:checked")
    const servicos = []

    checkboxes.forEach(cb => {
        servicos.push(Number(cb.value))
    })

    const res = await fetch(`${API}/agendamentos`, {

        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            cliente_nome: clienteNome,
            data: dataAgendamento,
            servicos
        })
    })

    const dados = await res.json()

    alert(dados.mensagem)
}

async function filtrarAgendamentos() {
    const dataInicio = document.getElementById("filtro_inicio").value
    const dataFim = document.getElementById("filtro_fim").value

    const res = await fetch(`${API}/agendamentos/historico?data_inicio=${dataInicio}&data_fim=${dataFim}`)

    const dados = await res.json()

    if (!dados.dados) {
        alert(dados.mensagem)
        return
    }

    const tabela = document.getElementById("tabela_agendamentos")
    tabela.innerHTML = ""

    dados.dados.forEach(agendamento => {
        tabela.innerHTML += `
            <tr>
                <td>${agendamento.id}</td>
                <td>${agendamento.cliente}</td>
                <td>${formatarData(agendamento.data)}</td>
                <td>${agendamento.servicos.join(', ')}</td>
                <td>${agendamento.status}</td>
                <td>R$ ${agendamento.valor}</td>
                <td>
                    <button onclick="editarAgendamento(${agendamento.id})">Editar</button>
                    <button onclick="alterarStatus(${agendamento.id})">Status</button>
                </td>
            </tr>
        `
    })

    alert(dados.mensagem)
}

async function listarAgendamentos() {
    const res = await fetch(`${API}/agendamentos`)

    const dados = await res.json()

    const tabela = document.getElementById("tabela_agendamentos")

    tabela.innerHTML = ""

    dados.dados.forEach(agendamento => {
        tabela.innerHTML += `
            <tr>
                <td>${agendamento.id}</td>
                <td>${agendamento.cliente}</td>
                <td>${formatarData(agendamento.data)}</td>
                <td>${agendamento.servicos.join(', ')}</td>
                <td>${agendamento.status}</td>
                <td>R$ ${agendamento.valor}</td>
                <td>
                    <button onclick="editarAgendamento(${agendamento.id})">Editar</button>
                    <button onclick="alterarStatus(${agendamento.id})">Status</button>
                </td>
            </tr>
        `
    })
}

async function editarAgendamento(id) {
    agendamentoEmEdicao = id

    const res = await fetch(`${API}/agendamentos`)

    const dados = await res.json()

    const agendamento = dados.dados.find(a => a.id == id)

    if (!agendamento) return

    document.getElementById("edit_id").textContent = id
    document.getElementById("edit_cliente").value = agendamento.cliente
    document.getElementById("edit_data").value = agendamento.data

    const servicosRes = await fetch(`${API}/servicos`)

    const servicosDados = await servicosRes.json()

    let html = ""

    servicosDados.dados.forEach(servico => {
        const checado = agendamento.servicos.includes(servico.nome) ? "checked" : ""

        html += `
            <label>
                <input type="checkbox" value="${servico.id}" ${checado}>
                ${servico.nome} - R$ ${servico.preco}
            </label><br>
        `
    })

    document.getElementById("edit_servicos").innerHTML = html

    document.getElementById("modalEdicao").style.display = "block"
}

async function salvarEdicao() {
    const data = document.getElementById('edit_data').value

    const admin = document.getElementById('edit_admin').checked
    
    const checkboxes = document.querySelectorAll("#edit_servicos input[type='checkbox']:checked")
    const servicos = []
    checkboxes.forEach(cb => servicos.push(Number(cb.value)))
    
    const res = await fetch(`${API}/agendamentos/${agendamentoEmEdicao}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            data,
            servicos,
            admin
        })
    })
    
    const dados = await res.json()
    alert(dados.mensagem)
    
    fecharModal()
    listarAgendamentos()
}

function fecharModal() {
    document.getElementById('modalEdicao').style.display = 'none'
    agendamentoEmEdicao = null
}

async function alterarStatus(id) {
    const novoStatus = prompt("Novo Status (Agendado, Confirmado, Cancelado, Concluído):")
    if (!novoStatus) return

    const res = await fetch(`${API}/agendamentos/${id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: novoStatus })
    })

    const dados = await res.json()

    alert(dados.mensagem)

    listarAgendamentos()
}

async function relatorioSemanal() {
    const ano = document.getElementById("ano").value
    const semana = document.getElementById("semana").value

    const res = await fetch(`${API}/agendamentos/relatorio-semanal?ano=${ano}&semana=${semana}`)

    const dados = await res.json()

    const relatorio = dados.dados

    if (!relatorio) {
        alert(dados.mensagem)
        return
    }

    let servicosRealizados = ""

    relatorio.servicos_realizados.forEach(servico => {
        servicosRealizados += `
            <li>${servico.servico} - ${servico.quantidade}x</li>
        `
    })

    document.getElementById("relatorio_semanal").innerHTML = `
        <h3>Semana ${relatorio.semana} / ${relatorio.ano}</h3>
        <p><b>Período:</b> ${relatorio.periodo.inicio} até ${relatorio.periodo.fim}</p>
        <p><b>Agendamentos:</b> ${relatorio.agendamentos_total}</p>
        <p><b>Faturamento Total:</b> R$ ${relatorio.faturamento_total}</p>
        <p><b>Ticket Médio:</b> R$ ${relatorio.ticket_medio}</p>

        <h4>Serviços Realizados</h4>
        <ul>
            ${servicosRealizados}
        </ul>
    `
}

function formatarData(data) {
    const partes = data.split("-")
    return `${partes[2]}/${partes[1]}/${partes[0]}`
}

window.onload = () => {
    carregarServicos()
    listarAgendamentos()
}

window.onclick = function(event) {
    const modal = document.getElementById('modalEdicao')
    if (event.target == modal) {
        fecharModal()
    }
}