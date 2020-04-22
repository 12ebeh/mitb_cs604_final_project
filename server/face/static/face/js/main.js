function show_uploaded_image(response) {
    console.log('uploaded image')
    console.log(response)
    imgContainer = response.uploaded_image_id + '_img'
    $('#'+imgContainer).attr('src', response.uploaded_image_url)
    $('#'+imgContainer).attr('style', 'height: 512px;')
}

function set_training_status(msg) {
    $('#train_status').text(msg)
    $('#train_loading').hide()
}

function update_train_status(response) {
    set_training_status(response.training_status)
}

function show_blend_image(response) {
    console.log('blended image')
    console.log(response)
    $('#blended_image').attr('src', response.result_url)
    $('#blended_image').attr('style', 'height: 512px;')
    $('.blend_image_submit').attr('disabled', false)
}

$(document).ready(function() {
    $("#train_loading").hide()
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
    })
    
    $('.train_images_form').ajaxForm({
        dataType: 'json',
        timeout: 0,
        beforeSubmit: (function(formData, jqForm, options) {
            $(".train_image_submit").attr("disabled", true)
            set_training_status("Extracting images latent representations...")
            $("#train_loading").show()
        }),
        success: update_train_status
    })
    
    $('.blend_images_form').ajaxForm({
        dataType: 'json',
        timeout: 0,
	beforeSubmit: (function(formData, jqForm, options) {
	    $(".blend_image_submit").attr("disabled", true)
        }),
        success: show_blend_image
    })
})
