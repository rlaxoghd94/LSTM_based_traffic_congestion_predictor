// var APPID = 'aNLnRJ4q';
// var DEG = 'c';
//
function startTime() {
    var today = new Date();
    var y = today.getFullYear();
    var mm = today.getMonth();
    var dd = today.getDay();

    mm = checkTime(mm);
    dd = checkTime(dd);

    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('card__date').innerHTML = y + "/" + mm + "/" + dd;
    document.getElementById('card__time').innerHTML =
        h + ":" + m + ":" + s;
}

function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }
      // add zero in front of numbers < 10
    return i;
}