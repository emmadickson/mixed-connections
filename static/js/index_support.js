
// Creates the normal looking lines in the listed posts
function CreateCleanLine(post_count){
  var list = document.getElementById("title_list");
  var par = document.createElement('p')
  par.id = 'post'
  par.style.position = 'absolute'
  par.style.left = 100;
  par.style.top = topNum

  topNum = topNum + 50;
  var pseudoBullet = document.createElement('span')
  pseudoBullet.id = "pseudoBullet"
  pseudoBullet.textContent = "*"
  par.appendChild(pseudoBullet)

  var timeSpan = document.createElement('span')
  timeSpan.id = "timeSpan"
  time = entries[post_count]['time'];
  timeSpan.textContent = time
  par.appendChild(timeSpan)

  var titleSpan = document.createElement('a')
  titleSpan.id = "titleSpan"
  titleSpan.href = "/missed"
  title = entries[post_count]['title'];
  titleSpan.textContent = title
  par.appendChild(titleSpan)

  var locationSpan = document.createElement('span')
  loc = "("+(entries[post_count]['location'])+")"
  locationSpan.textContent = loc
  par.appendChild(locationSpan)

  list.appendChild(par)
}

// Creates the off center lines in the listed post
function CreateMessyLine(par, count){
  var list = document.getElementById("title_list");
  par.id = 'post'
  par.style.position = 'absolute'
  par.style.left = Math.floor(Math.random() * ($(window).width()-500 - 0 + 1)) + 0;
  par.style.top = topNum
  topNum = topNum + Math.floor(Math.random() * (150 - 20 + 1)) + 20;
  var timeSpan = document.createElement('span')
  timeSpan.id = "timeSpan"
  time = entries[count]['time'];
  timeSpan.textContent = time
  par.appendChild(timeSpan)

  var titleSpan = document.createElement('a')
  titleSpan.id = "titleSpan"
  titleSpan.href = "/missed"
  title = entries[count]['title'];
  titleSpan.textContent = title
  par.appendChild(titleSpan)

  var locationSpan = document.createElement('span')
  loc = "("+(entries[count]['location'])+")"
  locationSpan.textContent = loc
  par.appendChild(locationSpan)

  list.appendChild(par)
}

// Creates the scrambled lines in the listed posts
function CreateLine(par, count){
  // 1. Use a set interval to constantly Scramble location text
  var list = document.getElementById("title_list");
  par.id = 'post'
  par.style.position = 'absolute'
  par.style.left = Math.floor(Math.random() * ($(window).width()-500 - 0 + 1)) + 0;
  par.style.top = topNum
  topNum = topNum + Math.floor(Math.random() * (150 - 20 + 1)) + 20;
  var timeSpan = document.createElement('span')
  timeSpan.id = "timeSpan"
  time = entries[count]['time'];
  timeSpan.textContent = time
  par.appendChild(timeSpan)

  var a = document.createElement('a')
  var titleScram = document.createElement('titleScram')
  titleScram.id = "titleScram"
  titleScram.href = "/missed"
  title = entries[count]['title'];
  titleScram.textContent = title
  a.appendChild(titleScram)
  par.appendChild(a)

  var locationSpan = document.createElement('span')
  loc = "("+(entries[count]['location'])+")"
  locationSpan.textContent = loc
  par.appendChild(locationSpan)

  list.appendChild(par)
}
