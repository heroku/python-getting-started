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


app.controller('TeamPageController', function ($scope, $http, $modal) {
    $scope._urls = {};

    $scope.team = null;
    $scope.roles = [];
    $scope.edited_role = {};


    $scope.init = function (urls) {
        $scope._urls = urls;

        // TODO: handle error statuses
        $http.get($scope._urls.team)
            .success(function (data) {
                $scope.team = data;
            });
        $http.get($scope._urls.roles)
            .success(function (data) {
                $scope.roles = data.entries;
            });
    };

    $scope.editRole = function (index) {
        $scope.edited_role = $scope.roles[index];
        $scope._openRoleModal();
    };

    $scope.createRole = function () {
        $scope.edited_role = {};
        $scope._openRoleModal();
    };

    $scope.saveRole = function () {
        $http.post($scope._urls.roles, $scope.edited_role)
            .success(function(_role){
                var existed = false;
                $scope.roles = $scope.roles.map(function(role){
                    if(role.id === _role.id){
                        existed = true;
                        return _role;
                    }
                    return role;
                });
                if(!existed){
                    $scope.roles.push(_role);
                }
            });
    };

    $scope.deleteRole = function (index) {
        if (!confirm('The role will be deleted')) {
            return null;
        }
        $http.delete($scope._urls.roles + '?role_id=' + $scope.roles[index].id);
        $scope.roles.splice(index, 1);
    };

    $scope._openRoleModal = function () {
        var params = {
            templateUrl: '_role_modal.html',
            resolve: {
                role: function() {
                    return angular.copy($scope.edited_role);
                }
            },
            controller: function ($scope, $modalInstance, role) {
                $scope.role = role;
                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
                $scope.save = function () {
                    $modalInstance.close(role);
                };
            }
        };
        var modalInstance = $modal.open(params);
        modalInstance.result.then(function (role) {
            $scope.edited_role = role;
            $scope.saveRole();
        }, function (role) {
            $scope.edited_role = {};
            console.log('canceled')
        });
    };

});