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

var wins_pie = 0
var defeats_pie = 0
var equals_pie = 0

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
                totalWins = response[0].wins
                totalDefeats = response[0].defeats
                totalEquals = response[0].equals
                totalGames = response[1]
                wins_pie = totalWins
                defeats_pie = totalDefeats
                equals_pie = totalEquals
                var nrWins = $('<a>Wins: ' + totalWins + ' </a>')
                var nrEquals = $('<a>Equals: ' + totalEquals + ' </a>')
                var nrDefeats = $('<a>Defeats:  ' + totalDefeats + ' </a>')
                var nrTotal = $('<a style="display:flex; align-items:center">Total games played: ' + totalGames + '</a>')
                $("#informations").empty()
                $("#informations").append(nrWins).html
                $("#informations").append(nrEquals).html
                $("#informations").append(nrDefeats).html
                $("#informations").append(nrTotal).html
                var markovForm = $('<form id="markov_form"><fieldset id="markov_fieldset"> </fieldset></form>')
                var lastResultVictory = $('<label id="victory_btn" class="radio-inline"><input class="rad-btn" type="radio" name="optradio" checked> Victory  </label>')
                var lastResultEqual = $('<label id="equal_btn" style="margin-left: 50px;" class="radio-inline"><input class="rad-btn" type="radio" name="optradio" checked> Equal  </label>')
                var lastResultDefeat = $('<label id="defeat_btn" style="margin-left: 50px;" class="radio-inline"><input class="rad-btn" type="radio" name="optradio" checked> Defeat  </label>')
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
            winChance = response['result_matrix'][0] * 100
            equalChance = response['result_matrix'][1] * 100
            defeatChance = response['result_matrix'][2] * 100
            var headerWin = $('<h4> Chance of winning: ' + winChance.toFixed(4)+ ' % </h4>')
            var headerEqual = $('<h4> Chance of equal: ' + equalChance.toFixed(4) + ' % </h4>')
            var headerDefeat = $('<h4> Chance of defeat: ' + defeatChance.toFixed(4) + ' % </h4>')
            $("#markov_informations").empty()
            $("#markov_informations").append(headerWin).html
            $("#markov_informations").append(headerEqual).html
            $("#markov_informations").append(headerDefeat).html
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

            var winWin = response['no_training_result']['0'][0] * 100
            console.log(winWin + "aaaaaaa")
            var equalWin = response['no_training_result']['0'][1] * 100
            var defeatWin = response['no_training_result']['0'][2] * 100
            var winEqual = response['no_training_result']['1'][0] * 100
            var equalEqual = response['no_training_result']['1'][1] * 100
            var defeatEqual = response['no_training_result']['1'][2] * 100
            var winDefeat = response['no_training_result']['2'][0] * 100
            var equalDefeat = response['no_training_result']['2'][1] * 100
            var defeatDefeat = response['no_training_result']['2'][2] * 100
            var table = $('<table id="tab" border="1"> </table>')
            var thead = $('<thead> <th>Win Start</th> <th>Equal Start</th> <th>Defeat Start</th> </thead>')
            var tbody = $('<tbody id="the_body"> </tbody>')
            $("#markov_table").empty().append(table)
            $("#tab").append(thead)
            $("#tab").append(tbody)
            var firstTr = $('<tr> <td>' + winWin.toFixed(3) + '%</td> <td>' + equalWin.toFixed(3) + '%</td> <td>' + defeatWin.toFixed(3) + '%</td> </tr>')
            var secondTr = $('<tr> <td>' + winEqual.toFixed(3) + '%</td>  <td>' + equalEqual.toFixed(3) + '%</td>  <td>' + defeatEqual.toFixed(3) + '%</td> </tr>')
            var thirdTr = $('<tr> <td>' + winDefeat.toFixed(3) + '%</td>  <td>' + equalDefeat.toFixed(3) + '%</td>  <td>' + defeatDefeat.toFixed(3) + '%</td> </tr>')
            $("#the_body").append(firstTr)
            $("#the_body").append(secondTr)
            $("#the_body").append(thirdTr)
        },
        error: function(error){
            console.log(error)
        }
    })
}

    
$('#bayes_button').click(function(event){
    var myTeam = $("#my_team").text().replace(" vs", "")
    var team = myTeam.replace(" ", "")
    var opponent = $("#opponent_team").text()
    event.preventDefault()
    event.stopPropagation()
    $.ajax({
         type: 'POST',
         url: '/bayes/calculate',
        data: {team1: team, team2: opponent},
        success: function(response){
            console.log(response)
            var bayesWin = response['bayes']['0'].toFixed(3)
            var bayesEqual = response['bayes']['1'].toFixed(3)
            var bayesDefeat = response['bayes']['2'].toFixed(3)
            var accuarcy = response['bayes']['3'] * 100   
            var winHead = $('<h4> Win chance: ' + bayesWin + ' %</h4>')
            var equalHead = $('<h4> Equal chance: ' + bayesEqual + ' %</h4>')
            var defeatHead = $('<h4> Defeat chance: ' + bayesDefeat + ' %</h4>')
            var accuarcyInfo = $('<p>The results were predicted with an acuarcy of: ' + accuarcy.toFixed(2) + ' % </p>')
            var bayesInformations = $('<div class="bayes-css" id="bayes_informations"> </div>')
            $("#bayes_clasifier_option").empty().append(bayesInformations).html
            $("#bayes_informations").append(winHead).html
            $("#bayes_informations").append(equalHead).html
            $("#bayes_informations").append(defeatHead).html
            $("#bayes_informations").append(accuarcyInfo).html            
        },
        error: function(error){
            console.log(error)
        }
     })
})


$('#markov_button').click(function(event){
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);
        
        function drawChart() {
                event.preventDefault()
                event.stopPropagation()
                var data = google.visualization.arrayToDataTable([
                    ['Matches', 'Match percentage'],
                    ['Wins',     wins_pie],
                    ['Losses',      defeats_pie],
                    ['Equals',  equals_pie]
                ]);
        
                var options = {
                    title: 'Statistic WLE',
                    backgroundColor: 'transparent',
                    'width':500,
                    'height':500,
                    colors: ['green','red', 'yellow'],
                    'font-color': 'white',
                    pieSliceTextStyle: {
                        color: 'black'
                    },
                    titleTextStyle: {
                        color: 'white'
                    },
                    legendTextStyle: {
                        color:'white'
                    },
                };
                var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(data, options);
            }
        })


