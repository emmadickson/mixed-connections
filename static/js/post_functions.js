function resetSentences(post){
  sentences = []
  var phrase = post.match( /[^\.!\?]+[\.!\?]+/g );
  if (phrase != null){
    for (var j = 0; j < phrase.length; j++){
      sentences.push(phrase[j]);
    }

  var myNode = document.getElementById('missed-connection')
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
  shuffle(sentences)
  sentences = sentences.join(' ')
  return sentences;
  }
}

function ScrapePosts(entries){
  shuffle(entries)
  return entries
}

function CreateDivDomElement(){
  var body = document.getElementsByTagName('missed-connection-container')[0]
  var div = document.createElement('missed-connection')
  var other = document.getElementsByTagName('other')[document.getElementsByTagName('other').length-1]
  if (other != undefined) {
    other.textContent = other.textContent.slice(0, other.textContent.length-1)
  }
  body.appendChild(div)
  return div
}
function shuffle(array) {
  for (let i = array.length; i; i--) {
      let j = Math.floor(Math.random() * i);
      [array[i - 1], array[j]] = [array[j], array[i - 1]];
  }
}
function TypeSet(spans, i, typing){

  var div = document.getElementsByTagName('missed-connection')

    div = div[div.length-1]
    if (div == undefined){
      clearInterval(typing)
    }
    else{
    div.textContent = div.textContent.slice(0, div.textContent.length-1)
    div.textContent = div.textContent + spans[i]
    div.textContent = div.textContent + "_"
  }
}
function CleanEntries(entries){
  var cleanedEntries = []
  for (var i = 0; i < entries.length; i++){
     if (entries[i] != undefined){
      cleanedEntries.push(entries[i])
    }
  }
  return cleanedEntries
}

function TypeSetOther(spans, i, typing){
  var div = document.getElementsByTagName('other')
    div = div[div.length-1]
  if (div == undefined){
    clearInterval(typing)
  }
  else{

    div.textContent = div.textContent.slice(0, div.textContent.length-1)
    div.textContent = div.textContent + spans[i]
    div.textContent = div.textContent + "_"
  }
}

function TypeSetReset(spans, i, hidden){
    var div = document.getElementsByTagName('div')
    div = div[div.length-1]
    div.textContent = div.textContent.slice(0, div.textContent.length-1)
}

function resetSpans(spans){
  spans =  spans.match( /[^\.!\?]+[\.!\?]+/g );
  shuffle(spans)
  spans = spans.join(' ')
  var myNode = document.getElementsByTagName('missed-connection-container')[0]
  while (myNode.firstChild) {
      myNode.removeChild(myNode.firstChild);
  }
  return spans;
}

function resolveDatabaseGrab(x) {
  return new Promise(resolve => {
    var databaseGrab = $.get('/raw_db')
    databaseGrab.done(function(data) {
      databaseData = data
      resolve(data)
      console.log("successful database grab")
    })
  });
}

async function GrabData() {
  entriesData = ""
  databaseData = ""
  databaseDataGrabbed = await resolveDatabaseGrab(databaseData);

  var body = document.getElementsByTagName('missed-connection-container')[0]
  var i = 0;
  var scraped_entries = SplitEntries(databaseDataGrabbed)
  var postElements = GetTitlesAndPosts(scraped_entries)
  var titles = postElements[0]
  titles = CleanEntries(titles)
  var posts = postElements[1]
  posts = CleanEntries(posts);

  GetRandomTitle(titles)
  shuffle(posts)
  phrases = SplitPosts(posts)
  shuffle(phrases)
  postBody = CreatePostBody(phrases)
  body.textContent = postBody
}
