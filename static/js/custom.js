$(document).ready(function() {
var oTable = $('#search_table').dataTable( {
        "sDom": 'T<"clear">lrtip',
        "oTableTools": {
            "sSwfPath": "{% static 'extras/copy_csv_xls_pdf.swf' %}",
		    "aButtons": [ "csv", "pdf", "print" ]
        },
        "bProcessing": true,
        //"bServerSide": true,
        //"sAjaxDataProp": "aaData",
        //"sServerMethod": "POST",
        //"sAjaxSource": "{% static 'js/simple.json' %}",
        "sAjaxSource": "{% url 'search_list_json' %}",
        "aaSorting": [ [1,'desc'], [2,'desc'] ],
        // Disable sorting for the Actions column.
        "aoColumnDefs": [ { "bSortable": false, "aTargets": [ 0,4 ] } ],
        "iDisplayLength":10,
        "sPaginationType": "full_numbers"
    } );

$(function() {
    // Sets the value of the submit_button_type field if the 'Submit & Add
    // Another button is clicked.
    $('#submit-id-submit_and_add').click(function() {
        $('#id_submit_button_type').val('submit_and_add');
    });
});
} );