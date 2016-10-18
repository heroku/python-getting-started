var app = angular.module('teamedUp', ['mm.foundation']);

app.directive('fDatepicker', function () {
    return {
        link: function(scope, element, attrs){
            $(element).fdatepicker({
                'pickTime': true,
                'format': 'mm-dd-yyyy hh:ii',
                'disableDblClickSelection': true
            });
        }
    }
});


app.config(['$interpolateProvider', '$httpProvider', function ($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $httpProvider.defaults.headers.common['X-CSRFToken'] = (function (cname) {
        var cookie_data = document.cookie.match(cname + '=[^;]*');
        return cookie_data == null ? null : cookie_data[0].split('=')[1];
    })('csrftoken');
}]);


