const qs = require("qs");
import { omit } from "lodash";

export function getTextFromValues(values, value) {
  const result = values.find(v => v.value === value);
  if (!result) {
    return "N/A";
  }
  return result.text;
}

export function buildQueryString(filters) {
  let queryString = "";
  filters.map(f => {
    let temp = omit(f, "uid");
    queryString === ""
      ? (queryString += qs.stringify(temp))
      : (queryString += "&" + qs.stringify(temp));
  });
  return queryString;
}
