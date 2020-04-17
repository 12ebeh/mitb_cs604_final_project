function show_uploaded_image(response) {
    console.log('uploaded image')
    console.log(response)
    imgContainer = response.uploaded_image_id + '_img'
    $('#'+imgContainer).attr('src', response.uploaded_image_url)
}

function set_training_status(msg) {
    $('#train_status').text(msg)
}

function update_train_status(response) {
    set_training_status(response.training_status)
}

function show_blend_image(response) {
    console.log('blended image')
}

$(document).ready(function() { 
    // bind 'myForm' and provide a simple callback function 
    $('.upload_image_form').ajaxForm({
        dataType: 'json',
        success: show_uploaded_image
    })
    
    $('.train_images_form').ajaxForm({
        dataType: 'json',
        beforeSubmit: (function(formData, jqForm, options) {
            set_training_status("Extracting images latent representations...")
        }),
        success: update_train_status
    })
    
    $('.blend_images_form').ajaxForm({
        dataType: 'json',
        success: show_blend_image
    })
})