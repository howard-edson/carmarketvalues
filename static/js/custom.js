$(document).ready(function() {

$('.carousel').carousel({
     interval:2000
});


    // Sets the value of the submit_button_type field if the 'Submit & Add
    // Another button is clicked. */
    $('#submit-id-submit_and_add').click(function() {
        $('#id_submit_button_type').val('submit_and_add');
    });


var make=$('select[name=vehicle_make]').val();
var model=$('#id_model').val();

if (make && make != 'NA') {
        request_url = '/search/get_models/' + make +'/';
        $.ajax({
            url: request_url,
            dataType: 'json',
            type: "GET", 
            success: function(data){
            	$('select[name=vehicle_model]').find('option').remove().end();
            	$('select[name=vehicle_model]').append('<option value="NA"> --------------- SELECT MAKE ------------- </option>');
            	
                $.each(data, function(key, value){
                    $('select[name=vehicle_model]').append('<option value="' + value + '">' + value +'</option>');
                    var t='select[name=vehicle_model] option[value="'+model+'"]';
                    
                    $(t).attr("selected","selected");
                    //$('option[value=model]').attr("selected",true);
                    $("select[name=vehicle_model]").attr('disabled', false);
                });
        }
        
    });
    }


});