const qs = require("qs");
import omit from "lodash-es/omit";
import ApiService from "@/api/ApiService.js";
const fileDownload = require("js-file-download");
import dayjs from "dayjs";

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

export function getDeepLink(corpNum) {
  return `https://tst.corponline.gov.bc.ca/corporateonline/colin/search/searchAction.do?corpNum=${corpNum}&_flowExecutionKey=e4s2`;
}

export async function downloadFile(url, fileName) {
  const response = await ApiService({
    url: url,
    method: "GET",
    responseType: "blob",
    headers: { Accept: "application/vnd.ms-excel" }
  });
  fileDownload(
    response.data,
    fileName || "DS-Results.xlsx",
    "application/vnd.ms-excel"
  );
}

export function formatDate(d) {
  return d ? dayjs(d).format("YYYY-MM-DD") : "-";
}
