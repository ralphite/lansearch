$(document).ready(function () {
    $('#search form, #results form').submit(function (event) {
        if ($.trim($('.searchbox').val()).length > 0) {
            return true;
        }
        return false;
    });

    $('.searchbox').focus(function (event) {
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

var search = function () {
    var q = $('.searchbox').val();
    window.location.href = 'search?q=' + q + '&t=' + $(event.target).attr('id');
};

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
        },
        {
            "name": "chn-yawen2",
            "discovered_time": 'now1'
        },
        {
            "name": "chn-yawen3",
            "discovered_time": 'now2'
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