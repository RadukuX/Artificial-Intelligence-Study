$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url: '/get-your-teams',
        success: function(response){
            console.log(response.teams)
            count = 1
            for(let team of response.teams){
                var result = $('<div id=team' + count + ' class="team-name item-hover"/>').append(team)
                $('#teams').append(result).html()
                var flagId = team.toLowerCase().replace(" ", "-")
                var photoId = "option-image-" + flagId
                console.log(flagId)
                console.log(photoId)
                var photo = $('<div id='+ flagId +' onmouseover="test(this)" class="' + photoId + ' item-hover" />')
                $('#team' + count).append(photo).html
                count = count + 1
            }
        },
        error: function(error){
            alert(error)
        }
    })
})

function test(id){
    teamName = id.id
    event.preventDefault()
    event.stopPropagation()
    $.ajax({
        type: 'GET',
        url: '/get-info/' + teamName,
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

