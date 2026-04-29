const JSON_CONTENT_TYPE = 'application/json'

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || ''
  if (!contentType.includes(JSON_CONTENT_TYPE)) {
    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`)
    }
    return null
  }

  const body = await response.json()
  if (!response.ok || body.code !== 200) {
    throw new Error(body.message || `请求失败：${response.status}`)
  }

  return body.data
}

export async function request(path, options = {}) {
  const response = await fetch(path, options)
  return parseResponse(response)
}
