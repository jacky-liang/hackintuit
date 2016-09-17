$(document).ready(function(){

    var submit_btn = $('#submit');

    submit_btn.click(function(){

        var age = $('#age').val();
        var sex = $('#sex').val();
        var mar = $('#mar').val();
        var ind = $('#ind').val();
        var loc = $('#loc').val();

        // use $.get to send http request to url?age=&sex=
        $.get('https://8e22f0d3.ngrok.io/salaries', { "age": age, "sex": sex, "mar": mar, "ind": ind, "loc": loc, "x": 5 }, function(res){
          $('#info').html(res);
        })


    })

})
