import axios from '../util/axios-auth'

export const API_PREFIX = '/api/v1'
export const DIRECTOR_SEARCH_PREFIX = `${API_PREFIX}/directors`
export const CORPORATION_SEARCH_PREFIX = `${API_PREFIX}/businesses`
export const EXPORT_CORPPARTY_URL = `${DIRECTOR_SEARCH_PREFIX}/export`
export const EXPORT_CORPORATION_URL = `${CORPORATION_SEARCH_PREFIX}export`

export function corpPartySearch (query, opts) {
  return axios.get(`${DIRECTOR_SEARCH_PREFIX}/?${query}`, opts)
}

export function corpPartySearchDetail (id) {
  return axios.get(`${DIRECTOR_SEARCH_PREFIX}/${id}`)
}

export function corpPartyOfficeSearch (id) {
  return axios.get(`${DIRECTOR_SEARCH_PREFIX}/${id}/offices`)
}

export function corporationDetailSearch (id) {
  return axios.get(`${CORPORATION_SEARCH_PREFIX}/${id}`)
}

export function corporationSearch (params, cancelToken) {
  return axios.get(`${CORPORATION_SEARCH_PREFIX}/`, {
    cancelToken,
    params
  })
}

export function exportCorpPartySearch (queryString) {
  return axios({
    url: `${EXPORT_CORPPARTY_URL}/?${queryString}`,
    method: 'GET',
    responseType: 'blob',
    headers: { Accept: 'application/vnd.ms-excel' }
  })
}

export function exportCorporationSearch (queryString) {
  return axios({
    url: `${EXPORT_CORPORATION_URL}/?${queryString}`,
    method: 'GET',
    responseType: 'blob',
    headers: { Accept: 'application/vnd.ms-excel' }
  })
}

export function warmUp () {
  return axios.get(`/api/v1/auth-check/`)
}
