import { request } from './httpClient'

export function createImageLayoutJob(payload) {
  return request('/api/dev/image-layout-jobs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
}

export function createImagePageJob(payload) {
  return request('/api/dev/image-page-jobs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
}

export function uploadImagePageSource(file) {
  const formData = new FormData()
  formData.append('file', file)

  return request('/api/image-page/upload', {
    method: 'POST',
    body: formData,
  })
}

export function generateImagePage(jobId) {
  return request(`/api/image-page/jobs/${encodeURIComponent(jobId)}/generate`, {
    method: 'POST',
  })
}
