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
