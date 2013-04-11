function addEvent(y, m, d) {
    date = y + '-' + m + '-' + d;
    $("#dialog").load("/add-event?dialog=1&date="+date).dialog({});
}

function processAjaxForm(form) {
    values = Sijax.getFormValues(form);
    Sijax.setRequestUri($(form).attr('action'));
    Sijax.request('process_add_event', [values]);
    return false;
}

