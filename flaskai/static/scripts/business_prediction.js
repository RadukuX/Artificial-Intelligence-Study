$(document).ready(function(){
    $('#search-team-b').on("input", function(e){
        myTeam = $('#search-team-b').val()
        $.ajax({
            type: 'POST',
            url: '/livesearch-business',
            data: {myTeam: myTeam},
            success: function(response){
                var rawTeam = String(response).replace("_", " ")
                var opponentTitle = $('<h4 id="your_team" class="opponent-title-prediction">' + rawTeam.toUpperCase()+ '</h4>')
                $('#team-b').empty().append(opponentTitle).html
            },
            error: function(error){
                console.log(error)
            }
        })
    })
})

$(document).ready(function(){
    $("#knn_button").click(function(event){
        event.preventDefault()
        event.stopPropagation()
//        var rawTeam = $("#team-b").text().toLowerCase()
//        var myTeam = rawTeam.replace(" ","_")
        var investments = $("#investments").val()
        var medAge = $("#med_age").val()
        var wins = $("#wins").val()
        var equals = $("#equals").val()
        var defeats = $("#defeats").val()
        var goals = $("#goals").val()
        $.ajax({
            type: 'POST',
            url: '/knn',
            data: {investments: investments, medAge: medAge, wins: wins, equals: equals, defeats: defeats, goals: goals},
            success: function(response){
                var result = response[0]
                var accuarcy = response[1]
                var info_place = $('<p> K nearest neighbour result: ' + result + ' </p>')
                var info_accuarcy = $('<p>Accuarcy of KNN: ' + accuarcy + ' %</p>')
                var info = $('<div id="inf" > </div>')
                $("#knn_info").empty().append(info).html
                $("#inf").append(info_place).html               
                $("#inf").append(info_accuarcy).html
            },  
            error: function(error){
                console.log(error)
            }
        })
    })
})

$(document).ready(function(){
    $("#linear_button").click(function(event){
        event.preventDefault()
        event.stopPropagation()
//        var rawTeam = $("#team-b").text().toLowerCase()
//        var myTeam = rawTeam.replace(" ","_")
        var investments = $("#investments").val()
        var medAge = $("#med_age").val()
        var wins = $("#wins").val()
        var equals = $("#equals").val()
        var defeats = $("#defeats").val()
        var goals = $("#goals").val()
        $.ajax({
            type: 'POST',
            url: '/linear',
            data: {investments: investments, medAge: medAge, wins: wins, equals: equals, defeats: defeats, goals: goals},
            success: function(response){
                var place = response['result']
                var info_place = $('<p class="linear-info"> Linear Regression result: ' + place.toFixed(1) + ' </p>')
                $("#linear_info").empty().append(info_place).html
            },   
            error: function(error){
                console.log(error)
            }
        })
    })
})