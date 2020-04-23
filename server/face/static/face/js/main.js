intervalID = 0

function show_uploaded_image(response) {
    console.log('uploaded image');
    console.log(response);
    imgContainer = response.uploaded_image_id + '_img';
    $('#'+imgContainer).attr('src', response.uploaded_image_url);
    $('#'+imgContainer).attr('style', 'height: 512px;');
}

function set_training_status(msg, show_img) {
    $('#train_status').text(msg);
    if (show_img) {
        $('#train_loading').show();
    } else {
        $('#train_loading').hide();
    }
}

function poll_train_status(response) {
    intervalID = setInterval(function () {
        $.ajax({
	    type: 'POST',
            url: 'poll_training',
            data: {
                session_id: response.session_id,
                csrfmiddlewaretoken: Cookies.get('csrftoken')
            },
	    success: update_train_status
        })
    }, 5000);
}

function update_train_status(response) {
    console.log("update_train_status");
    console.log(response);
    if (response.train_state == 1) {
        set_training_status("Extracting latent features from images...", true);
    } else if (response.train_state == 2) {
        set_training_status("Latent features extracted!", false);
        clearInterval(intervalID);
    } else {
        set_training_status("Latent features extraction failed.", false);
        $(".train_image_submit").attr("disabled", false);
        clearInterval(intervalID);
    }
}

function show_blend_image(response) {
    console.log('blended image');
    console.log(response);
    $('#blended_image').attr('src', response.result_url);
    $('#blended_image').attr('style', 'height: 512px;');
    $('.blend_image_submit').attr('disabled', false);
}

$(document).ready(function() {
    $("#train_loading").hide();
    // bind 'myForm' and provide a simple callback function 
    $('.upload_image_form').ajaxForm({
        dataType: 'json',
        timeout: 0,
        beforeSubmit: (function(formData, jqForm, options) {
            console.log(formData)
            console.log(jqForm)
            console.log(options)
            var pic_key = ""
            for (i=0; i<formData.length; i++) {
                if (formData[i]["name"] == "image_id") {
                    pic_key = formData[i]["value"]
                }
            }
            $("#image_upload_submit_"+pic_key).attr("disabled", true)
	}),
        success: show_uploaded_image
    });
    
    $('.train_images_form').ajaxForm({
        dataType: 'json',
        timeout: 0,
        beforeSubmit: (function(formData, jqForm, options) {
            $(".train_image_submit").attr("disabled", true);
            set_training_status("Extracting latent features from images...", true);
        }),
        success: poll_train_status
    })

    $('.blend_images_form').ajaxForm({
        dataType: 'json',
        timeout: 0,
	beforeSubmit: (function(formData, jqForm, options) {
	    $(".blend_image_submit").attr("disabled", true)
        }),
        success: show_blend_image
    });
})
