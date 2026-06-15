import { useState, useEffect } from 'react'
import {useNavigate} from 'react-router-dom'

function Unidade() {

  const navigate = useNavigate() // Para mudança de rota (página)
  
  const [unidade, setUnidade] = useState([]) // Cria uma caixa vazia para guardar as instituições

  const [menuAberto, setMenuAberto] = useState(false); // Para controlar a abertura do menu de opções

  const [busca, setBusca] = useState('') // Para Controlar o que o usuário digita no campo de busca


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
      .then(resposta =>{

        if (!resposta.ok){
          if (resposta.status == 401 || resposta.status ==403){
            sessionStorage.removeItem('token')
            alert("Sua sessão expirou. Faça login novamente.")
            navigate('/login')
          }
          throw new Error('Erro ao buscar instituições!')
        }

        return resposta.json()

      })
      .then(dadosDoBanco => {
        
        setUnidade(dadosDoBanco) // Pega os dados reais do banco e colocamos na lista

      })

      .catch(erro => console.error("Erro ao buscar instituições:", erro))

  }, [navigate])

  // Cria uma nova lista, filtrando a original, para mostrar apenas as instituições que correspondem à busca
  const listaFiltrada = unidade.filter((instituicao) => {

    return instituicao.nome.toLowerCase().includes(busca.toLowerCase())

  })

  return (
    <div className="pr-8 pl-8 pt-5 bg-gray-100 min-h-screen">

      <h1 className="text-3xl font-bold text-blue-600 mb-6">
        Unidades de Acolhimento
      </h1>

      <div className="flex flex-col md:flex-row md:items-center gap-4 mb-6">

        <div className="relative w-full md:w-60">

          <input
            type="text"
            placeholder="Buscar instituição"
            value={busca}
            // A cada letra digitada, atualizamos o estado
            onChange={(e) => setBusca(e.target.value)}
            className="w-full pl-10 pr-2 py-2 border bg-white border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-sm text-sm"
          />
          
          {/* Ícone de Lupa dentro do input */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>

        </div>

        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-[12px]">
          Adicionar Instituição
        </button>

      </div>

      <ul className="space-y-4 flex flex-col ">
        {unidade.map(instituicao => (
          <li key={instituicao.id} className="bg-white rounded shadow pl-4">

            <h3 className="text-[16px] font-semibold text-gray-800">
              {instituicao.nome}
            </h3>

            <div className="flex gap-4 mt-1">

              <p className="text-gray-600">Endereço: {instituicao.endereco}</p>
              <div className="w-px h-4 mt-1 bg-gray-400"></div> {/* Linha Vertical */}

              <p className="text-gray-600">Contato: {instituicao.contato}</p>
              <div className="w-px h-4 mt-1 bg-gray-400"></div> {/* Linha Vertical */}

              <p className="text-gray-600">Capacidade: {instituicao.capacidade_total}</p>
              <div className="w-px h-4 mt-1 bg-gray-400"></div> {/* Linha Vertical */}

              <p className="text-gray-600">categoria: {instituicao.categorizacao}</p>
              <div className="w-px h-4 mt-1 bg-gray-400"></div> {/* Linha Vertical */}

              <p className="text-gray-600">{instituicao.ativo ? 'Ativo' : 'Inativo'}</p>
              <button
                onClick = {() => setMenuAberto(!menuAberto)}
                className="pb-1 text-gray-500 hover:text-blue-600 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                title="Opções"
              >
                {/* Ícone de 3 Pontos Verticais (Kebab) */}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                </svg>
              </button>

              {menuAberto &&(
                <div className="absolute mt-2 bg-white border border-gray-300 rounded shadow-md p-2 z-10 w-32">
                  <button className="block w-full text-left px-2 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded">
                    Editar 
                  </button>
                  <button className="block w-full text-left px-2 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded">
                    Inativar
                  </button>
                </div>
              )
              }
            </div>

          </li>

        ))}

      </ul>

    </div>
  )
}

export default Unidade