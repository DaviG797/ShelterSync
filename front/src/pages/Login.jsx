import { useState } from 'react'
import { useNavigate } from 'react-router-dom' // Importa o hook useNavigate do controlador de rotas

import iconOlhoFechado from '../assets/olho_fechado.svg'
import iconOlhoAberto from '../assets/olho_aberto.svg'
import iconLogo from '../assets/ShelterSync_.png'

function Login() {
  const [usuario, setUsuario] = useState('')
  const [senha, setSenha] = useState('')

  // Estado de controle para a senha
  const [mostrarSenha, setMostrarSenha] = useState(false)

  // Inicializa o "guia" de navegação
  const navigate = useNavigate()

  const handleLogin = (e) => {
    e.preventDefault()

    const credenciais = {
      username: usuario,
      password: senha
    }

    // Faz a requisição para a API de login do Django
    fetch('http://localhost:8000/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credenciais),
    })
      .then(resposta => {
        if (!resposta.ok) {
          throw new Error('Usuário ou senha incorretos!')
        }
        return resposta.json()
      })
      .then(dados => {
        sessionStorage.setItem('token', dados.token)

        navigate('/unidades') 
      })
      .catch(erro => {

        alert("Falha no login. Verifique se digitou tudo corretamente.")
      })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-200">

      <div className="bg-white p-8 rounded-xl shadow-lg w-102">

        <div className="relative flex items-center gap-1 mb-8">
          <img src={iconLogo} alt="Logo do ShelterSync" className="w-14 " />
          <h2 className="text-4xl font-bold text-center text-blue-600">
            ShelterSync
          </h2>
        </div>

        <form onSubmit={handleLogin} className="flex flex-col gap-5">
          <div>
            <label className="block text-gray-700 font-semibold text-lg mb-1">Usuário</label>
            <input
              type="text"
              className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-blue-500"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              placeholder="Digite seu usuário"
              required
            />
          </div>

          <div>
            <label className="block text-gray-700 font-semibold text-lg mb-1">Senha</label>
            <div className="relative">
              <input
                type={mostrarSenha ? "text" : "password"}
                className="w-full border border-gray-300 p-2 pr-10 rounded focus:outline-none focus:border-blue-500"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                placeholder="Digite sua senha"
                required
              />
              <img
                src={mostrarSenha ? iconOlhoAberto : iconOlhoFechado}
                alt={mostrarSenha ? "Ocultar senha" : "Mostrar senha"}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xl text-gray-500 hover:text-gray-700 w-5 cursor-pointer"
                onClick={() => setMostrarSenha(!mostrarSenha)}
              />
            </div>


          </div>

          <div className="flex justify-center mt-2">
            <button
              type="submit"
              className="w-40 bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition"
            >
              Entrar
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login