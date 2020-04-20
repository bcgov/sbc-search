import ApiService from "./ApiService.js";

export const API_PREFIX = "/api/v1";
export const DIRECTOR_SEARCH_PREFIX = `${API_PREFIX}/directors`;
export const CORPORATION_SEARCH_PREFIX = `${API_PREFIX}/businesses`;
export const EXPORT_CORPPARTY_URL = `${DIRECTOR_SEARCH_PREFIX}/export`;
export const EXPORT_CORPORATION_URL = `${CORPORATION_SEARCH_PREFIX}export`;

export function corpPartySearch(query) {
  return ApiService.get(`${DIRECTOR_SEARCH_PREFIX}/?${query}`);
}

export function corpPartySearchDetail(id) {
  return ApiService.get(`${DIRECTOR_SEARCH_PREFIX}/${id}`);
}

export function corpPartyOfficeSearch(id) {
  return ApiService.get(`${DIRECTOR_SEARCH_PREFIX}/${id}/offices`);
}

export function corporationDetailSearch(id) {
  return ApiService.get(`${CORPORATION_SEARCH_PREFIX}/${id}`);
}

export function corporationSearch(params) {
  return ApiService.get(`${CORPORATION_SEARCH_PREFIX}/`, {
    params
  });
}

export function exportCorpPartySearch(queryString) {
  return ApiService({
    url: `${EXPORT_CORPPARTY_URL}/?${queryString}`,
    method: "GET",
    responseType: "blob",
    headers: { Accept: "application/vnd.ms-excel" }
  });
}

export function exportCorporationSearch(queryString) {
  return ApiService({
    url: `${EXPORT_CORPORATION_URL}/?${queryString}`,
    method: "GET",
    responseType: "blob",
    headers: { Accept: "application/vnd.ms-excel" }
  });
}

export function warmUp() {
  return ApiService.get(`/api/v1/auth-check/`);
}
