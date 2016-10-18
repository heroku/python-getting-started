app.controller('NotificationsPageController', function ($scope, $http) { // TODO: rename controller to NotificationsController
    $scope._urls = {};
    $scope.entries = [];
    $scope.total = 0;
    $scope._page = 0;

    $scope.init = function(urls){
        $scope._urls = urls;
        $scope.load();
    };

    $scope.load = function(){
        $scope._page += 1;
        $http.get($scope._urls.notifications + '?page=' + $scope._page)
            .success(function(data){
                $scope.entries = data.entries;
                $scope.total = data.total;
            });
    };

    $scope.post = function(url, index){
        // TODO:
        // This approach is only viable during MVC.
        // The notifications system should be greatly improved before going "live".
        $http.post(url);
        $scope.entries.splice(index, 1);
    }
});