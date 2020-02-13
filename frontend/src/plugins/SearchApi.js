import ApiService from "@/plugins/ApiService.js";

const PERSON_SEARCH_URL = "/person/search";

export function searchApi(params) {
  return ApiService.get(PERSON_SEARCH_URL, {
    params: params
  });
}

export function advancedSearchApi(query) {
  return ApiService.get(`${PERSON_SEARCH_URL}/?${query}`);
}

export function searchApiV2(params, { type }) {
  console.log("Type", type);
  if (type === "basic") {
    return searchApi(params);
  } else if (type === "advanced") {
    return advancedSearchApi(params);
  }
}
