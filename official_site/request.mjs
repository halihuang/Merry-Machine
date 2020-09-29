export { request }

const url='http://amarmaks.pythonanywhere.com/data'


async function request() {
  return axios.get(url)
}