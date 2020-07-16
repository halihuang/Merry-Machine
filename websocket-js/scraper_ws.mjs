export { client_ws }

import { new_web_socket } from './websocket.mjs'

class client_ws {

  constructor() {
    this.client_ws = new_web_socket('/scraper/ws')
    this.client_ws.onmessage = function(data) {
      console.log(data.data)
      // let parsed = JSON.parse(data.data).targets
      // console.log('message data: ' + parsed[0])
      // console.log(parsed)
      // console.log(typeof parsed)
    };
  }

  connected() {
    this.getArticles()
    console.log('woohoo! we\'re connected!')
  }

  getArticles() {
    this.client_ws.send('get articles')
  }
}