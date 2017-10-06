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
