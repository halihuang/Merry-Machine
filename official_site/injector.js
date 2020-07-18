import {client_ws} from "../websocket-js/scraper_ws.mjs"

window.vue = new Vue({
  el:"#news",
  data: {
    sources: []
  },
  mounted(){
    this.$refs.articles.style.display = 'block'
    setTimeout( async () =>{
      if(true){
        var backup = await axios.get('../server/predictions.json')
        this.sources = backup.data
      }
    }, 12000)
  }
});

let ws = new client_ws()
