import { request } from './httpClient'

export function uploadAsset(file) {
  const formData = new FormData()
  formData.append('file', file)

  return request('/api/assets/upload', {
    method: 'POST',
    body: formData,
  })
}
