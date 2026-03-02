// requireed api for auto complte ✅ Maps JavaScript API

// ✅ Places API

let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields

    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address},function(results,status){
        if (status==google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $("#id_latitude").val(latitude);
            $("#id_longitude").val(longitude);
            $("#id_address").val(address);


        }
    });
    // loop through all adress componet like city place area etc ..
    console.log(place.address_components)
    for(var i=0; i<place.address_components.length;i++){
        for(var j=0; j<place.address_components[i].types.length;j++){
            // get country
            if(place.address_components[i].types[j]=='country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j]=='administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            
            // get_city
            if(place.address_components[i].types[j]=='locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode

            if(place.address_components[i].types[j]=='postal_code'){
                $('#id_pincode').val(place.address_components[i].long_name);
            }else{
                $('#id_pincode').val("");
            }

        }
    }
}

//  this function work for addinge product in cart without refresh
$(document).ready(function(){
// real time show qty increamwnt and cart no 
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        
        let url = $(this).data('url');
       
        $.ajax({
            type:'GET',
            url : url,
            // data : data,
            success : function(response){
                console.log(response)
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+response.food_id).html(response.qty)
            }
        })

      
    })
// decrease cart and other things
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        
        let url = $(this).data('url');
       
        $.ajax({
            type:'GET',
            url : url,
            // data : data,
            success : function(response){
                console.log(response)
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+response.food_id).html(response.qty)
            }
        })

      
    })
})  

$(document).on('click', '.delete_cart', function (e) {
    e.preventDefault();

    let url = $(this).data('url');
    let cartId = $(this).data('id');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {

            if (response.status === 'success') {

                // Remove cart row instantly
                $('#cart-row-' + cartId).fadeOut(300, function () {
                    $(this).remove();
                });

                // Update cart counter
                $('#cart_counter').html(response.cart_counter.cart_count);

                // Empty cart check
                if (response.cart_counter.cart_count === 0) {
                    $('.cart-list').html('<h5>Cart is empty</h5>');
                }
            }
        }
    });
});

// add hours js . 1st  it will hit class name which i assinged  in button 
$(document).on('click', '.add_hour', function (e) {
    e.preventDefault();
    var day = document.getElementById('id_day').value // if you not assinged any id key in html  js defaul give it a id like id_day etc
    var from_hour = document.getElementById('id_from_hour').value 
    var to_hour = document.getElementById('id_to_hour').value 
    var is_closed = document.getElementById('id_is_closed').checked
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
    var url = document.getElementById('add_hours_url').value // here we define id separty so js not assinged it default

    if(is_closed){
        is_closed = "True"
        condition = " day != '' "
    }else{
        is_closed="False"
        condition = " day != '' && from_hour != '' && to_hour != '' "
    }
// this responsible for sending request or naything to django becoze url come in action here 
    if(eval(condition)){
        $.ajax({
            type:'POST',
            url : url,
            data : {
                'day':day,
                'from_hour':from_hour,
                'to_hour':to_hour,
                'is_closed':is_closed,
                'csrfmiddlewaretoken':csrf_token,
            },
            success:function(response){
                if(response.status=='success'){
                    if(response.is_closed=='Closed'){
                        // here we are making html for append in html table  
                        html = '<tr id="hour-'+response.id +'"><td><b>'+ response.day +'</b></td><td>Closed</td><td><a href="#" class="remove_hours" data-url="/vendor/opening-hours/remove/'+response.id +'/">Remove</a></td></tr>';
                    }else{
                        html = '<tr id="hour-'+response.id +'"><td><b>'+ response.day +'</b></td><td>'+ response.from_hour +'  '+ response.to_hour + '</td><td><a href="#" class="remove_hours" data-url="/vendor/opening-hours/remove/'+response.id +'/">Remove</a></td></tr>';

                    }
                    
                    $('.opening_hours_table').append(html)
                    document.getElementById('opening_hours').reset();
                }
            }
        })
    }else{
        alert("Please filled every fields")
        
    }

    console.log(day,from_hour,to_hour,is_closed,csrf_token)

});
// for removing hours

$(document).on('click', '.remove_hours', function (e) {
    e.preventDefault()
    // url = document.getElementById('remove_opening_hours') this kind of getting url used when it fixed not have any id alway fixed url we used like this
    url = $(this).attr('data-url'); // when url are not fix change very time then used this type approche here url also have id which is change very time
    console.log(url)
    $.ajax({
      type:'GET',
      url : url,
      success : function(response){
        if(response.status=='success'){
            document.getElementById('hour-'+response.id).remove()
            
        }
    }  
    })

});