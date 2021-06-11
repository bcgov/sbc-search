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

    const authApiUrl: string = response.data['AUTH_API_URL'] + response.data['AUTH_API_VERSION']
    axios.defaults.baseURL = authApiUrl
    sessionStorage.setItem('AUTH_API_URL', authApiUrl)

    const statusApiUrl: string = response.data['STATUS_API_URL'] + response.data['STATUS_API_VERSION']
    axios.defaults.baseURL = statusApiUrl
    sessionStorage.setItem('STATUS_API_URL', statusApiUrl)

    const searchApiUrl: string = response.data['SEACH_API_URL'] + response.data['SEACH_API_VERSION']
    axios.defaults.baseURL = searchApiUrl
    sessionStorage.setItem('SEACH_API_URL', searchApiUrl)

    const authWebUrl: string = response.data['AUTH_WEB_URL']
    sessionStorage.setItem('AUTH_WEB_URL', authWebUrl)

    const frontendDomainUrl: string = response.data['DIRECTOR_SEARCH_URL']
    sessionStorage.setItem('DIRECTOR_SEARCH_URL', frontendDomainUrl)

    const corpOnlineUrl: string = response.data['BCONLINE_URL']
    sessionStorage.setItem('BCONLINE_URL', corpOnlineUrl)

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
