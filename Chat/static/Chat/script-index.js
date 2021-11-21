$(document).ready(function () {
    $("#set").click(function () {
        var name = $("#name").val();
        window.location.pathname = '/chat/' + name + '/';
    })
});