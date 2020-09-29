import { request } from "./request.mjs"

window.vue = new Vue({
  el:"#news",
  data: {
    sources: []
  },
  mounted: async function(){
    await request().then(response => {
      // handle success
      console.log(response.data)
      window.vue.sources = response.data
    })
    .catch(error => {
      // handle error
      console.log(error)
    })
    this.$refs.articles.style.display = 'block'
    setTimeout( async () =>{
      if(this.sources.length == 0){
        var backup = await axios.get('../server/predictions.json')
        this.sources = backup.data
      }
    }, 12000)
  }
});
