$(document).ready(function () {
    $('.search-box').focus(function (event) {
        this.selectionStart = this.selectionEnd = this.value.length;
    }).focus();

    var t = getUrlParameter('t') || 'match';
    $('#' + t).removeClass('btn-default').addClass('btn-info').addClass('selected');

    $('.copy-button').each(function () {
        var client = new ZeroClipboard($(this));
    });
});

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

var app = angular.module("app", [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller("getDomainCtrl", function ($scope, $http) {
    $scope.domain = "domain";
    $scope.machineList = [
        {
            "name": "chn-yawen",
            "discovered_time": 'now'
        }
    ];
    $scope.getCurrentDomain = function () {
        $http.get('api/v1/get-current-domain').success(function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                $scope.domain = data.domain;
            }
        });
    };
    $scope.getMachineList = function () {
        $http.get('api/v1/get-machine-list').success(function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                $scope.machineList = data.machineList;
            }
        });
    };
});

app.controller("indexSearchCtrl", function ($scope) {
    $scope.searchType = 'match';
    $scope.search = function () {
        // console.log($(event));
        if ($(event.target).hasClass('btn')) {
            var q = $('.search-box').val();
            $('.search-type').removeClass('btn-info').addClass('btn-default');
            $(event.target).addClass('btn-info');
            $scope.searchType = $(event.target).attr('id');
            if (q) {
                window.location.href = 'search?q=' + q + '&t=' + $scope.searchType;
            }
        }
        else if ($(event.target).hasClass('search-box')) {
            if (event.keyCode == 13) {
                window.location.href = 'search?q=' + $('.search-box').val() + '&t=' + $scope.searchType;
            }
        }
    };
});