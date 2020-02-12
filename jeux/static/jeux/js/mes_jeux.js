$(function() {
        // This function gets cookie with a given name
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        /*
        The functions below will create a header with csrftoken
        */

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

    });

function ordre_li(ou){
    liste_noms = $(ou).get();
    liste_noms.sort(function(a,b){
        if($(a).text().trim() < $(b).text().trim()) return -1;
        if($(a).text().trim() > $(b).text().trim()) return 1;
        return 0;
    });
    $(liste_noms).each(function(i, li){
        $(ou).parent().append(li);
    });
}

function search_jeu(lequel){
    // la ligne dessous renvoie le texte présent dans la boite de recherche
    texte_cherche = $("#"+lequel+"-search").val().toLowerCase();
    // pour toutes les lignes qui ont un nom de jeu
    $("#"+lequel+"-div tr[id]").each(function(){
        // Si le nom du jeu ne contiens pas le texte du champ recherche
        if ($(this).children("th").children("label").text().toLowerCase().indexOf(texte_cherche) == -1){
            $(this).hide();
        }else{
            $(this).show();
        }
    });
}
// Fonction appellée quand on clique sur une étoile pour voter
function vote_clic(ident, valeur){
    $.ajax({
        type: "POST",
        url: "ajax/vote_jeuvideo",
        data: {jeu: ident, vote: valeur},
        success: function(){
            for (i = 1; i <= 5; i++){
                if ( i <= valeur){
                    if($('#'+ident+' #vote-'+i).hasClass("far")){
                        $('#'+ident+' #vote-'+i).addClass("fas");
                        $('#'+ident+' #vote-'+i).removeClass("far");
                    }
                }else{
                    if($('#'+ident+' #vote-'+i).hasClass("fas")){
                        $('#'+ident+' #vote-'+i).addClass("far");
                        $('#'+ident+' #vote-'+i).removeClass("fas");
                    }
                }
            }
        },
        dataType: "json"
    });
}

function print_votes(){
    vote_list = $("#votes").text().replace(/\s+/g,'').split('*');
    for(i=0; i<vote_list.length; i++){
        id = vote_list[i].split('/')[0]
        value = vote_list[i].split('/')[1]
        for (j=1;j<=5;j++){
            if(j<=value){
                if($('#tr-'+id+' #vote-'+j).hasClass("far")){
                    $('#tr-'+id+' #vote-'+j).addClass("fas");
                    $('#tr-'+id+' #vote-'+j).removeClass("far");
                }
            }else{
                if($('#tr-'+id+' #vote-'+j).hasClass("fas")){
                    $('#tr-'+id+' #vote-'+j).addClass("far");
                    $('#tr-'+id+' #vote-'+j).removeClass("fas");
                }
            }
        }
    }
}

$("#ajouter-search").on('keyup', function(event){
    search_jeu("ajouter");
});

$("#enlever-search").on('keyup', function(event){
    search_jeu("enlever");
});

$("#nom").focus(function(){
    if($("#nom").val() == "Nom :"){
        $('#nom').val("");
    }
});
$("#nom").blur(function(){
    if($("#nom").val() == ""){
        $("#nom").val("Nom :"); 
    }
});

$(document).keypress(function(e) {
    if(e.which == 13) {
        e.preventDefault();
        e.stopPropagation();
    }
});

$(document).ready(function(){
    console.log("jQuery OK");
    if(window.location.pathname === '/mes_jeux'){
        $("#link-jeux").addClass('active');
    }
    ordre_li('#ajouter-div table tr');
    ordre_li('#enlever-div table tr');
    // Pour chaque clic sur les étoiles d'un jeu
    $('tr.jeu #vote-1').on('click', function(){
        // L'id du jeu sur lequel on a cliqué
        vote_clic($(this).parent().parent().attr('id'), 1);
    });
    $('tr.jeu #vote-2').on('click', function(){vote_clic($(this).parent().parent().attr('id'), 2);});
    $('tr.jeu #vote-3').on('click', function(){vote_clic($(this).parent().parent().attr('id'), 3);});
    $('tr.jeu #vote-4').on('click', function(){vote_clic($(this).parent().parent().attr('id'), 4);});
    $('tr.jeu #vote-5').on('click', function(){vote_clic($(this).parent().parent().attr('id'), 5);});
    print_votes();
});

