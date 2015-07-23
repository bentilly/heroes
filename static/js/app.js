$(function () {
    var config = {};
    console.log('heeeeelo')
    $.get('/users/config/', function (data) {
        config = data;
        if (!config.user_id) {
            $('#login').attr('href', config.login_url)
        }
    })
});
