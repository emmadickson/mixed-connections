// Support functions for the index page

// Support function that creates the bullets for each post
function createBullet(par){
  var pseudoBullet = document.createElement('span')
  pseudoBullet.id = "pseudoBullet"
  pseudoBullet.textContent = "*"
  par.appendChild(pseudoBullet)
  return par
}

// Support function that creates the Time Stamp for each post
function createTimeSpan(par, entries, postCount){
  var timeSpan = document.createElement('span')
  timeSpan.id = "timeSpan"
  time = entries[postCount]['time'];
  timeSpan.textContent = time
  par.appendChild(timeSpan)
  return par
}

// Support function that creates the Titile for each post
function createTitle(par, entries, postCount){
  var titleSpan = document.createElement('a')
  titleSpan.id = "titleSpan"
  titleSpan.href = "/missed"
  title = entries[postCount]['title'];
  titleSpan.textContent = title
  par.appendChild(titleSpan)
  return par
}

// Support function that creates a scrambling title for each post
function createScrambledTitle(par, entries, postCount){
  var titleSpan = document.createElement('a')
  var titleScram = document.createElement('titleScram')
  titleScram.id = "titleScram"
  titleScram.href = "/missed"
  title = entries[postCount]['title'];
  titleScram.textContent = title
  titleSpan.appendChild(titleScram)
  par.appendChild(titleSpan)
  return par
}

// Support function that creates the location for each post
function createLocation(par, entries, postCount){
  var list = document.getElementsByTagName("title-list")[0];
  var locationSpan = document.createElement('span')
  locationSpan.style.color = 'blue'
  loc = "("+(entries[postCount]['location'])+")"
  locationSpan.textContent = loc
  par.appendChild(locationSpan)
  list.appendChild(par)
  return par
}

// Support function that styles the post as a normally aligned line
function styleCleanLine(line, topNum){
  line.style.position = 'absolute'
  line.style.left = 100;
  line.style.top = topNum
  topNum = topNum + 50;
  return topNum
}

// Support function that styles the off center lines in the post
function styleMessyLine(par, topNum){
  par.style.position = 'absolute'
  par.style.left = Math.floor(Math.random() * ($(window).width()-500 - 0 + 1)) + 0;
  par.style.top = topNum
  topNum = topNum + Math.floor(Math.random() * (150 - 50 + 1)) + 50;
  var a = document.createElement('a')
  return topNum
}
