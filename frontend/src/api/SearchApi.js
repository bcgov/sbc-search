import ApiService from "./ApiService.js";

const PERSON_SEARCH_URL = "/person/search";
const COPRPARTY_SEARCH_URL = "/person";
const CORPPARTY_OFFICE_URL = "/person/officesheld";
const CORPORATION_SEARCH_URL = "/corporation";

export function searchApi(query) {
  return ApiService.get(`${PERSON_SEARCH_URL}/?${query}`);
}

export function corpPartySearch(id) {
  return ApiService.get(`${COPRPARTY_SEARCH_URL}/${id}`);
}

export function corpPartyOfficeSearch(id) {
  return ApiService.get(`${CORPPARTY_OFFICE_URL}/${id}`);
}

export function corporationSearch(id) {
  return ApiService.get(`${CORPORATION_SEARCH_URL}/${id}`);
}
