function activateDragAndDrop(obj, url, callback) {
    // Drag&Drop en el objeto
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("dropping")
    });
    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('drop', function (e) {
        $(this).removeClass("dropping")
        e.preventDefault();
        var files = e.originalEvent.dataTransfer.files;
        $(files).each(function(index){
            handleFileUpload(files[index], obj, url, callback);
        });
    });
    // Control Drag&Drop fuera del objeto, no necesario pero sí mejor
    $(document).on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $(document).on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        obj.removeClass("dropping")
    });
    $(document).on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
}

function handleFileUpload(files, obj, url, callback) {
    var fd = new FormData($("#upload-form")[0]);
    if (files instanceof Array)
        fd.append('image', files[0]);
    else
        fd.append('image', files);
    // Envía el csrf token con los datos de post, para que Django no lo interprete como un ataque
    // Visto en: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        url: url,
        type: 'POST',
        data: fd,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success: callback
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}