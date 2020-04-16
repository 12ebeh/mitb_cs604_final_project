function show_uploaded_image(response) {
    console.log('json returned!')
    console.log(response)
    imgContainer = response.uploaded_image_id + '_img'
    $('#'+imgContainer).attr('src', response.uploaded_image_url)
}

$(document).ready(function() { 
    // bind 'myForm' and provide a simple callback function 
    $('.upload_image_form').ajaxForm({
        dataType: 'json',
        success: show_uploaded_image
    })
})