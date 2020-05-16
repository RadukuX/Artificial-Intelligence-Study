$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url: '/get-your-teams',
        success: function(response){
            console.log(response.teams)
            count = 1
            console.log(response.teams)
            for(let team of response.teams){
                var result = $('<div id=team' + count + ' class="team-name item-hover" />').append(team)
                $('#teams').append(result).html()
                var flagId = team.toLowerCase().replace(" ", "-")
                var flagId2 = team.replace(" ", "-")
                var photoId = "option-image-" + flagId
                var photo = $('<div id='+ flagId2 +' onclick="predictionTitle(id)" onmouseover="showResults(this)" class="' + photoId + ' item-hover" />')
                $('#team' + count).append(photo).html
                //var predictionButton = $('<button style="display: flex; align-items: center, justify-content:center, margin-bottom:100px">Do a prediction</button>')
                //$('#teams').append(predictionButton).html
                count = count + 1
            }
        },
        error: function(error){
            alert(error)
        }
    })
})

function showResults(id){
    teamName = id.id
    event.preventDefault()
    event.stopPropagation()
    $.ajax({
        type: 'GET',
        url: '/get-info/' + teamName.toLowerCase(),
        success: function(response){
            var seasons = response
            var the_row
            $('#table_name').empty().append(teamName).html
            $('#table_body').empty().html
            Object.entries(seasons).forEach(([key, value]) => {
                console.log(value)
                the_row = $('<tr> <td>' + value[0] + '</td> <td>' + value[1] + '</td><td>' + value[2] + '</td> <td>' + value[3] + '</td> <td>' + value[4] + '</td> <td>' + value[5] + '</td> <td>' + value[6] + '</td> <td>' + value[7] + '</td>')
                $('#table_body').append(the_row).html
            });
            
        },
        error: function(error){
            console.log(error)
        }
    })
}

//function prediction(){
//    $.ajax({
//        type: 'GET',
  ///      url: '/prediction',
  //      success: function(response){
//
//document.location.href = '/prediction'
   //     },
   //     error: function(error){
   //         document.location.href = '/home'
//        }
  //  })
//}

function predictionTitle(id){
    teamName = id
    console.log('team name !!!' + teamName)
    $.ajax({
        type: 'GET',
        url: '/prediction',
        success: function(response){
            localStorage.setItem('team-name', teamName)
            document.location.href = '/prediction'
        },
        error: function(error){
            console.log(error)
        }
    })
}