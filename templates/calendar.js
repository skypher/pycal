function addEvent(y, m, d) {
    date = y + '-' + m + '-' + d;
    $("#dialog").load("/add-event?dialog=1&date="+date).dialog({hide:{effect:'fade', duration:800}});
}

function processAjaxForm(form) {
    values = Sijax.getFormValues(form);
    Sijax.setRequestUri($(form).attr('action'));
    Sijax.request('process_add_event', [values]);
    return false;
}

$(document).ready(function(){
  $('.calendar td').mouseover(function(){$(this).find('.actions a').css('visibility','visible');});
  $('.calendar td').mouseout(function(){$(this).find('.actions a').css('visibility','hidden');});
});
