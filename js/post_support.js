//Support function that shuffles the sentences in a post
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

// Support function that creates a dom element to be used in apost
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

// Support function that shuffles given array
function shuffle(array) {
  for (let i = array.length; i; i--) {
      let j = Math.floor(Math.random() * i);
      [array[i - 1], array[j]] = [array[j], array[i - 1]];
  }
}

// Support function to imitate typing
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

// Support function that weeds out null data
function CleanEntries(entries){
  var cleanedEntries = []
  for (var i = 0; i < entries.length; i++){
     if (entries[i] != undefined){
      cleanedEntries.push(entries[i])
    }
  }
  return cleanedEntries
}

// Support function to break up a post into sentences
function CleanerPost(post){
  sentences = [];
  var phrase = post.match( /[^\.!\?]+[\.!\?]+/g );
  if (phrase != null){
    for (var j = 0; j < phrase.length; j++){
      sentences.push(phrase[j]);
    }
  }
  return sentences
}

// Support function to create post
async function GrabData() {
  entriesData = ""

  // Support to grab stored posts
  var databaseData = JSON.parse(document.getElementById('raw_db').innerHTML);

  var body = document.getElementsByTagName('missed-connection-container')[0]
  var i = 0;
  var scraped_entries = SplitEntries(databaseData)
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
