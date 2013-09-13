

function getUrl(theUrl, extraParameters) {
    var extraParametersEncoded = $.param(extraParameters);
    var seperator = theUrl.indexOf('?') == -1 ? "?" : "&";

    return(theUrl + seperator + extraParametersEncoded);
}