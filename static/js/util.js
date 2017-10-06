function hexToBase64(hexstring) {
  return btoa(hexstring.match(/\w{2}/g).map(function(a) {
      return String.fromCharCode(parseInt(a, 16));
  }).join(""));
}

function hex2bin(hex){
  return ("00000000" + (parseInt(hex, 16)).toString(2)).substr(-8);
}

function bin_to_dec(bstr) {
  return parseInt((bstr + '')
  .replace(/[^01]/gi, ''), 2);
}

function makeid() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  for (var i = 0; i < 2; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

// 1. clean is a function used to remove blank spaces from the array of
// titles and posts and shuffle is a function used to shuffle the array of
// phrases. getRandomIntInclusive is a function designed to select a
// number randomly inclusive of ints.
Array.prototype.clean = function(deleteValue) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] == deleteValue) {
      this.splice(i, 1);
      i--;
    }
  }
  return this;
};

function shuffle(a) {
    for (let i = a.length; i; i--) {
        let j = Math.floor(Math.random() * i);
        [a[i - 1], a[j]] = [a[j], a[i - 1]];
    }
}

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
