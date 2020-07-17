export { setCurrentArticles, setCurrentData, onPositive, onNegative, onPolitical, onNeutral}

import { client_ws } from '../websocket-js/data_ws.mjs'

let ws = new client_ws();

let articles = {}
let articleData = {}
let sourceIndex = 0
let articleIndex = 0

function setCurrentArticles(input) {
  articles = input
}

function setCurrentData() {
  console.log('hello')
  while (articles[sourceIndex].articles[articleIndex] == null) {
    if (articleIndex < articles[sourceIndex].articles.length) {
      articleIndex++
    } else {
      articleIndex = 0
      sourceIndex++
    }
  }
  console.log('article @ index: ')
  console.log(articles[sourceIndex])
  console.log(articles[sourceIndex].articles[articleIndex])

  if (articleIndex < articles[sourceIndex].articles.length) {
    articleData.title = articles[sourceIndex].articles[articleIndex].title
    articleData.summary = articles[sourceIndex].articles[articleIndex].summary
    articleData.text = articles[sourceIndex].articles[articleIndex].text
    articleData.author = articles[sourceIndex].articles[articleIndex].meta[0]
    articleData.link = articles[sourceIndex].articles[articleIndex].url
    articleData.date = articles[sourceIndex].articles[articleIndex].meta[1]
    articleData.source = articles[sourceIndex].source
    articleData.positive = '0'
    articleData.negative = '0'
    articleData.political = '0'
    articleData.neutral = '0'
  } else {
    articleData.title = 'End of set'
    articleData.summary = 'End of set'
    articleData.text = 'End of set'
    articleData.author = 'End of set'
    articleData.link = 'End of set'
    articleData.date = 'End of set'
    articleData.source = 'End of set'
    articleData.positive = '0'
    articleData.negative = '0'
    articleData.political = '0'
    articleData.neutral = '0'
    if (sourceIndex < articles.length) {
      sourceIndex++;
      articleIndex = 0;
      setCurrentData()
      return
    } else {}
  }
  
  console.log('article data: ')
  console.log(articleData)

  updateHTML()
}

function onPositive() {
  if (articleData.title == 'End of set')
    return
  articleData.positive = '1'
  intoJSON()
  articleIndex++
  setCurrentData()
}

function onNegative() {
  if (articleData.title == 'End of set')
    return
  articleData.negative = '1'
  intoJSON()
  articleIndex++
  setCurrentData()
}

function onPolitical() {
  if (articleData.title == 'End of set')
    return
  articleData.political = '1'
  intoJSON()
  articleIndex++
  setCurrentData()
}

function onNeutral() {
  if (articleData.title == 'End of set')
    return
  articleData.neutral = '1'
  intoJSON()
  articleIndex++
  setCurrentData()
}

function intoJSON() {
  console.log('article being sent off & type: \n' + articleData.title + '\nPositive:' + articleData.positive + '\nNegative:' + articleData.negative + '\nPolitical:' + articleData.political + '\nNeutral:' + articleData.neutral)
  ws.sendJSON(JSON.stringify(articleData))
}

function updateHTML() {
  document.getElementById("source").innerHTML = articleData.source + ' ' + articleData.author
  document.getElementById("title").innerHTML = articleData.title
  document.getElementById("text").innerHTML = articleData.text

  document.getElementById("cardTitle").innerHTML = articleData.title
  document.getElementById("cardTitle").href = articleData.link
  document.getElementById("cardFrom").innerHTML = articleData.author
  document.getElementById("cardSummary").innerHTML = articleData.summary
  document.getElementById("cardLink").innerHTML = articleData.source
  document.getElementById("cardLink").href = articleData.link
}