export { setCurrentArticles, setCurrentData, onPositive, onNegative, onPolitical, onNeutral}

import { client_ws } from './data_ws.mjs'

let ws = new client_ws();

let articles = {}
let articleData = {}
let index = 0

function setCurrentArticles(input) {
  articles = input
}

function setCurrentData(index) {
  while (articles[index] == null) {
    index++
  }
  console.log('article @ index: ')
  console.log(articles[index])

  if (index < articles.length) {
    articleData.title = articles[index].title
    articleData.summary = articles[index].summary
    articleData.text = articles[index].text
    articleData.author = articles[index].authors
    articleData.link = articles[index].url
    articleData.type = 'none'
    index = index;
  } else {
    articleData.title = 'End of set'
    articleData.summary = 'End of set'
    articleData.text = 'End of set'
    articleData.author = 'End of set'
    articleData.link = 'End of set'
    articleData.type = 'none'
    index = index;
  }
  
  console.log('article data: ')
  console.log(articleData)

  updateHTML()
}

function onPositive() {
  if (articleData.title == 'End of set')
    return
  articleData.type = 'positive'
  intoJSON()
  index++
  setCurrentData(index)
}

function onNegative() {
  if (articleData.title == 'End of set')
    return
  articleData.type = 'negative'
  intoJSON()
  index++
  setCurrentData(index)
}

function onPolitical() {
  if (articleData.title == 'End of set')
    return
  articleData.type = 'political'
  intoJSON()
  index++
  setCurrentData(index)
}

function onNeutral() {
  if (articleData.title == 'End of set')
    return
  articleData.type = 'neutral'
  intoJSON()
  index++
  setCurrentData(index)
}

function intoJSON() {
  console.log('article being sent off & type: ' + articleData.title + ' ' + articleData.type)
  ws.sendJSON(JSON.stringify(articleData))
}

function updateHTML() {
  document.getElementById("source").innerHTML = articleData.author
  document.getElementById("title").innerHTML = articleData.title
  document.getElementById("text").innerHTML = articleData.text

  document.getElementById("cardTitle").innerHTML = articleData.title
  document.getElementById("cardTitle").href = articleData.link
  document.getElementById("cardFrom").innerHTML = articleData.author
  document.getElementById("cardSummary").innerHTML = articleData.summary
  document.getElementById("cardLink").innerHTML = articleData.link
  document.getElementById("cardLink").href = articleData.link
}