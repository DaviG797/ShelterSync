import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

function AutoLogout() {

    const [tempoRestante, setTempoRestante] = useState(900)
    const navigate = useNavigate()
    const location = useLocation()

    useEffect(() => {
        // Se estiver no login, não faz nada
        if (location.pathname === '/') return

        const intervalo = setInterval(() => {
            setTempoRestante((tempoAtual) => {
                if (tempoAtual <= 1) {
                    clearInterval(intervalo) // Para o relógio
                    sessionStorage.removeItem('token')
                    navigate('/') // Expulsa para o login
                    return 0
                }
                return tempoAtual - 1
            })
        }, 1000) // Roda a cada 1000 milissegundos (1 segundo)

        return () => clearInterval(intervalo)
    }, [navigate, location.pathname])

    // Percebe o movimento e reseta o relógio
    useEffect(() => {
        if (location.pathname === '/') return

        const resetarRelogio = () => {
            setTempoRestante(900)
        }

        const eventos = ['mousedown', 'click', 'scroll', 'keypress']
        eventos.forEach(evento => window.addEventListener(evento, resetarRelogio))

        return () => {
            eventos.forEach(evento => window.removeEventListener(evento, resetarRelogio))
        }
    }, [location.pathname])

    // Se estiver na tela de login, desenha NADA
    if (location.pathname === '/') return null

    // 1. Pegamos o total de minutos arredondado para cima
    const totalMinutos = Math.ceil(tempoRestante / 60)

    // 2. Calculamos quantas horas inteiras cabem nesse tempo
    const horasFormatadas = String(Math.floor(totalMinutos / 60)).padStart(2, '0')

    // 3. Pegamos apenas os minutos que sobram (o resto da divisão por 60)
    const minutosFormatados = String(totalMinutos % 60).padStart(2, '0')

    // O desenho do contador na tela (inspirado na sua imagem)
    return (

        <div className=" text-white flex items-center gap-4 text-sm">

            <span className="font-sans italic ">
                Tempo de Sessão: {horasFormatadas}:{minutosFormatados}
            </span>

            <button
                onClick={() => {
                    sessionStorage.removeItem('token')
                    navigate('/')
                }}
                className="font-bold text-white hover:text-blue-100 transition-colors cursor-pointer"
            >
                SAIR
            </button>
        </div>
    )
}

export default AutoLogout