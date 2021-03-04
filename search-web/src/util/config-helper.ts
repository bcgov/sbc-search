/* eslint-disable no-console */
import axios from '@/util/axios-auth'

const url = `${process.env.VUE_APP_PATH}config/configuration.json`

const headers = {
  Accept: 'application/json',
  ResponseType: 'application/json',
  'Cache-Control': 'no-cache'
}

export default class ConfigHelper {
  static async fetchConfig () {
    const response = await axios.get(url, { headers })
    sessionStorage.setItem('AUTH_API_CONFIG', JSON.stringify(response.data))

    const searchApiUrl: string = response.data['VUE_APP_BACKEND_HOST']
    axios.defaults.baseURL = searchApiUrl
    sessionStorage.setItem('VUE_APP_BACKEND_HOST', searchApiUrl)

    const frontendDomailUrl: string = response.data['VUE_APP_FRONTEND_DOMAIN']
    sessionStorage.setItem('VUE_APP_FRONTEND_DOMAIN', frontendDomailUrl)

    const corpOnlineUrl: string = response.data['VUE_APP_CORP_ONLINE_ROOT_URL']
    sessionStorage.setItem('VUE_APP_CORP_ONLINE_ROOT_URL', corpOnlineUrl)

    const hotjarId: string = response.data['HOTJAR_ID']
    sessionStorage.setItem('HOTJAR_ID', hotjarId)
  }

  /**
   * this will run everytime when vue is being loaded..so do the call only when session storage doesnt have the values
   */
  static saveConfigToSessionStorage () {
    return this.fetchConfig()
  }
}
