$.ajaxSetup({
  cache:false
}); // This causes browser to not cache to ajax calls so it can call it when the page reloads

$( "#dt" ).datepicker();

$( "#hire_date" ).datepicker();

$( "#start_date" ).datepicker();

$( "#end_date" ).datepicker();

$( "#order_date" ).datepicker();

// Basically disables Chrome's default datepicker on a date field
$( "#hire_date" ).attr("type", "text");
$( "#start_date" ).attr("type", "text");
$( "#end_date" ).attr("type", "text");
$( "#order_date" ).attr("type", "text");

$(function() {
var $store_list = $('#store_list');
var $employee_list = $('#employee_list');
var $job_list = $('#job_list');
var $select_box = $('#selector');
var $list = $('#list');
var $job_details = $('#job_details');

// Select box on View Info page
$select_box.change(function() {
    if ($select_box.val() == 'employee') {
        $.getJSON('static/data/employees.json', function(response) {
            var table_HTML = '<table><thead><tr><td>Name</td><td>Address</td><td>Work Level</td></tr></thead>';
            $.each(response, function(index, employee) {
                table_HTML += '<tr><td>' + employee.name + '</td>';
                table_HTML += '<td>' + employee.address + '</td>';
                table_HTML += '<td>' + employee.work_level + '</td></tr>';
            });
            table_HTML += '</table>';
            $list.html(table_HTML);
        });
    } else if ($select_box.val() == 'store') {
        $.getJSON('static/data/stores.json', function(response) {
            var table_HTML = '<table><thead><tr><td>Name</td><td>Number</td><td>Address</td><td></td></tr></thead>';
            $.each(response, function(index, store) {
                table_HTML += '<tr><td>' + store.retailer.name + '</td>';
                table_HTML += '<td>' + store.store_num + '</td>';
                table_HTML += '<td>' + store.address + '</td>';
                table_HTML += '<td><a href="/store' + store.id_num + '">Details</a></td></tr>';
            });
            table_HTML += '</table>';
            $list.html(table_HTML);
        });
    } else if ($select_box.val() == 'job') {
        var assigned;
        $.getJSON('static/data/jobs.json', function(response) {
            var table_HTML = '<table><thead><tr><td>Retailer</td><td>Client</td><td>Required Level</td>';
            table_HTML += '<td>Assigned Rep</td><td></td></tr></thead>';
            $.each(response, function(index, job) {
                table_HTML += '<tr><td>' + job.names.store_name + '</td>';
                table_HTML += '<td>' + job.names.client + '</td>';
                table_HTML += '<td>' + job.values.required_level + '</td>';
                if (job.assigned_reps.assigned === null) {
                    table_HTML += '<td>Not Assigned</td>';
                } else {
                    table_HTML += '<td>' + job.assigned_reps.assigned + '</td>';
                };
                table_HTML += '<td><a href="/job' + job.values.job_id + '">Details</a></td></tr>';
            });
            table_HTML += '</table>';
            $list.html(table_HTML);
        });
    } else if ($select_box.val() == '0') {
        $list.html('<p>Please select a category</p>');
    }
});

// Add Job Page
var $retailer = $('#retailer');
var $client = $('#client');
var $store = $('#store');

$store.html('<option value="0">Select a retailer first</option>');
$retailer.change(function() {
    if ($retailer.val() === '0') {
        $store.html('<option value="0">Select a retailer first</option>');
    } else {
        $.getJSON('static/data/stores.json', function(response) {
            var store_HTML = '<option value="0">Select a retailer</option>';
            $.each(response, function(index, store) {
                if (store.retailer.id.toString() === $retailer.val().toString()) {
                    store_HTML += '<option value="' + store.id_num;
                    store_HTML += '">' + store.store_num + ": " + store.address;
                    store_HTML += '</option>';
                }
            });
            $store.html(store_HTML);
        });
    }
});

// New Part Order Page: Client to part
var $p_client = $('#p_client');
var $part_id = $('#part_id');
$part_id.html('<option value="0">Select a client first</option>');
$p_client.change(function() {
    if ($p_client.val() === '0') {
        $part_id.html('<option value="0">Select a client first</option>');
    } else {
        $.getJSON('../static/data/parts.json', function(response) {
            var parts_HTML = '<option value="0">Select a part</option>';
            $.each(response, function(index, part) {
                if (part.client.toString() === $p_client.val().toString()) {
                    parts_HTML += '<option value="' + part.id;
                    parts_HTML += '">' + part.part_number + ": " + part.description;
                    parts_HTML += '</option>';
                }
            });
            $part_id.html(parts_HTML);
        });
    }
});

// New Part Order Page: retailer
var $p_retailer = $('#p_retailer');
var $p_store = $('#p_store');

$p_store.html('<option value="0">Select a retailer first</option>');
$p_retailer.change(function() {
    if ($p_retailer.val() === '0') {
        $p_store.html('<option value="0">Select a retailer first</option>');
    } else {
        $.getJSON('../static/data/stores.json', function(response) {
            var store_HTML = '<option value="0">Select a retailer</option>';
            $.each(response, function(index, store) {
                if (store.retailer.id.toString() === $p_retailer.val().toString()) {
                    store_HTML += '<option value="' + store.id_num;
                    store_HTML += '">' + store.store_num + ": " + store.address;
                    store_HTML += '</option>';
                }
            });
            $p_store.html(store_HTML);
        });
    }
});



// Here begins the compare distances page
var $store_select = $('#store_select');
var $emp_select = $('#emp_select');

// put data into select boxes
$.getJSON('static/data/stores.json', function(response) {
    var store_add_HTML = '<option value="401 Main Street Johnstown, PA 15901">City Hall</option>';
    $.each(response, function(index, store) {
        store_add_HTML += '<option value="' + store.address + '">';
        store_add_HTML += store.retailer.name + ' ' + store.store_num + '</option>';
    });
    $store_select.html(store_add_HTML);
});
$.getJSON('static/data/employees.json', function(response) {
    var store_add_HTML = '<option value="401 Main Street Johnstown, PA 15901">City Hall</option>';
    $.each(response, function(index, emp) {
        store_add_HTML += '<option value="' + emp.address + '">';
        store_add_HTML += emp.name + '</option>';
    });
    $emp_select.html(store_add_HTML);
});


$store_select.change(function() {
    initMap($emp_select.val(), $store_select.val());
});


$emp_select.change(function() {
    initMap($emp_select.val(), $store_select.val());
});


// Compare Distances
// Trying it myself
function initMap(emp_add, store_add) {
    var bounds = new google.maps.LatLngBounds;
    var markersArray = [];

    var origin1 = emp_add;
    var destinationA = store_add;

    var destinationIcon = 'https://chart.googleapis.com/chart?' +
        'chst=d_map_pin_letter&chld=D|FF0000|000000';
    var originIcon = 'https://chart.googleapis.com/chart?' +
        'chst=d_map_pin_letter&chld=O|FFFF00|000000';
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 55.53, lng: 9.4},
        zoom: 10
    });
    var geocoder = new google.maps.Geocoder;

    var service = new google.maps.DistanceMatrixService;
    service.getDistanceMatrix({
    origins: [origin1],
    destinations: [destinationA],
    travelMode: 'DRIVING',
    unitSystem: google.maps.UnitSystem.IMPERIAL,
    avoidHighways: false,
    avoidTolls: false
    }, function(response, status) {
        if (status !== 'OK') {
            alert('Error was: ' + status);
        } else {
            var originList = response.originAddresses;
            var destinationList = response.destinationAddresses;
            var outputDiv = document.getElementById('output');
            outputDiv.innerHTML = '';
            deleteMarkers(markersArray);

            var showGeocodedAddressOnMap = function(asDestination) {
                var icon = asDestination ? destinationIcon : originIcon;
                return function(results, status) {
                if (status === 'OK') {
                    map.fitBounds(bounds.extend(results[0].geometry.location));
                    markersArray.push(new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        icon: icon
                    }));
                } else {
                  alert('Geocode was not successful due to: ' + status);
                }
              };
            };

            for (var i = 0; i < originList.length; i++) {
              var results = response.rows[i].elements;
              geocoder.geocode({'address': originList[i]},
                  showGeocodedAddressOnMap(false));
              for (var j = 0; j < results.length; j++) {
                geocoder.geocode({'address': destinationList[j]},
                    showGeocodedAddressOnMap(true));
                outputDiv.innerHTML += originList[i] + ' to ' + destinationList[j] +
                    '<br>Distance: ' + results[j].distance.text + '<br>Time: ' +
                    results[j].duration.text + '<br>';
              }
            }
          }
        });
      }

      function deleteMarkers(markersArray) {
        for (var i = 0; i < markersArray.length; i++) {
          markersArray[i].setMap(null);
        }
        markersArray = [];
      }

});