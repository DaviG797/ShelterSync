import { useState, useEffect } from 'react'

function Instituicoes() {
  // Cria uma caixa vazia para guardar as instituições
  const [instituicoes, setInstituicoes] = useState([])

  useEffect(() => {

    // A função fetch() é quem faz a "ligação" para a nossa API
    fetch('http://localhost:8000/api/instituicoes-api/')
      .then(resposta => resposta.json()) 
      .then(dados => {
        setInstituicoes(dados)
      })
      .catch(erro => console.error("Ops, deu erro:", erro))
  }, []) // Os colchetes vazios significam "rode isso apenas uma vez"

  return (
    <div className="pr-8 pl-8 pt-5 bg-gray-100 min-h-screen">

      <h1 className="text-3xl font-bold text-blue-600 mb-2">
        Nossas Instituições
      </h1>

      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-3 text-sm">
        Adicionar Instituição
      </button>

      <ul className="space-y-4 flex flex-col ">
        {instituicoes.map(instituicao => (
          <li key={instituicao.id} className="bg-white rounded shadow">

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
                className="pb-1 text-gray-500 hover:text-blue-600 hover:bg-gray-100 rounded-full transition-colors cursor-pointer"
                title="Opções"
              >
                {/* Ícone de 3 Pontos Verticais (Kebab) */}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                </svg>
              </button>

            </div>


          </li>

        ))}
      </ul>

    </div>
  )
}

export default Instituicoes