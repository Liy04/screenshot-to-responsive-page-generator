import { request } from './httpClient'

export function createGeneration(payload) {
  return request('/api/generations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
}

export function getGeneration(jobId) {
  return request(`/api/generations/${jobId}`)
}

export function getGenerationResult(jobId) {
  return request(`/api/generations/${jobId}/result`)
}
