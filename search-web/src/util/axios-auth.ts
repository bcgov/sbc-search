import axios from 'axios'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'

const instance = axios.create()

instance.interceptors.request.use(
  config => {
    config.headers.common['Authorization'] = `Bearer ${sessionStorage.getItem(
      SessionStorageKeys.KeyCloakToken
    )}`
    if (sessionStorage.getItem(SessionStorageKeys.CurrentAccount)) {
      const accountInfo = JSON.parse(
        sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
      )
      config.headers['X-Account-Id'] = accountInfo.id
    }
    return config
  },
  error => Promise.reject(error)
)

instance.interceptors.response.use(
  response => response,
  error => Promise.reject(error)
)

export default instance
