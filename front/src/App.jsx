import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

import Instituicoes from './pages/Unidade'
import Login from './pages/Login'
import Layout from './components/Layout'

function Acolhidos() {
  return <h1 className="p-8 text-2xl font-bold">Página de Acolhidos (Em breve) 🫂</h1>
}

function App() {
  return (
    <BrowserRouter>

      {/* O "Mapa" de Rotas */}
      <Routes>
        <Route path="/" element={<Login />} />

        <Route element={<Layout />}>
          <Route path="/unidades" element={<Instituicoes />} />
          <Route path="/acolhidos" element={<Acolhidos />} />
        </Route>
      </Routes>
    </BrowserRouter>

  )
}

export default App