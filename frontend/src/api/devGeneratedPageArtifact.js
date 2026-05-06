import { request } from './httpClient'

export function getGeneratedPageArtifact(jobId) {
  return request(
    `/api/dev/generation-jobs/${encodeURIComponent(jobId)}/artifacts/generated-page`,
  )
}
