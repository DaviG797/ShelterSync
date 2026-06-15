import { useEffect, useState } from 'react'

function Count({ label = '', endpoint = null, value = null, refreshInterval = 0, onClick = null, className = '' }) {

  const [count, setCount] = useState(value ?? null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true

    async function getCount() {
      if (!endpoint) return
      setLoading(true)
      setError(null)

      try {
        const token = sessionStorage.getItem('token')
        const res = await fetch(endpoint, {
          headers: token ? { 'Authorization': `Token ${token}` } : {}
        })

        if (!res.ok) throw new Error('Erro ao buscar contador')

        const data = await res.json()

        let parsed = null
        if (typeof data === 'number') parsed = data
        else if (data === null) parsed = 0
        else if (Array.isArray(data)) parsed = data.length
        else if (typeof data === 'object') {
          parsed = data.count ?? data.total ?? data.length ?? null
        }

        if (mounted && parsed !== null) setCount(parsed)

      } catch (err) {
        if (mounted) setError(err.message)
      } finally {
        if (mounted) setLoading(false)
      }
    }

    // If a direct `value` prop is provided, prefer it and skip fetching
    if (value !== null) {
      setCount(value)
      return
    }

    // initial fetch
    getCount()

    // optional polling
    let timer = null
    if (refreshInterval > 0) {
      timer = setInterval(getCount, refreshInterval)
    }

    return () => {
      mounted = false
      if (timer) clearInterval(timer)
    }
  }, [endpoint, refreshInterval, value])

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded shadow p-4 flex items-center justify-between cursor-default ${className}`}
    >
      <div>
        <div className="text-sm text-gray-500">{label}</div>
        <div className="text-2xl font-bold text-blue-600">
          {loading ? '...' : error ? '-' : (count ?? '-')}
        </div>
      </div>
      <div className="text-gray-300 text-4xl">📊</div>
    </div>
  )
}

export default Count
