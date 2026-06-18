import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Trash2 } from 'lucide-react'

import Count from '../components/Count'
import Busca from '../components/Busca'

function Unidade() {

  // Guarda as informações em cache ---------------------------
  const [unidade, setUnidade] = useState([])
  const [contPagina, setContPagina] = useState(1)
  const [categorizacaoInput, setCategorizacaoInput] = useState('')
  const [listaCategoria, setListaCategoria] = useState([])

  // Sistema de Paginação --------------------------------------

  const [buscaAtual, setBuscaAtual] = useState('')
  // Estados para a paginação
  const [paginaAtual, setPaginaAtual] = useState(1)
  const [temProxima, setTemProxima] = useState(false)
  const [temAnterior, setTemAnterior] = useState(false)

  // Para mudança de rota (página)
  const navigate = useNavigate()

  // Controle de Estados ---------------------------------------

  // controle do modal 
  const [isModalAberto, setIsModalAberto] = useState(false)
  // Para controlar a abertura do menu de opções
  const [menuAberto, setMenuAberto] = useState(false);

  // Para cadastro e edição ------------------------------------

  // Formulario de cadastro -----

  // Nome
  const [nomeInput, setNomeInput] = useState('')

  // Endereço ----
  const [cepInput, setCepInput] = useState('')
  const [ruaInput, setRuaInput] = useState('')
  const [bairroInput, setBairroInput] = useState('')
  const [cidadeInput, setCidadeInput] = useState('')
  const [estadoInput, setEstadoInput] = useState('')
  const [numeroEnderecoInput, setNumeroEnderecoInput] = useState('')

  // Capacidade
  const [capacidadeInput, setCapacidadeInput] = useState('')

  // CNPJ
  const [cnpjInput, setCnpjInput] = useState('')

  // Contato
  const [contatoInput, setContatoInput] = useState([])
  const contatoTipo = ['Celular', 'Telefone', 'E-mail']
  const [contatosForm, setContatosForm] = useState([{ tipo: '', contato: '' }])

  const adicionarNovoContato = () => {
    setContatosForm([...contatosForm, { tipo: '', contato: '' }])
  }

  const removerContato = (indexParaRemover) => {
    const novaLista = contatosForm.filter((_, index) => index !== indexParaRemover)
    setContatosForm(novaLista)
  }

  const atualizarCampoContato = (index, campo, valor) => {
    // Cópia de segura da lista
    const novaLista = [...contatosForm]

    if (campo === 'contato') {
      // Passa o valor pela máscara antes de salvar!
      novaLista[index][campo] = aplicarMascara(novaLista[index].tipo, valor);
    } else if (campo === 'tipo') {
      // Se mudou o tipo, limpa o campo de texto automaticamente
      novaLista[index][campo] = valor;
      novaLista[index].contato = '';
    }

    setContatosForm(novaLista)
  }

  const aplicarMascara = (tipo, valor) => {
    // Se for e-mail, não mexe enquanto o usuário digita
    if (tipo === 'e-mail') return valor

    // Remove absolutamente tudo que não for número
    let numeros = valor.replace(/\D/g, '')

    if (tipo === 'celular') {
      // Limita a 11 dígitos
      if (numeros.length > 11) numeros = numeros.slice(0, 11)

      // Aplica a máscara: (99) 99999-9999
      numeros = numeros.replace(/^(\d{2})(\d)/g, '($1) $2')
      numeros = numeros.replace(/(\d{5})(\d)/, '$1-$2')
      return numeros;
    }

    if (tipo === 'telefone') {
      // Limita a 10 dígitos
      if (numeros.length > 9) numeros = numeros.slice(0, 10)

      // Aplica a máscara: (99)9999-9999
      numeros = numeros.replace(/^(\d{2})(\d)/g, '($1) $2')
      numeros = numeros.replace(/(\d{4})(\d)/, '$1-$2')
      return numeros;
    }

    return valor;
  };

  const mascaraCnpj = (e) => {
    let valor = e.target.value.replace(/\D/g, '')

    // Limita a 14 dígitos
    if (valor.length > 14) valor = valor.slice(0, 14)

    valor = valor.replace(/^(\d{2})(\d)/, "$1.$2")
    valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
    valor = valor.replace(/\.(\d{3})(\d)/, ".$1/$2")
    valor = valor.replace(/(\d{4})(\d)/, "$1-$2")

    setCnpjInput(valor)
  }

  const mascaraCep = (e) =>{
    let valor = e.target.value.replace(/\D/g, '')

    if (valor.length > 8) valor = valor.slice(0, 8)
    
    valor = valor.replace(/^(\d{5})(\d)/, "$1-$2")

    setCepInput(valor)
  }

  // Funções de pesquisa -----------------------------------------

  const realizarBusca = (termoPesquisar, pagina = 1) => {

<<<<<<< HEAD

  useEffect(() => {
=======
>>>>>>> ed0c52a86cdb91605d6db735e1219f10f6a43a7d
    const token = sessionStorage.getItem('token')

    setBuscaAtual(termoPesquisar)

    fetch(`http://localhost:8000/api/instituicoes-api/?search=${termoPesquisar}&page=${pagina}`, {
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
      .then(dados => {
        console.log(dados.results)
        setUnidade(dados.results)

        setTemProxima(dados.next !== null)
        setTemAnterior(dados.previous !== null)
        setPaginaAtual(pagina)

        // Quantidade de páginas totais
        const totalPagina = Math.ceil(dados.count / 10)
        setContPagina(totalPagina === 0 ? 1 : totalPagina)
      })
      .catch(erro => console.error("Erro:", erro))

  }

  useEffect(() => {
    realizarBusca('')
  }, [])

  // Função de enviar os dados para o banco (Cadastrar e Editar) -----------------------

  // Enviar o cadastro para o Banco (POST)
  const enviarCadastro = (e) => {
    e.preventDefault() // Impede a página de dar F5 ao enviar o formulário

    const token = sessionStorage.getItem('token')

    const cnpjPuro = cnpjInput.replace(/\D/g, '')

    const novaUnidade = {
      nome: nomeInput,
      capacidade_total: capacidadeInput,
      categorizacao: categorizacaoInput, // ID da categoria selecionada
      cnpj: cnpjPuro,

      // 1. Enviamos a nossa lista dinâmica de contatos
      contatos: contatosForm,

      // 2. Agrupamos o endereço (assumindo que o seu backend espera um objeto aninhado)
      endereco: {
        cep: cepInput,
        rua: ruaInput,
        numero: numeroEnderecoInput,
        bairro: bairroInput,
        cidade: cidadeInput,
        estado: estadoInput
      }
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
        setRuaInput('')
        setIsModalAberto(false)
        alert('Instituição cadastrada com sucesso!')
      })
      .catch(erro => alert('Não foi possível cadastrar: ' + erro.message))
  }


  useEffect(() => {
    const token = sessionStorage.getItem('token')

    // Ajuste a URL para a rota exata onde seu Django lista as categorias
    fetch('http://localhost:8000/api/categorias-api/', { 
        method: 'GET',
        headers: { 
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if (!res.ok) throw new Error('Falha ao carregar categorias')
        return res.json()
    })
    .then(dados => {
        // Se a sua API tem paginação, a lista real fica dentro de 'dados.results'. 
        // Se não tiver paginação, fica direto em 'dados'.
        const categoriasExtraidas = dados.results ? dados.results : dados
        
        // Salvamos a lista inteira no estado!
        setListaCategoria(categoriasExtraidas)
    })
    .catch(erro => console.error("Erro ao buscar categorias:", erro))
}, [])

  return (
    <div className="pr-8 pl-8 pt-5 bg-gray-50 min-h-screen">

      <h1 className="text-3xl font-bold text-blue-600 mb-2">
        Unidades de Acolhimento
      </h1>

      <div className="flex flex-col md:flex-row md:items-center gap-2 mb-2">
        <Busca
          placeholder="Buscar Unidade"
          apiEndpoint="http://localhost:8000/api/instituicoes-api/"
          onBuscar={(termo) => realizarBusca(termo, 1)}
        />

        <button
          onClick={() => setIsModalAberto(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-[14px]"
        >
          Adicionar Unidade
        </button>

        <div className='ml-auto pb-2'>
          <Count label="unidades" value={unidade.length} className='w-35' />
        </div>
      </div>

      <div className="flex items-center justify-between bg-gray-100 px-1 py-2 border-l border-r border-gray-200 sm:px-6 rounded-lg  ">

        <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p className="text-sm text-gray-700">
              Página <span className="font-medium">{paginaAtual}</span> de  <span className='font-medium'>{contPagina}</span>
            </p>
          </div>
          <div>
            <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
              <button
                onClick={() => realizarBusca(busca, paginaAtual - 1)}
                disabled={!temAnterior}
                className={`relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 bg-white ring-1 ring-inset ring-gray-300 ${!temAnterior ? 'cursor-not-allowed bg-gray-50' : 'cursor-pointer hover:bg-gray-50 focus:z-20'}`}
              >
                <span className="sr-only">Anterior</span>
                {/* Ícone de seta para a esquerda */}
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clipRule="evenodd" />
                </svg>
              </button>

              <button
                onClick={() => realizarBusca(buscaAtual, paginaAtual + 1)}
                disabled={!temProxima}
                className={`relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 bg-white ring-1 ring-inset ring-gray-300 ${!temProxima ? 'cursor-not-allowed bg-gray-50' : 'cursor-pointer hover:bg-gray-50 focus:z-20'}`}
              >
                <span className="sr-only">Próxima</span>
                {/* Ícone de seta para a direita */}
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>

      {/* Listagem dos Cartões */}
      <div className="flex flex-col gap-2 mt-2">
        {unidade.map((item) => (
          <div key={item.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex justify-between items-center">
            <div>

              <h3 className="text-lg font-semibold text-gray-800">{item.nome}</h3>
              <div className='flex gap-3'>

                <p className="text-sm text-gray-500">Endereço: {item.rua}</p>
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
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in ">

          <div className='w-full max-w-xl mx-2 bg-white rounded-xl shadow-2xl border border-gray-100 pr-px overflow-y-hidden'>

            <div className=" max-h-[90vh] overflow-y-auto p-6 pr-6">

              <h2 className="text-3xl font-bold text-blue-600 mb-4">Cadastrar Instituição</h2>
              <form onSubmit={enviarCadastro} className="space-y-4">

                <div className='flex gap-3 w-full mb-3'>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Nome da Instituição</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: Abrigo Nova Vida"
                      value={nomeInput}
                      onChange={(e) => setNomeInput(e.target.value)}
                      className="min-w-sm px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
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

                </div>

                <div className='flex gap-3 w-full mb-3'>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">CNPJ</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: 00.000.000/0000-00"
                      value={cnpjInput}
                      onChange={mascaraCnpj}
                      className="w-xs px-3 py-2 h-11 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Categoria</label>
                    <select
                      className='border border-gray-300 rounded-lg h-11 w-full pr-2 py-2 text-gray-500 text-sm 
                      focus:outline-none focus:border-blue-500 '
                      value={categorizacaoInput}
                      onChange={(e) => setCategorizacaoInput(e.target.value)}
                      required
                    >
                      <option value="" disabled>Selecione uma categoria...</option>

                      {listaCategoria.map((cat) => (
                        <option key={cat.id} value={cat.id}>
                          {cat.nome}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>


                <div className='flex items-center gap-4 w-full'>

                  <span className="whitespace-nowrap text-lg font-bold text-gray-700">
                    Endereço Completo
                  </span>
                  <div className='flex-1 border-b border-gray-400'></div>

                </div>
                <div className='grid grid-cols-2 gap-2'>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">CEP</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: 00000-000"
                      value={cepInput}
                      onChange={mascaraCep}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Cidade</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: Serra Talhada"
                      value={cidadeInput}
                      onChange={(e) => setCidadeInput(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Bairro</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: Centro"
                      value={bairroInput}
                      onChange={(e) => setBairroInput(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div className='grid grid-cols-2 gap-2'>
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-1">Número</label>
                      <input
                        type="text"
                        required
                        placeholder="Ex: 123A"
                        value={numeroEnderecoInput}
                        onChange={(e) => setNumeroEnderecoInput(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                      />
                    </div>
                    <div>

                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Logradouro</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: Avenida Bezerra"
                      value={ruaInput}
                      onChange={(e) => setRuaInput(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div className='grid grid-cols-2 gap-2'>
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-1">Estado</label>
                      <input
                        type="text"
                        required
                        placeholder="Ex: PE"
                        value={estadoInput}
                        onChange={(e) => setEstadoInput(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                      />
                    </div>
                    <div></div>
                  </div>
                </div>

                <div className='flex items-center gap-4 w-full'>

                  <span className="whitespace-nowrap text-lg font-bold text-gray-700">
                    Contatos
                  </span>
                  <div className='flex-1 border-b border-gray-400'></div>

                </div>

                <div className='flex w-full items-center gap-3'>
                  <div>
                    {contatosForm.map((item, index) => (
                      <div key={index} className="flex items-end gap-3 mb-4">

                        {/* Campo: TIPO */}
                        <div className="w-1/3">
                          <label className="block text-sm font-semibold text-gray-700 mb-1">Tipo</label>
                          <select
                            className="border border-gray-300 rounded-lg h-11 w-full px-3 py-2 text-gray-700 text-sm outline-none focus:border-blue-500 capitalize"
                            value={item.tipo}
                            onChange={(e) => atualizarCampoContato(index, 'tipo', e.target.value)}
                            required
                          >
                            <option value="" disabled className="normal-case">Selecione...</option>
                            {contatoTipo.map((tipo) => (
                              <option key={tipo} value={tipo} className="capitalize">{tipo}</option>
                            ))}
                          </select>
                        </div>

                        {/* Campo: O NÚMERO OU EMAIL (O VALOR) */}
                        <div className="flex-1">
                          <label className="block text-sm font-semibold text-gray-700 mb-1">Contato</label>
                          <input
                            type={item.tipo === 'e-mail' ? 'email' : 'tel'}

                            // O pattern verifica: texto + @ + texto + .com (aceitando .com.br também por precaução)
                            pattern={item.tipo === 'e-mail' ? "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.com(\\.br)?$" : undefined}

                            // A mensagem de erro vermelha que o navegador mostra se o pattern falhar
                            title={item.tipo === 'e-mail' ? "O e-mail deve ser válido e terminar com .com ou .com.br" : "Preencha corretamente"}

                            placeholder={item.tipo === 'e-mail' ? "exemplo@email.com" : "Digite o número..."}
                            className="border border-gray-300 rounded-lg h-11 w-full px-3 py-2 text-gray-700 text-sm outline-none focus:border-blue-500"

                            value={item.contato}
                            onChange={(e) => atualizarCampoContato(index, 'contato', e.target.value)}
                            required
                          />
                        </div>

                        {/* Botão de Excluir (Só aparece se tiver mais de 1 contato na lista) */}
                        {contatosForm.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removerContato(index)}
                            className="h-11 px-3 text-red-500 hover:bg-red-50 rounded-lg transition-colors flex items-center justify-center cursor-pointer"
                            title="Remover contato"
                          >
                            <Trash2 size={20} />
                          </button>
                        )}
                      </div>
                    ))}

                    {/* O Botão Mágico de Adicionar Linha */}
                    <button
                      type="button"
                      onClick={adicionarNovoContato}
                      className="mt-2 flex items-center gap-2 text-sm font-semibold text-blue-600 hover:text-blue-800 transition-colors cursor-pointer"
                    >
                      <Plus size={16} />
                      Adicionar mais um contato
                    </button>

                  </div>
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

        </div>
      )}

    </div>
  )
}

export default Unidade