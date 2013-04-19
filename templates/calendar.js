function addEvent(y, m, d) {
    date = y + '-' + m + '-' + d;
    $("#dialog").load("/add-event?dialog=1&date="+date).dialog({hide:{effect:'fade', duration:800}});
}

function editEvent(y, m, d) {
    date = y + '-' + m + '-' + d;
    $("#dialog").load("/edit-event?dialog=1&date="+date).dialog({hide:{effect:'fade', duration:800}});
}

function processAjaxForm(form, handler) {
    values = Sijax.getFormValues(form);
    Sijax.setRequestUri($(form).attr('action'));
    Sijax.request(handler, [values]);
    return false;
}

function processAddForm (form) {
    processAjaxForm(form, 'process_add_event');
}

function processEditForm (form) {
    processAjaxForm(form, 'process_edit_event');
}

$(document).ready(function(){
    $('td[event-info]').tooltip({content:function(){return $(this).attr('event-info')}});
});
