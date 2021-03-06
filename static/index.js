// Handle the calls to request and any javascript necessary.

var hotlight;

function load_results(response) {
  console.log(response);
  console.log(response[0]);
  //Process variable
  var isLightOn = response[0].Location.Hotlight;
  document.getElementById("output").innerHTML = isLightOn ? "Hot right now!" : "Not hot right now :(";
  
  // Set Image
  var image_string = isLightOn ? 'hot_krispy_kreme.png' : 'off_krispy_kreme.png';
  document.getElementById("light").src = '/static/assets/'+image_string;

  // Set form
  if(!isLightOn){
    $('#form').css("display", "inline");
  }
  else{
    $('#form').css("display","none");
  }

  // Update Database
  updateHotLightDatabase(isLightOn);

  // Get Lat/Long of user location
  var latitude = response[0].Location.Latitude;
  var longitude = response[0].Location.Longitude;
  update_map(latitude, longitude);
};

function processForm(e) {
  e.preventDefault();
  var phone = $('#phone').val();

  $.post('/api/phone', {
    'phone': phone
  }).done(function(response){
    console.log(response);
    if(response['success']){
        $('#form-failure').css("display", "none");
      $('#form').css("display","none");
      $('#form-success').css("display", "inline");
    }
    else{
      $('#phone-parent').addClass('error');
      $('#form-failure').css("display", "inline");
    }
  }).fail(function(){
    alert('Server error');
  });

  return true;
}

function updateHotLightDatabase(isLightOn) {
  hot = isLightOn ? 'True' : 'False';
  $.post('/api/update_hotlight', {
    'timestamp': Date.now(),
    'hot': hot
  });
}

form = document.getElementById('form');
if (form.attachEvent) {
  form.attachEvent("submit", processForm);
}
else {
  form.addEventListener("submit", processForm);
}

function update_map(latitude, longitude) {
  // Follow format http://maps.google.com/?q=[lat],[long]
  $('#map').attr('data-url', "http://maps.google.com/?q=" + latitude + "," + longitude);
}

var tag = document.createElement("script");
tag.src = 'https://services.krispykreme.com/api/locationsearchresult/?callback=load_results&responseType=Full&search=%7B%22Where%22%3A%7B%22LocationTypes%22%3A%5B%22Store%22%2C%22Commissary%22%2C%22Franchise%22%5D%2C%22OpeningDate%22%3A%7B%22ComparisonType%22%3A0%7D%7D%2C%22Take%22%3A%7B%22Min%22%3A3%2C%22DistanceRadius%22%3A100%7D%2C%22PropertyFilters%22%3A%7B%22Attributes%22%3A%5B%22FoursquareVenueId%22%2C%22OpeningType%22%5D%7D%7D&lat=29.6516344&lng=-82.32482619999996&_=1517112369718';

document.getElementsByTagName("head")[0].appendChild(tag);

// DOCUMENTATION
/*

  console.log(response); // array of all locations  
  console.log(response[0]);

  Responds with
  
  "Location": {
            "Id": 100,
            "LocationNumber": 440,
            "Name": "Gainesville",
            "Slug": "gainesville",
            "DetailUrl": "http://krispykreme.com/location/gainesville",
            "LocationType": "Franchise",
            "Address1": "306 NW 13th Street",
            "Address2": null,
            "City": "Gainesville",
            "Province": "FL",
            "PostalCode": "32601",
            "Country": "US",
            "PhoneNumber": "(352) 377-0052",
            "Latitude": 29.653956,
            "Longitude": -82.339244,
            "FundraisingType": "Online",
            "Hotlight": true,
            "OffersCoffee": false,
            "OffersWifi": false,
            "ExtendedDetails": {
                "Description": "",
                "Message": "Hot Light Hours may vary by day and day of week.&nbsp;"
            },
            "Attributes": {},
            "LocationHours": {
                "Store Hours": [
                    {
                        "DaysOfWeek": 127,
                        "DaysOfWeekAlias": "Sun-Sat",
                        "Times": [
                            {
                                "StartTime": "00:00:00",
                                "EndTime": "00:00:00"
                            }
                        ]
                    }
                ],
                "Drive-Thru Hours": [
                    {
                        "DaysOfWeek": 127,
                        "DaysOfWeekAlias": "Sun-Sat",
                        "Times": [
                            {
                                "StartTime": "00:00:00",
                                "EndTime": "00:00:00"
                            }
                        ]
                    }
                ],
                "Hot Light Hours": [
                    {
                        "DaysOfWeek": 127,
                        "DaysOfWeekAlias": "Sun-Sat",
                        "Times": [
                            {
                                "StartTime": "06:00:00",
                                "EndTime": "11:00:00"
                            },
                            {
                                "StartTime": "18:00:00",
                                "EndTime": "23:00:00"
                            }
                        ]
                    }
                ]
            },
            "OpeningDate": null,
            "OpeningDateTBD": false
        },
        "Distance": 0.88120944562769832
    },
  */