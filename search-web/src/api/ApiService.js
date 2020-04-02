import axios from "axios";

// create axios instance to avoid overwriting global axios settings
const apiInstance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_HOST,
  headers: {}
});
export default apiInstance;
