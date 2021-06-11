import omit from 'lodash-es/omit'
import dayjs from 'dayjs'
const qs = require('qs')
const fileDownload = require('js-file-download')
export * from './axios-auth'
export * from './config-helper'

export function getTextFromValues (values, value) {
  const result = values.find(v => v.value === value)
  if (!result) {
    return 'N/A'
  }
  return result.text
}

export function buildQueryString (filters) {
  let queryString = ''
  filters.map(f => {
    let temp = omit(f, 'uid')
    queryString === ''
      ? (queryString += qs.stringify(temp))
      : (queryString += '&' + qs.stringify(temp))
  })
  return queryString
}

export function getDeepLink (corpNum) {
  return `${sessionStorage.getItem('BCONLINE_URL')}`
}

export async function downloadFile (data, fileName) {
  return fileDownload(
    data,
    fileName || 'DS-Results.xlsx',
    'application/vnd.ms-excel'
  )
}

export function formatDate (d) {
  return d ? dayjs(d).format('YYYY-MM-DD') : '-'
}
