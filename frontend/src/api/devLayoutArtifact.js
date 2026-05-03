import { request } from './httpClient'

export function getLayoutJsonArtifact(jobId) {
  return request(
    `/api/dev/generation-jobs/${encodeURIComponent(jobId)}/artifacts/layout-json`,
  )
}
