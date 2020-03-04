import ApiService from "./ApiService.js";

const PERSON_SEARCH_URL = "/person/search";
const COPRPARTY_SEARCH_URL = "/person";
const CORPPARTY_OFFICE_URL = "/person/officesheld";
const CORPORATION_SEARCH_URL = "/corporation/search/";
const CORPORATION_DETAIL_SEARCH_URL = "/corporation";

export function corpPartySearch(query) {
  return ApiService.get(`${PERSON_SEARCH_URL}/?${query}`);
}

export function corpPartySearchDetail(id) {
  return ApiService.get(`${COPRPARTY_SEARCH_URL}/${id}`);
}

export function corpPartyOfficeSearch(id) {
  return ApiService.get(`${CORPPARTY_OFFICE_URL}/${id}`);
}

export function corporationDetailSearch(id) {
  return ApiService.get(`${CORPORATION_DETAIL_SEARCH_URL}/${id}`);
}

export function corporationSearch(params) {
  return ApiService.get(`${CORPORATION_SEARCH_URL}`, {
    params
  });
}
