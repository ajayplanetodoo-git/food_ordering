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

//  this function work for addinge product in cart without refress
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