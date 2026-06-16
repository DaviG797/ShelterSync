import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import Count from '../components/Count'

function Unidade() {

  const navigate = useNavigate() // Para mudança de rota (página)

  const [unidade, setUnidade] = useState([]) // Cria uma caixa vazia para guardar as instituições

  const [menuAberto, setMenuAberto] = useState(false); // Para controlar a abertura do menu de opções

  const [busca, setBusca] = useState('') // Para Controlar o que o usuário digita no campo de busca

  // controle do modal e formulario de cadastro
  const [isModalAberto, setIsModalAberto] = useState(false)

  const [nomeInput, setNomeInput] = useState('')
  const [enderecoInput, setEnderecoInput] = useState('')
  const [capacidadeInput, setCapacidadeInput] = useState('')
  const [categorizacaoInput, setCategorizacaoInput] = useState('')
  const [cnpjInput, setCnpjInput] = useState('')
  const [contatoInput, setContatoInput] = useState('')


  // const menuRef = useRef(null); // Referência para o elemento do menu, para detectar cliques fora dele

  // useEffect(() => { // Fecha o menu quando clicar fora
  //   function lidarComCliqueFora(event) {
  //     if (menuAberto && menuRef.current && !menuRef.current.contains(event.target)) {
  //       setMenuAberto(false);
  //     }
  //   }

  //   document.addEventListener("mousedown", lidarComCliqueFora);
  // }, [menuAberto]);

  useEffect(() => {
    const token = sessionStorage.getItem('token')
    fetch('http://localhost:8000/api/instituicoes-api/', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    })
      .then(resposta => {
        if (!resposta.ok) {
          if (resposta.status === 401 || resposta.status === 403) {
            sessionStorage.removeItem('token')
            alert("Sua sessão expirou.")
            navigate('/')
          }
          throw new Error('Erro ao buscar dados')
        }
        return resposta.json()
      })
      .then(dados => setUnidade(dados))
      .catch(erro => console.error("Erro:", erro))
  }, [navigate])

  // Enviar o cadastro para o Banco (POST)
  const lidarComCadastro = (e) => {
    e.preventDefault() // Impede a página de dar F5 ao enviar o formulário

    const token = sessionStorage.getItem('token')

    // Montamos o pacotinho de dados igual ao que o Django espera receber
    const novaUnidade = {
      nome: nomeInput,
      endereco: enderecoInput,
      capacidade_total: capacidadeInput,
      categorizacao: categorizacaoInput,
      cnpj: cnpjInput,
      contato: contatoInput
    }

    fetch('http://localhost:8000/api/instituicoes-api/', {
      method: 'POST', // Mudamos o método para salvar
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(novaUnidade) // Transforma o objeto em texto JSON
    })
      .then(async resposta => {
        if (!resposta.ok) {
          // Pega o detalhe do erro que o Django enviou
          const erroDetalhado = await resposta.json()

          // Imprime no F12 para a gente ver o que é
          console.error("Motivo da recusa do Django:", erroDetalhado)

          // Transforma o erro em texto para o alerta da tela
          throw new Error(JSON.stringify(erroDetalhado))
        }
        return resposta.json() // O Django geralmente devolve o item salvo com o ID criado
      })
      .then(instituicaoSalva => {

        // ATUALIZAÇÃO EM TEMPO REAL:
        setUnidade([...unidade, instituicaoSalva])

        // Limpamos o formulário e fechamos a janela
        setNomeInput('')
        setEnderecoInput('')
        setIsModalAberto(false)
        alert('Instituição cadastrada com sucesso!')
      })
      .catch(erro => alert('Não foi possível cadastrar: ' + erro.message))
  }


  return (
    <div className="pr-8 pl-8 pt-5 bg-gray-100 min-h-screen">

      <h1 className="text-3xl font-bold text-blue-600 mb-2">
        Unidades de Acolhimento
      </h1>

      <div className="flex flex-col md:flex-row md:items-center gap-4 mb-2">

        <div className="relative w-full md:w-65">
          <input
            type="text"
            placeholder="Buscar Unidade"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 shadow-sm"
          />

          {/* Ícone de Lupa */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>

          {/* Botão X*/}
          {busca.length > 0 && (
            <button
              onClick={() => setBusca('')}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer p-1 rounded-full hover:bg-gray-100 transition-colors"
              title="Limpar busca"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        <button
          onClick={() => setIsModalAberto(true)}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-[12px]"
        >
          Adicionar Unidade
        </button>

        <div className='ml-auto pb-2'>
          <Count label="unidades" value={unidade.length} className='w-35' />
        </div>
      </div>

      {/* Listagem dos Cartões */}
      <div className="flex flex-col gap-2">
        {unidade.map((item) => (
          <div key={item.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex justify-between items-center">
            <div>

              <h3 className="text-lg font-semibold text-gray-800">Nome: {item.nome}</h3>
              <div className='flex gap-3'>

                <p className="text-sm text-gray-500">Endereço: {item.endereco}</p>
                <div className='w-px h-4 mt-1 bg-gray-400 '></div>
                <p className="text-sm text-gray-500">CNPJ: {item.cnpj}</p>
                <div className='w-px h-4 mt-1 bg-gray-400 '></div>
                <p className="text-sm text-gray-500">{item.ativo ? 'Ativo' : 'Inativo'}</p>

              </div>

            </div>
            <button
              onClick={() => setMenuAberto(!menuAberto)}
              className="p-2 text-gray-500 hover:text-blue-600 hover:bg-gray-100 rounded-full cursor-pointer"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
              </svg>
            </button>

            {/*Verificar*/}
            {menuAberto && (
              <div className="absolute mt-2 bg-white border border-gray-300 rounded shadow-md p-2 z-10 w-32">
                <button className="block w-full text-left px-2 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded">
                  Editar
                </button>
                <button className="block w-full text-left px-2 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded">
                  Inativar
                </button>
              </div>
            )}

          </div>
        ))}
      </div>

      {/* 4. O MODAL DE CADASTRO (Só aparece se isModalAberto for verdadeiro) */}
      {isModalAberto && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
          <div className="bg-white rounded-xl p-6 shadow-2xl w-full max-w-md mx-4 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Cadastrar Instituição</h2>

            <form onSubmit={lidarComCadastro} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Nome da Instituição</label>
                <input
                  type="text"
                  required
                  placeholder="Ex: Abrigo Nova Vida"
                  value={nomeInput}
                  onChange={(e) => setNomeInput(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Endereço / Referência</label>
                <input
                  type="text"
                  required
                  placeholder="Ex: Rua Flores, Nº 123"
                  value={enderecoInput}
                  onChange={(e) => setEnderecoInput(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Capacidade</label>
                <input
                  type="number"
                  required
                  placeholder="Ex: 50"
                  value={capacidadeInput}
                  onChange={(e) => setCapacidadeInput(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Categorização</label>
                <input
                  type="text"
                  required
                  placeholder="Ex: Idoso"
                  value={categorizacaoInput}
                  onChange={(e) => setCategorizacaoInput(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">CNPJ</label>
                <input
                  type="text"
                  required
                  placeholder="Ex: 00.000.000/0000-00"
                  value={cnpjInput}
                  onChange={(e) => setCnpjInput(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Contato</label>
                <input
                  type="text"
                  required
                  placeholder="Ex: (00)0 0000-0000"
                  value={contatoInput}
                  onChange={(e) => setContatoInput(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>


              {/* Botões de Ação do Formulário */}
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsModalAberto(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-semibold cursor-pointer"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow cursor-pointer"
                >
                  Salvar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  )
}

export default Unidade