ALPHABET = [
"\u2020", "\u2021", "\u2022", "\u2023", "\u2024", "\u2025", "\u2026",
"\u2027", "\u2028", "\u2029", "\u2031", "\u2039", "\u203A", "\u203B"
, "\u203C", "\u203D", "\u203F", "\u2040", "\u2041", "\u2042", "\u2045"
, "\u2046", "\u2047", "\u2048", "\u204A", "\u204B", "\u2058", "\u2059"];

function shuffle(array) {
  for (let i = array.length; i; i--) {
      let j = Math.floor(Math.random() * i);
      [array[i - 1], array[j]] = [array[j], array[i - 1]];
  }
}

function CleanPost(post){
  sentences = [];
  var phrase = post.textContent.match( /[^\.!\?]+[\.!\?]+/g );
  // 8. For now I'm breaking it up based on punctuation so if someone uses
  // no puntuation I ignore the whole post.
  if (phrase != null){
    for (var j = 0; j < phrase.length; j++){
      sentences.push(phrase[j]);
    }
  }
  return sentences
}
function scramble(originalText, domElement){
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

function AdjustColor(count){
  var hidden = document.getElementById('hidden')
  var hidden2 = document.getElementById('hidden2')
  var color_value = 255 - count/4;
  var color_value2 = 255 - count2/8;
  hidden.style.color = "rgb(" + color_value + "," + color_value+ "," + color_value + ")"
  if (beneath_flag == true){
    count2 = count2 + 1;
    hidden2.style.color = "rgb(" + color_value2 + "," + color_value2 + "," + color_value2 + ")"
  }
}


function MixupPost(evt) {
  var post = document.getElementById("missed-connection");
  sentences = CleanPost(post)
  shuffle(sentences)
  post.textContent = sentences.join(' ')
  count = count + 1;
  AdjustColor(count)
}

function SplitEntries(data){
  var entries = JSON.stringify(data)
  entries = entries.split("\\")
  return entries
}

function GetTitlesAndPosts(entries){
  // 3. Set up Arrays to recieve titles and posts from the txt file.
  titles = []
  posts = []

  // 4. posts the document up into lines and from individiaul lines into titles and posts
  for (var i = 0; i < entries.length; i++){
     if (entries[i].length > 10){
      var limbs = entries[i].split("***");
      title = limbs[0]
      title = title.substring(1, title.length-1)
      titles.push(title)
      posts.push(limbs[1]);
    }
  }
  return [titles, posts]
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

function GetRandomTitle(titles){
  // 5. Randomly select a title and display it in h1 id="title"
  var randomTitle = titles[Math.floor(Math.random()*titles.length)];
  var domTitle = document.getElementById('title');
  domTitle.textContent = randomTitle;
}

function SplitPosts(posts){
  // 7. Break the posts up into sentences
  phrases = [];
  for (var k = 0; k < posts.length; k++){
    if (posts[k] != undefined){
      var sentences = posts[k].match( /[^\.!\?]+[\.!\?]+/g );
      // 8. For now I'm breaking it up based on punctuation so if someone uses
      // no puntuation I ignore the whole post.
      if (sentences != null){
        for (var j = 0; j < sentences.length; j++){
          phrases.push(sentences[j]);
        }
      }
    }
  }
  return phrases
}

function CreatePostBody(phrases){
  threads = [];
  var postLength = Math.floor((Math.random() * 5) + 2);
  var postBody = " ";
  while (threads.length < postLength){
    random = getRandomIntInclusive(0,phrases.length-1);
    selection = phrases[random];
    if (threads.indexOf(selection) === -1){
      threads.push(selection);
    }
  }
  postBody = threads.join(" ");
  return postBody
}

function CreateMixedConnection(){

  jQuery.get('/raw_db', function(data) {

   var entries = SplitEntries(data)

   var postElements = GetTitlesAndPosts(entries)

   var titles = postElements[0]
   titles = CleanEntries(titles)

   var posts = postElements[1]
   posts = CleanEntries(posts)

  GetRandomTitle(titles)

  // 6. Shuffle posts
  shuffle(posts)

  // 7. Break the posts up into sentences
  phrases = SplitPosts(posts)

  // 9. Shuffle sentences
  shuffle(phrases)

  postBody = CreatePostBody(phrases)

  // 11. Take the post body and display it in the p id="missed-connection"
  var domMissedConnection = document.getElementById('missed-connection');
  domMissedConnection.textContent = postBody;
})
}
