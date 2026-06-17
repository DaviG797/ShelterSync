import { useState, useRef } from 'react'

export default function Busca({ onBuscar, apiEndpoint, placeholder = "Buscar..." }) {

    // Para Controlar o que o usuário digita no campo de busca
    const [busca, setBusca] = useState('')

    // Caixa de Sugestões de busca
    const [sugestoes, setSugestoes] = useState([])
    const [mostrarSugestoes, setMostrarSugestoes] = useState(false)

    // Usamos useRef para guardar o cronômetro do Debounce sem causar re-renderizações
    const debounceTimer = useRef(null)

    const autoComplete = (e) => {
        const valor = e.target.value
        setBusca(valor)

        if (valor.trim().length < 2) {
            setSugestoes([])
            setMostrarSugestoes(false)
            return
        }

        if (debounceTimer.current) clearTimeout(debounceTimer.current)

        debounceTimer.current = setTimeout(() => {
            const token = sessionStorage.getItem('token')

            // Usamos a variável apiEndpoint que veio do Pai!
            fetch(`${apiEndpoint}?search=${valor}`, {
                headers: { 'Authorization': `Token ${token}` }
            })
                .then(res => res.json())
                .then(dados => {
                    const sugestoesUnicas = dados.results.filter((item, index, arrayCompleto) =>
                        index === arrayCompleto.findIndex((t) => t.nome.toLowerCase() === item.nome.toLowerCase())
                    )
                    setSugestoes(sugestoesUnicas)
                    setMostrarSugestoes(true)
                })
                .catch(erro => console.error("Erro nas sugestões:", erro))
        }, 300)
    }

    const lidarComEnvioBusca = (e) => {
        e.preventDefault()
        setMostrarSugestoes(false)

        onBuscar(busca)
    }

    const selecionarSugestao = (nome) => {
        setBusca(nome)
        setMostrarSugestoes(false)

        onBuscar(nome)
    }

    const limparBusca = () => {
        setBusca('')
        setSugestoes([])
        setMostrarSugestoes(false)

        if(debounceTimer.current) clearTimeout(debounceTimer.current)

        onBuscar('')
    }

    return (
        <form onSubmit={lidarComEnvioBusca} className="relative flex items-center w-full md:w-auto rounded-lg border border-gray-300 ">
            <div className="relative w-full md:w-65 ">
                <input
                    type="text"
                    placeholder={placeholder}
                    value={busca}
                    onChange={autoComplete}
                    onBlur={() => setTimeout(() => setMostrarSugestoes(false), 200)}
                    onFocus={() => sugestoes.length > 0 && setMostrarSugestoes(true)}
                    className="w-full pl-10 pr-10 py-2   focus:outline-none focus:ring-2 focus:ring-blue-300 focus:rounded-l-lg"
                />

                {/* Ícone Lupa */}
                <svg xmlns="http://www.w3.org/2000/svg" className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>

                {/* Botão X*/}
                {busca.length > 0 && (
                    <button
                        onClick={() => limparBusca()}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer p-1 rounded-full hover:bg-gray-100 transition-colors"
                        title="Limpar busca"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                )}
                {mostrarSugestoes && sugestoes.length > 0 && (
                    <ul className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                        {sugestoes.map((item) => (
                            <li
                                key={item.id}
                                onMouseDown={() => selecionarSugestao(item.nome)}
                                className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-2 text-gray-700"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                                {item.nome}
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-[15px] py-2 px-2 transition-colors rounded-r-lg border border-gray-300">
                Buscar
            </button>
        </form>

    )
}


