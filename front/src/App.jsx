import { useState, useEffect } from 'react'

function App() {
  // 1. Criamos a nossa "caixa" vazia (um array []) para guardar as instituições
  const [instituicoes, setInstituicoes] = useState([])

  // 2. Usamos o useEffect para buscar os dados quando a tela carregar
  useEffect(() => {

    // A função fetch() é quem faz a "ligação" para a nossa API
    fetch('http://localhost:8000/api/instituicoes-api/')
      .then(resposta => resposta.json()) // Transforma a resposta em JSON
      .then(dados => {
        console.log("Dados que chegaram do Django:", dados)
        setInstituicoes(dados) // Guarda os dados na nossa "caixa"
      })
      .catch(erro => console.error("Ops, deu erro:", erro))
  }, []) // Os colchetes vazios significam "rode isso apenas uma vez"

  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">
        Nossas Instituições
      </h1>
      
      <ul className="space-y-4 flex flex-col ">
        {instituicoes.map(instituicao => (
          <li key={instituicao.id} className="bg-white p-2 rounded shadow mb-1">
            <h3 className="text-xl font-semibold text-gray-800">
              {instituicao.nome}
            </h3>
            <p className="text-gray-600">{instituicao.endereco}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
