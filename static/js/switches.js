// Constants

// Reference for Scramble function
ALPHABET = [
"\u2020", "\u2021", "\u2022", "\u2023", "\u2024", "\u2025", "\u2026",
"\u2027", "\u2028", "\u2029", "\u2031", "\u2039", "\u203A", "\u203B"
, "\u203C", "\u203D", "\u203F", "\u2040", "\u2041", "\u2042", "\u2045"
, "\u2046", "\u2047", "\u2048", "\u204A", "\u204B", "\u2058", "\u2059"];

// Scrambled the text content of the associated element
function Scramble(originalText, domElement){
  var alteredText = originalText;
  for (var j = 0; j < 3; j++){
    var letterSelection = Math.floor((Math.random() * alteredText.length) + 0);
    var letter = alteredText.indexOf(j);
    var randomAlphabet = Math.floor((Math.random() * 25) + 0);
    var replacementLetter = ALPHABET[randomAlphabet]
    firstChunk = alteredText.slice(0,letterSelection-1);
    secondChunk = alteredText.slice(letterSelection, alteredText.length)
    lengthCheck = firstChunk + replacementLetter + secondChunk
    if (lengthCheck.length == alteredText.length){
        alteredText = lengthCheck;
    }
  }
  domElement.textContent = alteredText
}

// Support function to eliminate null entries if found
function CleanPost(post){
  sentences = [];
  var phrase = post.textContent.match( /[^\.!\?]+[\.!\?]+/g );
  if (phrase != null){
    for (var j = 0; j < phrase.length; j++){
      sentences.push(phrase[j]);
    }
  }
  return sentences
}

// Support function to split up entries
function SplitEntries(data){
  var entries = (data)
  entries = entries['posts']
  return entries
}

// Support function to return lists of titles and posts
function GetTitlesAndPosts(entries){
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
function GetRandomTitle(titles){
  var randomTitle = titles[Math.floor(Math.random()*titles.length)];
  var domTitle = document.getElementById('title');
  domTitle.textContent = randomTitle;
}

//Support function to split a post up into individual sentences
function SplitPosts(posts){
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

// Support function to build post body
function CreatePostBody(phrases){
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

// Support function to scrape and add new posts
async function Grab() {
  $.get( "add", function( data ) {
  });
}
