import {client_ws} from "../websocket-js/positive_ws.mjs"
let ws = new client_ws()


var vue = new Vue({
  el:"#news",
  data: {
    sources: ws.sources
  },
});