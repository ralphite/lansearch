$(document).ready(function() {
    $('#search form, #results form').submit(function(event) {
        if($.trim($('.searchbox').val()).length > 0) {
            return true;
        }
        return false;
    });

    $('.searchbox').focus(function(event) {
        this.selectionStart = this.selectionEnd = this.value.length;
    });

    $('.searchbox').focus();

});

var select = function() {
    $('.searchtype').removeClass('btn-info').removeClass('selected').addClass('btn-default');
    $(event.target).addClass('btn-info').addClass('selected');
};