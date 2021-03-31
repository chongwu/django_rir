function getPositions(position_type) {
    let checkboxes = '';
    django.jQuery.getJSON('/adaptation/getPositions/', {position_type: position_type}, function(data){
       for (let i = 0; i < data.length; i++) {
           let checked = false;
           if(typeof POINT_OBJECT !== 'undefined' && POINT_OBJECT.positions.includes(data[i].pk)){
                checked = true;
           }
           checkboxes += '<li><label for="id_positions_'+ i +'"><input type="checkbox" name="positions" value="'+ data[i].pk +'" required=""' + (checked ? ' checked': '') + ' id="id_positions_'+ i +'"> ' + data[i].fields.name + '</label></li>';
       }
       django.jQuery("ul#id_positions").html(checkboxes);
       django.jQuery("div.field-positions").show();
   });
}

(function($){
    $(function(){
        if (typeof POINT_OBJECT !== 'undefined' && POINT_OBJECT.position_type > 1) {
            getPositions(POINT_OBJECT.position_type);
        }
        else {
            $("div.field-positions").hide();
        }
    });
    $(document).on('change', 'select#id_point_type', function(){
       let position_type = $(this).val();
       if (position_type > 1){
           getPositions(position_type);
       }
       else {
           $("div.field-positions").hide();
       }
    });
})(django.jQuery);