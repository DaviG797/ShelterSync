import { Link, Outlet, Navigate } from 'react-router-dom'

import AutoLogout from './AutoLogout'

function Layout() {

    const token = sessionStorage.getItem("token") // Verifica se o token existe no sessionStorage

    // Se o token não existir, redireciona para a página de login
    if (!token) { 
        return <Navigate to="/" replace />
    } 

    return (
        <div className="min-h-screen bg-gray-200">
            
            <div className="max-w-6xl mx-auto bg-gray-50 min-h-screen shadow-2xl flex flex-col">

                <nav className="bg-blue-800 pl-10 pr-10 py-1 text-white flex justify-between items-center shadow-md">
                    <div className="flex gap-4 items-center">
                        <span className="font-bold text-xl mr-4">ShelterSync</span>
                        <div className="w-px h-6 bg-gray-400"></div> {/* Linha Vertical */}
                        <div className="flex gap-2">
                            <Link to="/unidades" className="hover:text-blue-100 font-semibold transition-colors">Unidades</Link>
                        <div className="w-1 h-px mt-3.5 bg-gray-400"></div> {/* Linha Vertical */}
                        <Link to="/acolhidos" className="hover:text-blue-100 font-semibold transition-colors">Acolhidos</Link>
                        </div>
                        
                    </div>

                    <div>
                        <AutoLogout />
                    </div>
                </nav>

                <main className=" grow">
                    <Outlet />
                </main>

            </div>
        </div>
    )
}

export default Layout