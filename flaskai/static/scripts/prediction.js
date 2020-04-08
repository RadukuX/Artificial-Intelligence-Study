$(document).ready(function(){
    var teamName =  localStorage.getItem('team-name')
    var teamTitle = $('<h1 id="my_team" class="team-title-prediction">' + teamName + ' vs </h1>')
    $('#title_team').append(teamTitle).html
})

$(document).ready(function(){
    var teamName = localStorage.getItem('team-name')
    $('#search-team').on("input", function(e){
        op = $('#search-team').val()
        $.ajax({
            type: 'POST',
            url: '/livesearch',
            data: {myTeam: teamName.toLowerCase(), opponent:op},
            success: function(response){
                var opponentTeam = response[0][0]
                var opponentTitle = $('<h1 id="opponent_team" class="opponent-title-prediction">' + opponentTeam + '</h1>')
                $('#opponent-team').empty().append(opponentTitle).html
            },
            error: function(error){
                console.log(error)
            }
        })
    })
})

$(document).ready(function(){
    $('#markov_button').click(function(event){
        var myTeam = $("#my_team").text().replace(" vs", "")
        var opponentTeam = $("#opponent_team").text()
        console.log(myTeam)
        console.log(opponentTeam)
        $.ajax({
            type: 'POST',
            url: '/markov/informations',
            data: {team1: myTeam.replace(" ", ""), team2: opponentTeam},
            success: function(response){
                console.log(response)
                var markovForm = $('<form id="markov_form"><fieldset id="markov_fieldset"> </fieldset></form>')
                var lastResultVictory = $('<label id="victory_btn" class="radio-inline"><input class="rad-btn" type="radio" name="optradio" checked> Victory </label>')
                var lastResultEqual = $('<label id="equal_btn" class="radio-inline"><input class="rad-btn" type="radio" name="optradio" checked> Equal </label>')
                var lastResultDefeat = $('<label id="defeat_btn" class="radio-inline"><input class="rad-btn" type="radio" name="optradio" checked> Defeat </label>')
                var power = $('<div class="form-group"><label for="power">Nr of tests</label><input id="power" type="number" class="form-control"> </div>')
                var submitButton = $('<button id="calc_prob_matrix" type="button" onclick="probMatrix(); markovMatrix();" class="btn btn-primary">Calculate</button>')
                $("#markov_chains_option").empty().append(markovForm).html
                $("#markov_fieldset").append(lastResultVictory).html
                $("#markov_fieldset").append(lastResultEqual).html
                $("#markov_fieldset").append(lastResultDefeat).html
                $("#markov_fieldset").append(power).html
                $("#markov_fieldset").append(submitButton).html

            },
            error: function(error){
                console.log(error)
            }
        })
        event.preventDefault()
        event.stopPropagation()
    })
})

function probMatrix(){
    var myTeam = $("#my_team").text().replace(" vs", "")
    var opponentTeam = $("#opponent_team").text()
    var rawResult = $("input[name='optradio']:checked").parent('label').text();
    var result = rawResult.replace(" ", "")
    var lastResult = result.charAt(0).toLowerCase()
    var power = $('#power').val()
    console.log(myTeam)
    console.log(opponentTeam)
    console.log(lastResult)
    console.log(power)
    $.ajax({
        type: 'POST',
        url: '/markov/probability-matrix',
        data: { team1: myTeam.replace(" ", ""), team2: opponentTeam, lastResult: lastResult, power: power},
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
    event.preventDefault()
    event.stopPropagation()
}

function markovMatrix(){
    var myTeam = $("#my_team").text().replace(" vs", "")
    var team = myTeam.replace(" ", "")
    var opponentTeam = $("#opponent_team").text()
    console.log(opponentTeam)
    $.ajax({
        type: 'POST',
        url: '/markov/matrix',
        data: {team1: team, team2: opponentTeam},
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
}

function bayes(){
    var myTeam = $("#my_team").text().replace(" vs", "")
    var team = myTeam.replace(" ", "")
    var opponent = $("#opponent_team").text()
    $.ajax({
        type: 'POST',
        url: '/bayes/calculate',
        data: {team1: team, team2: opponent},
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
}