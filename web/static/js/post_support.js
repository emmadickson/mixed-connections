// Support functions for the missed page

// Support function that creates a dom element to be used in a post
function createDivDomElement(){
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

// Support function to split up entries
function splitEntries(data){
  var entries = (data)
  entries = entries['posts']
  return entries
}

// Support function to return lists of titles and posts
function getTitlesAndPosts(entries){
  titles = []
  posts = []

  for (var i = 0; i < entries.length; i++){
    title = entries[i].title
    titles.push(title)
    posts.push(entries[i].body);
  }

  return [titles, posts]
}

// Support function to return random title
function getRandomTitle(titles){
  var domTitle = document.getElementById('title');
  domTitle.textContent = titles;
}

// Support function to imitate typing
function typeSet(spans, i, typing){
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
function cleanEntries(entries){
  var cleanedEntries = []
  for (var i = 0; i < entries.length; i++){
     if (entries[i] != undefined){
      cleanedEntries.push(entries[i])
    }
  }
  return cleanedEntries
}

// Support function to grab stored posts
function resolvePostGrab(x) {
  return new Promise(resolve => {
    var databaseGrab = $.get('/random_post')
    databaseGrab.done(function(data) {
      databaseData = data
      resolve(data)
      console.log("successful post grab")
    })
  });
}

// Support function to break up a post into sentences
function cleanerPost(post){
  sentences = [];
  var phrase = post.match( /[^\.!\?]+[\.!\?]+/g );
  if (phrase != null){
    for (var j = 0; j < phrase.length; j++){
      sentences.push(phrase[j]);
    }
  }
  return sentences
}

// Support function to build post body
function createPostBody(phrases){
  threads = [];
  var postLength = Math.floor((Math.random() * 5) + 2);
  var postBody = " ";

  while (threads.length < postLength){
    random = Math.floor(Math.random() * phrases.length-1);
    selection = phrases[random];
    if (threads.indexOf(selection) === -1){
      threads.push(selection);
    }
  }

  return threads
}

//Support function to split a post up into individual sentences
function splitPosts(posts){
  phrases = [];
  for (var k = 0; k < posts.length; k++){
    if (posts[k] != undefined){
      var sentences = posts[k].match( /[^\.!\?]+[\.!\?]+/g );
      if (sentences != null){
        for (var j = 0; j < sentences.length; j++){
          phrases.push(sentences[j]);
        }
      }
    }
  }
  return phrases
}

// Support function to create post
async function grabData() {
  entriesData = ""
  databaseData = ""
  databaseDataGrabbed = await resolvePostGrab(databaseData);

  var body = document.getElementsByTagName('missed-connection-container')[0]
  var i = 0;
  var scraped_entries = splitEntries(databaseDataGrabbed)
  console.log(scraped_entries)
  var titles = scraped_entries[4]
  var posts = scraped_entries[0]

  getRandomTitle(titles)
  phrases = splitPosts(posts)
  shuffle(phrases)
  postBody = createPostBody(phrases)
  body.textContent = postBody
}
