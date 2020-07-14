export { client_ws }

import { setCurrentArticles, setCurrentData } from './training_injector.mjs'

import { new_web_socket } from './websocket.mjs'

class client_ws {

  constructor() {
    this.client_ws = new_web_socket('/data/ws')
    this.client_ws.onmessage = function(data) {
      let parsed = JSON.parse(data.data).targets
      console.log('message data: ' + parsed[0])
      console.log(parsed)
      console.log(typeof parsed)
      if (typeof parsed === 'object') {
        setCurrentArticles(parsed)
        setCurrentData()
      }
    };
  }

  connected() {
    console.log('woohoo! we\'re connected!')
  }

  sendJSON(data) {
    this.client_ws.send(data)
  }
}