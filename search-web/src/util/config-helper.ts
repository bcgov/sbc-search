/* eslint-disable no-console */
import Axios from "axios";

/**
 * Fetches config from environment and API.
 * Also identifies Business ID from initial route.
 * @returns A promise to get & set session storage keys with appropriate values.
 */
export async function fetchConfig(): Promise<any> {
  // get config from environment
  const origin: string = window.location.origin;
  const processEnvVueAppPath: string = process.env.VUE_APP_PATH;

  if (!origin || !processEnvVueAppPath) {
    return Promise.reject(new Error("Missing environment variables"));
  }

  // fetch config from API
  // eg, http://localhost:8080/basePath/config/configuration.json
  // eg, https://business-create-dev.pathfinder.gov.bc.ca/businesses/edit/config/configuration.json
  const url = `${origin}${processEnvVueAppPath}config/configuration.json`;
  const headers = {
    Accept: "application/json",
    ResponseType: "application/json",
    "Cache-Control": "no-cache"
  };

  const response = await Axios.get(url, { headers }).catch(() => {
    return Promise.reject(new Error("Could not fetch configuration.json"));
  });

  sessionStorage.setItem("AUTH_API_CONFIG", JSON.stringify(response.data));

  const searchApiUrl: string = response.data["VUE_APP_BACKEND_HOST"];
  sessionStorage.setItem("VUE_APP_BACKEND_HOST", searchApiUrl);

  const frontendDomailUrl: string = response.data["VUE_APP_FRONTEND_DOMAIN"];
  sessionStorage.setItem("VUE_APP_FRONTEND_DOMAIN", frontendDomailUrl);

  const corpOnlineUrl: string = response.data["VUE_APP_CORP_ONLINE_ROOT_URL"];
  sessionStorage.setItem("VUE_APP_CORP_ONLINE_ROOT_URL", corpOnlineUrl);

  const authApiUrl: string = response.data["VUE_APP_AUTH_ROOT_API"];
  sessionStorage.setItem("VUE_APP_AUTH_ROOT_API", authApiUrl);
}
