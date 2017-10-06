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
