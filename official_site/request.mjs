export { request }

const url='https://amarmaks.pythonanywhere.com/data'


async function request() {
  return axios.get(url)
}