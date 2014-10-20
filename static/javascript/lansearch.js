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

    var t = getUrlParameter('t') || 'match';
    $('#'+t).removeClass('btn-default').addClass('btn-info').addClass('selected');
});

function getUrlParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
}

var search = function() {
    var q = $('.searchbox').val();
    window.location.href = 'search?q=' + q + '&t=' + $(event.target).attr('id');
};

$('.copy-button').each(function() {
  //Create a new clipboard client
  var clip = new ZeroClipboard.Client();
  clip.setHandCursor( true );

  //Glue the clipboard client to the last td in each row
  clip.glue(this);

 // var url = $(this).attr("href");
  //Grab the text from the parent row of the icon
 // var code = $(this).children('span').html();
  clip.setText('aaa');

  //Add a complete event to let the user know the text was copied
  clip.addEventListener('complete', function(client, text) {
    alert("Copied text to clipboard:\n" + text);
    //popUp(url);
  });
});