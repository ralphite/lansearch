$(document).ready(function () {
    $('.search-box').focus();

    var t = getUrlParameter('t') || 'match';
    $('#' + t).removeClass('btn-default').addClass('btn-info').addClass('selected');
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

// make the size originally in bytes to human readable
angular.module('filters', []).filter('sizeFilter', function () {
    return function (input) {
        if (input < 1024)
            return input.toString() + ' Bytes';
        input /= 1024;
        if (input < 1024)
            return input.toPrecision(4).toString() + ' KB';
        input /= 1024;
        if (input < 1024)
            return input.toPrecision(4).toString() + ' MB';
        input /= 1024;
        if (input < 1024)
            return input.toPrecision(4).toString() + ' GB';
        input /= 1024;
        return input.toPrecision(4).toString() + ' TB';
    };
});

var app = angular.module("app", ['angularSpinner', 'filters'], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.directive('resultTable', function () {
    return function (scope, element, attrs) {
        scope.$watch('searchResult', function (value) {
            var val = value || null;
            if (val) {
                // this will run after ng table is populated
                // to make copy buttons
                $('.copy-button').each(function () {
                    var client = new ZeroClipboard($(this));
                });
            }
        });
    };
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
    $scope.indexSearch = function () {
        var searchBox = $('#search-box');
        var q = $.trim(searchBox.val());
        if ($(event.target).hasClass('btn')) {
            $('.search-type').removeClass('btn-info').addClass('btn-default');
            $(event.target).addClass('btn-info');
            $scope.searchType = $(event.target).attr('id');
            if (q) {
                window.location.href = 'search?q=' + q + '&t=' + $scope.searchType;
            } else {
                searchBox.val('');
            }
        }
        else {
            if (event.keyCode == 13) {
                window.location.href = 'search?q=' + q + '&t=' + $scope.searchType;
            }
        }
    };
});

app.controller("searchCtrl", ['$scope', '$http', 'usSpinnerService',
    function ($scope, $http, usSpinnerService) {
        $scope.searchType = getUrlParameter('t') || 'match';
        $scope.searchResult = {};
        $scope.itemsPerPage = 20;
        $scope.page = 1;
        $scope.pages = {};
        var get = function (url) {
            // start spinner before the heavy http get
            usSpinnerService.spin('spinner-1');
            $http.get(url).success(
                function (data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        $scope.searchResult = data.searchResult;
                        $scope.itemsPerPage = data.itemsPerPage;
                        $scope.page = data.offset;
                        $scope.pages = data.pages;
                    }
                    // stop spinner when success
                    // spinner might not stop if error
                    usSpinnerService.stop('spinner-1');
                }
            );
        };
        $scope.search = function () {
            var q = $.trim($('#search-box').val());
            if ($(event.target).hasClass('btn')) {
                $('.search-type').removeClass('btn-info').addClass('btn-default');
                $(event.target).addClass('btn-info');
                $scope.searchType = $(event.target).attr('id');
                if (q) {
                    get('/api/v1/' + 'search?q=' + q + '&t=' + $scope.searchType);
                }
            }
            else if ($(event.target).hasClass('page')) {
                if ($(event.target).hasClass('click')) {
                    var page = $(event.target).text();
                    var p;
                    if (page === '<<') p = 1;
                    else if (page === '<') p = $scope.page - 1;
                    else if (page === '>') p = $scope.page + 1;
                    else if (page === '>>') {
                        p = Number(($scope.searchResult['hits']['total']
                            / $scope.itemsPerPage).toFixed());
                    }
                    else {
                        p = Number(page);
                    }
                    var url = '/api/v1/' + 'search?q=' + q + '&t=' + $scope.searchType + '&p=' + p.toString();
                    get(url);
                }
            }
            else {
                if (event.keyCode == 13) {
                    if (q) get('/api/v1/' + 'search?q=' + q + '&t=' + $scope.searchType);
                }
            }
        };
    }]);