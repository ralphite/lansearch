$(document).ready(function () {
    $('#search form, #results form').submit(function (event) {
        if ($.trim($('.searchbox').val()).length > 0) {
            return true;
        }
        return false;
    });

    $('.searchbox').focus(function (event) {
        this.selectionStart = this.selectionEnd = this.value.length;
    });

    $('.searchbox').focus();

    var t = getUrlParameter('t') || 'match';
    $('#' + t).removeClass('btn-default').addClass('btn-info').addClass('selected');

    $('.copy-button').each(function () {
        var client = new ZeroClipboard($(this));
    });
});

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

var search = function () {
    var q = $('.searchbox').val();
    window.location.href = 'search?q=' + q + '&t=' + $(event.target).attr('id');
};