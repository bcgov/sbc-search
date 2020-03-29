import ApiService from "./ApiService.js";

export const API_PREFIX = "/api/v1";
export const DIRECTOR_SEARCH_PREFIX = `${API_PREFIX}/directors`;
export const PERSON_SEARCH_URL = `${DIRECTOR_SEARCH_PREFIX}/search`;
export const CORPPARTY_OFFICE_URL = `${DIRECTOR_SEARCH_PREFIX}/officesheld`;
export const CORPORATION_SEARCH_PREFIX = `${API_PREFIX}/businesses`;
export const CORPORATION_SEARCH_URL = `${CORPORATION_SEARCH_PREFIX}/search/`;
export const EXPORT_CORPPARTY_URL = `${PERSON_SEARCH_URL}/export`;
export const EXPORT_CORPORATION_URL = `${CORPORATION_SEARCH_URL}export`;

export function corpPartySearch(query) {
  return ApiService.get(`${PERSON_SEARCH_URL}/?${query}`);
}

export function corpPartySearchDetail(id) {
  return ApiService.get(`${DIRECTOR_SEARCH_PREFIX}/${id}`);
}

export function corpPartyOfficeSearch(id) {
  return ApiService.get(`${CORPPARTY_OFFICE_URL}/${id}`);
}

export function corporationDetailSearch(id) {
  return ApiService.get(`${CORPORATION_SEARCH_PREFIX}/${id}`);
}

export function corporationSearch(params) {
  return ApiService.get(`${CORPORATION_SEARCH_URL}`, {
    params
  });
}
