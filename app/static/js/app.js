var app = angular.module('teamedUp', []);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);


app.controller('TeamPageController', function($scope, $http){
    $scope._urls = {};

    $scope.team = null;
    $scope.roles = [];

    $scope.init = function(urls){
        $scope._urls = urls;

        // TODO: handle error statuses
        $http.get($scope._urls.team)
            .success(function(data){
                $scope.team = data;
            })
        $http.get($scope._urls.roles)
            .success(function(data){
                console.log(data);
            });
    }

});