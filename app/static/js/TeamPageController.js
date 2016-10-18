app.controller('TeamPageController', function ($scope, $http, $modal) {
    $scope._urls = {};

    $scope.team = null;
    $scope.roles = [];
    $scope.members = [];
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
        $http.get($scope._urls.members)
            .success(function (data) {
                $scope.members = data.entries;
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
                    $modalInstance.close($scope.role);
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

    $scope.assignRole = function(index){
        $scope.edited_role = $scope.roles[index];
        $scope._openAssignModal();
    };

    $scope._openAssignModal = function () {
        var params = {
            templateUrl: '_assignees_modal.html',
            resolve: {
                role: function() {
                    return angular.copy($scope.edited_role);
                },
                members: function(){
                    return $scope.members;
                }
            },
            controller: function ($scope, $modalInstance, role, members) {
                $scope.role = role;
                $scope.members = members;
                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
                $scope.save = function () {
                    $scope.role.members_ids = $scope.members.filter(function(member){
                        return member.roles.indexOf($scope.role.id) !== -1;
                    }).map(function(member){
                        return member.user.id;
                    });
                    $modalInstance.close($scope.role);
                };
            }
        };
        var modalInstance = $modal.open(params);
        modalInstance.result.then(function (role) {
            $scope.edited_role = role;
            $scope.saveRole();
        }, function () {
            $scope.edited_role = {};
            console.log('canceled')
        });
    };

    $scope.isAssignedRole = function(index){
        var role = $scope.roles[index];
        return $scope.members.filter(function(member){
                return member.roles.indexOf(role.id) !== -1;
            }).length > 0;
    }

});