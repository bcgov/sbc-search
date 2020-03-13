import axios from "axios";
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_HOST;
export default axios;
