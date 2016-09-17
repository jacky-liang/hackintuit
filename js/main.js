$(document).ready(function(){

    var submit_btn = $('#submit');

    submit_btn.click(function(){
        var age = $('#age').val();
        var sex = $('#sex').val();
        var mar = $('#mar').val();
        var ind = $('#ind').val();
        var loc = $('#loc').val();

        $.get('https://8e22f0d3.ngrok.io/salaries', { "age": age, "sex": sex, "mar": mar, "ind": ind, "loc": loc, "x": 5 }, function(res){
          console.log(res);
          $('#info').html(res);
          $('#salary').html(res['salary'])
          $('#con_hardship').html(res['con_hardship'])
          $('#con_price').html(res['con_price'])
          $('#house_hardship').html(res['house_hardship'])
          $('#sfr_price').html(res['sfr_price'])
          $('#time_to_con').html(res['time_to_con'])
          $('#time_to_house').html(res['time_to_house'])
        })

    })

})
