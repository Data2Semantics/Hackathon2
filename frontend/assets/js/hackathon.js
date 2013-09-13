

function getUrl(theUrl, extraParameters) {
    var extraParametersEncoded = $.param(extraParameters);
    var seperator = theUrl.indexOf('?') == -1 ? "?" : "&";

    return(theUrl + seperator + extraParametersEncoded);
}

$.urlParam = function(name){
    var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else {
       return results[1] || 0;
    }
}
