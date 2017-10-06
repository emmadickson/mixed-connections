function mixConnections(){

  jQuery.get('/raw', function(data) {

   var entries = JSON.stringify(data)
   entries = entries.split("\\")

    // 3. Set up Arrays to recieve titles and posts from the txt file.
    titles = []
    posts = []
    // 4. posts the document up into lines and from individiaul lines into titles and posts

    var linesOfText = entries
    for (var i = 0; i < entries.length; i++){
       if (entries[i].length > 10){
        var limbs = entries[i].split("***");


        title = limbs[0]
        title = title.substring(1, title.length-1)
        titles.push(title)
        posts.push(limbs[1]);
      }
    }

  // 5. Randomly select a title and display it in h1 id="title"
  var randomTitle = titles[Math.floor(Math.random()*titles.length)];
  var domTitle = document.getElementById('title');
  domTitle.textContent = randomTitle;

  // 6. Shuffle posts
  shuffle(posts)

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

  // 9. Shuffle sentences
  shuffle(phrases)

  // 10. Go through phrases and select a random number
  threads = [];

  var postBody = " ";
  var postLength = Math.floor((Math.random() * 5) + 2);
  while (threads.length < postLength){
    random = getRandomIntInclusive(0,phrases.length-1);
    selection = phrases[random];
    if (threads.indexOf(selection) === -1){
      threads.push(selection);
    }
  }
  postBody = threads.join(" ");

  // 11. Take the post body and display it in the p id="missed-connection"
  var domMissedConnection = document.getElementById('missed-connection');
  domMissedConnection.textContent = postBody;
})
}

function scramble(originalText, domElement){
  var master = originalText;
  alphabet = [
  "\u2020", "\u2021", "\u2022", "\u2023", "\u2024", "\u2025", "\u2026",
  "\u2027", "\u2028", "\u2029", "\u2031", "\u2039", "\u203A", "\u203B"
  , "\u203C", "\u203D", "\u203F", "\u2040", "\u2041", "\u2042", "\u2045"
  , "\u2046", "\u2047", "\u2048", "\u204A", "\u204B", "\u2058", "\u2059"];
  for (var j = 0; j < 3; j++){
    var letterSelection = Math.floor((Math.random() * master.length) + 0);
    var letter = master.indexOf(j);
    var randomAlphabet = Math.floor((Math.random() * 25) + 0);
    var replacementLetter = alphabet[randomAlphabet]

    firstChunk = master.slice(0,letterSelection-1);
    secondChunk = master.slice(letterSelection, master.length)
    lengthCheck = firstChunk + replacementLetter + secondChunk
    if (lengthCheck.length == master.length){
        master = lengthCheck;
    }
  }

  domElement.textContent = master
}

function makeid() {
  var text = "";
  var possible = "abcdefghijklmnopqrstuvwxyz0123456789";
  for (var i = 0; i < 6; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}


// 2. Set up event listeners to change css and scramble title
function mixup(evt) {
  var post = document.getElementById("missed-connection").textContent;
  sentences = [];
  var phrase = post.match( /[^\.!\?]+[\.!\?]+/g );
  // 8. For now I'm breaking it up based on punctuation so if someone uses
  // no puntuation I ignore the whole post.
  if (phrase != null){
    for (var j = 0; j < phrase.length; j++){
      sentences.push(phrase[j]);
    }
  }
  shuffle(sentences)

  var css = document.getElementsByTagName('style')[0]
  var css = document.createElement("style");
  css.textContent = "";
  var titleFontVariant = ['small-caps', 'normal']
  var selectTitleFontVariant = Math.floor((Math.random() * 500) + 0);
  if (selectTitleFontVariant % 2 == 0){
    selectTitleFontVariant = 0;
  }
  else{
    selectTitleFontVariant = 1;
  }
  var titleFontWeight = Math.floor((Math.random() * 900) + 0);
  var titleFontFamily = ["Times New Roman", "Georgia", "Arial", "Verdana", "Courier New", "Lucida Console"]
  var selectTitleFontFamily = Math.floor((Math.random() * 5) + 0);
  var titleFontStyle = ["normal", "italic", "oblique"]
  var selectTitleFontStyle = Math.floor((Math.random() * 2) + 0);
  var titleFontSize = Math.floor((Math.random() * 20) + 8);
  var titleHexColor = makeid();

  var styles = '#title { font-variant: ' + titleFontVariant[selectTitleFontVariant] + ';font-weight: ' + titleFontWeight + '; font-style: ' + titleFontStyle[selectTitleFontStyle] + '; font-family: ' + titleFontFamily[selectTitleFontFamily] + 'px; color: #' + titleHexColor + '}';


  var backgroundColor =  makeid();

  styles += 'body { background-color: #' + backgroundColor + '}';

  for (var k = 0; k <= sentences.length; k++){
    var element = document.createElement('span');
    element.id = "missed-connection"
    var postFontVariant = ['small-caps', 'normal']
    var selectPostFontVariant = Math.floor((Math.random() * 500) + 0);
    if (selectPostFontVariant % 2 == 0){
      selectPostFontVariant = 0;
    }
    else{
      selectPostFontVariant = 1;
    }
    var postFontWeight = Math.floor((Math.random() * 900) + 0);
    var postFontFamily = ["Times New Roman", "Georgia", "Arial", "Verdana", "Courier New", "Lucida Console"]
    var selectPostFontFamily = Math.floor((Math.random() * 5) + 0);
    var postFontStyle = ["normal", "italic", "oblique"]
    var selectPostFontStyle = Math.floor((Math.random() * 2) + 0);
    var postFontSize = Math.floor((Math.random() * 50) + 14);
    var postHexColor = '#' + makeid();

    styles += '#missed-connection { font-variant: ' + postFontVariant[selectPostFontVariant] + ';font-weight: ' + postFontWeight + '; font-style: ' + postFontStyle[selectPostFontStyle] + '; font-family: ' + titleFontFamily[selectPostFontFamily] + '; font-size: ' + postFontSize + 'px; color: ' + postHexColor + '}';

    document.body.appendChild(element)
    if (css.styleSheet) css.styleSheet.cssText = styles;
    else css.appendChild(document.createTextNode(styles));
    document.getElementsByTagName("head")[0].removeChild(document.getElementsByTagName("head")[0].childNodes[0])
    document.getElementsByTagName("head")[0].appendChild(css);
  }
}