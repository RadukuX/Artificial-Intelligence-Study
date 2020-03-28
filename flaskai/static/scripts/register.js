
function getSelectValues() {
    var result = [];
    var select = document.getElementById('selectbox');

    var options = select;
    var opt;

    for (var i=0, iLen=options.length; i<iLen; i++) {
        opt = options[i];
        if (opt.selected) {
            result.push(opt.value);
        }
    }
    return result;
}

$(document).ready(function(){
    $(".selection-class").click(function(){
        values = getSelectValues()
        $("#team_list")
            .html($("<li class='list-group-item selected-teams'>" + values + "</li>"));
    });
});


$(document).ready(function() {
    var arr = new Array();
    $("select[multiple]").change(function() {
        $(this).find("option:selected")
        if ($(this).find("option:selected").length > 3) {
            $(this).find("option").removeAttr("selected");
            $(this).val(arr);
            alert("You can only choose 3 teams! For more teams you have to pay")
        }
        else {
            arr = new Array();
            $(this).find("option:selected").each(function(index, item) {
                arr.push($(item).val());
            });
            
        }
    });
});

$(function(){
    $("#register-button").click(function(){
        var send_result = getSelectValues()
        console.log(JSON.stringify({result:  send_result }))
        $.ajax({
            type: "POST",
            url:"http://localhost:5000/register",
            data: JSON.stringify({result:  send_result }),
            contentType: 'application/json;charset=UTF-8'
        })
        
    })
})