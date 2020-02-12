var checkmark = "fas fa-check";
var uncheckmark = "fas fa-times";
var full_star = "fas fa-star";
var empty_star = "far fa-star";
var half_star = "fas fa-star-half-alt";
var liste_jeux = [];
var amis_presents = [];
var tri = {'last': 'nom', 'votes': false, 'hot_seat': false, 'online': false, 'f2p': false,
            'coop': false, 'pvp': false, 'nom': true};

function Jeu(id, nom, pvp, coop, f2p, max_hot_seat, max_online, possede_par, votes){
    this.ident = id
    this.nom = nom;
    this.pvp = pvp;
    this.coop = coop;
    this.f2p = f2p;
    this.max_hot_seat = max_hot_seat;
    this.max_online = max_online;
    this.possede_par = possede_par;
    this.votes = [];
    this.cache = false;
    this.selectable = true;
    this.real_vote = -1;
    this.my_vote = -1;
}

Jeu.prototype.remplir_info = function(){
    this.nom = $('#'+this.ident+" .nom").text();
    this.max_hot_seat = parseInt($('#'+this.ident+" .hot_seat").text());
    this.max_online = parseInt($('#'+this.ident+" .online").text());
    this.cache = false;
    this.selectable = $('#'+this.ident+" .selectable").children('input');
    if($('#'+this.ident+" .pvp").text() === "False"){
        this.pvp = false;
        $('#'+this.ident+" .pvp").html('<i class="fas fa-times-circle"></i>');
    }else{
        this.pvp = true;
        $('#'+this.ident+" .pvp").html('<i class="fas fa-users"></i>');
    }
    if ($('#'+this.ident+" .coop").text() === "False"){
        this.coop = false;
        $('#'+this.ident+" .coop").html('<i class="fas fa-times-circle"></i>');
    }else{
        this.coop = true;
        $('#'+this.ident+" .coop").html('<i class="fas fa-users"></i>');
    }
    if ($('#'+this.ident+" .f2p").text() === "False"){
        this.f2p = false;
        $('#'+this.ident+" .f2p").html('<i class="fas fa-money-bill-wave"></i>');
    }else{
        this.f2p = true;
        $('#'+this.ident+" .f2p").html('<i class="fab fa-creative-commons-nc"></i>');
    }
    this.possede_par = [];
    possession = [];
    my_name = this.nom;
    list_votes = [];
    $(".jeu_ami").each(function(i){
        return $(this).children('li').each(function(j){
            if ($(this).text().split("|")[0].trim() === my_name){
                possesseur_name = $(this).parent().attr('id');
                possession.push(possesseur_name);
                list_votes.push([possesseur_name, $(this).text().split("|")[1].trim()]);
                $(this).html($(this).text().split("|")[0]);
            }
        });
    });
    this.possede_par = possession;
    this.my_vote = parseInt($('#'+this.ident+" .votes").text())
    this.votes = list_votes;
    this.get_real_vote(this.possede_par);
}

Jeu.prototype.get_real_vote = function(list_presents){
    calcul_real_vote = this.my_vote;
    if(list_presents.length > 0){
        for (var i = 0; i < this.votes.length; i++) {
            for (var j = 0; j < list_presents.length; j++){
                if(this.votes[i][0] === list_presents[j]){
                    calcul_real_vote = calcul_real_vote + parseInt(this.votes[i][1])
                }
            }
        }
        this.real_vote = calcul_real_vote/(list_presents.length+1);
    }else{
        this.real_vote = calcul_real_vote;
    }
    $('#'+this.ident+" .votes").html('');
    for (var i = 1; i <= 5; i++ ){
        if(i <= this.real_vote){
            $('#'+this.ident+" .votes").append('<i class="'+ full_star +'" id="vote-'+ i +'"></i>')
        }else if (i - 0.5 < this.real_vote){
            $('#'+this.ident+" .votes").append('<i class="'+ half_star +'" id="vote-'+ i +'"></i>')
        }else{
            $('#'+this.ident+" .votes").append('<i class="'+ empty_star +'" id="vote-'+ i +'"></i>')
        }
    }
}

function ordre_table(ou, quoi, valeur){
    liste_noms = $(ou).get();
    liste_noms.sort(function(a,b){
        switch(quoi){
            case 'nom':
                if(valeur){
                    if($(a).children('.nom').text().trim() < $(b).children('.nom').text().trim())return -1;
                    if($(a).children('.nom').text().trim() > $(b).children('.nom').text().trim()) return 1;
                    return 0;
                }else{
                    if($(a).children('.nom').text().trim() > $(b).children('.nom').text().trim())return -1;
                    if($(a).children('.nom').text().trim() < $(b).children('.nom').text().trim()) return 1;
                    return 0;
                }
            case 'online':
                if(valeur){
                    if(parseInt($(a).children('.online').text().trim()) > parseInt($(b).children('.online').text().trim())) return -1;
                    if(parseInt($(a).children('.online').text().trim()) < parseInt($(b).children('.online').text().trim())) return 1;
                    return 0;
                }else{
                    if(parseInt($(a).children('.online').text().trim()) < parseInt($(b).children('.online').text().trim())) return -1;
                    if(parseInt($(a).children('.online').text().trim()) > parseInt($(b).children('.online').text().trim())) return 1;
                    return 0;
                }
            case 'hot_seat':
                if(valeur){
                    if(parseInt($(a).children('.hot_seat').text().trim()) > parseInt($(b).children('.hot_seat').text().trim())) return -1;
                    if(parseInt($(a).children('.hot_seat').text().trim()) < parseInt($(b).children('.hot_seat').text().trim())) return 1;
                    return 0;
                }else{
                    if(parseInt($(a).children('.hot_seat').text().trim()) < parseInt($(b).children('.hot_seat').text().trim())) return -1;
                    if(parseInt($(a).children('.hot_seat').text().trim()) > parseInt($(b).children('.hot_seat').text().trim())) return 1;
                    return 0;
                }
            case 'pvp':
                if(valeur){
                    if($(a).children('.pvp').children('i').hasClass('fa-users') > $(b).children('.pvp').children('i').hasClass('fa-users')) return -1;
                    if($(a).children('.pvp').children('i').hasClass('fa-users') < $(b).children('.pvp').children('i').hasClass('fa-users')) return 1;
                    return 0;
                }else{
                    if($(a).children('.pvp').children('i').hasClass('fa-users') < $(b).children('.pvp').children('i').hasClass('fa-users')) return -1;
                    if($(a).children('.pvp').children('i').hasClass('fa-users') > $(b).children('.pvp').children('i').hasClass('fa-users')) return 1;
                    return 0;
                }
            case 'f2p':
                if(valeur){
                    if($(a).children('.f2p').children('i').hasClass('fa-creative-commons-nc') > $(b).children('.f2p').children('i').hasClass('fa-creative-commons-nc')) return -1;
                    if($(a).children('.f2p').children('i').hasClass('fa-creative-commons-nc') < $(b).children('.f2p').children('i').hasClass('fa-creative-commons-nc')) return 1;
                    return 0;
                }else{
                    if($(a).children('.f2p').children('i').hasClass('fa-creative-commons-nc') < $(b).children('.f2p').children('i').hasClass('fa-creative-commons-nc')) return -1;
                    if($(a).children('.f2p').children('i').hasClass('fa-creative-commons-nc') > $(b).children('.f2p').children('i').hasClass('fa-creative-commons-nc')) return 1;
                    return 0;
                }
            case 'coop':
                if(valeur){
                    if($(a).children('.coop').children('i').hasClass('fa-users') > $(b).children('.coop').children('i').hasClass('fa-users')) return -1;
                    if($(a).children('.coop').children('i').hasClass('fa-users') < $(b).children('.coop').children('i').hasClass('fa-users')) return 1;
                    return 0;
                }else{
                    if($(a).children('.coop').children('i').hasClass('fa-users') < $(b).children('.coop').children('i').hasClass('fa-users')) return -1;
                    if($(a).children('.coop').children('i').hasClass('fa-users') > $(b).children('.coop').children('i').hasClass('fa-users')) return 1;
                    return 0;
                }
            case 'votes':
                ai = 0.0;
                bi = 0.0;
                for (i = 1; i <= 5; i++){
                    if($(a).children('.votes').children('#vote-'+i).hasClass("fas") && $(a).children('.votes').children('#vote-'+i).hasClass("fa-star")) ai += 1;
                    if($(b).children('.votes').children('#vote-'+i).hasClass("fas") && $(b).children('.votes').children('#vote-'+i).hasClass("fa-star")) bi += 1;
                    if($(a).children('.votes').children('#vote-'+i).hasClass("fas") && $(a).children('.votes').children('#vote-'+i).hasClass("fa-star-half-alt")) ai += 0.5;
                    if($(b).children('.votes').children('#vote-'+i).hasClass("fas") && $(b).children('.votes').children('#vote-'+i).hasClass("fa-star-half-alt")) bi += 0.5;
                }
                if(valeur){
                    if(ai > bi) return -1;
                    if(ai < bi) return 1;
                }else{
                    if(ai > bi) return 1;
                    if(ai < bi) return -1;
                }
            default:
                return 0;
        }
    });
    $(liste_noms).each(function(i, tr){
        $(ou).parent().append(tr);
    });
    $('tr.tete').find('.fa-caret-down').remove();
    $('tr.tete').find('.fa-caret-up').remove();
    switch(quoi){
        case 'nom':
            if(valeur){
                $('th.nom:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.nom:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        case 'f2p':
            if(valeur){
                $('th.f2p:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.f2p:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        case 'coop':
            if(valeur){
                $('th.coop:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.coop:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        case 'pvp':
            if(valeur){
                $('th.pvp:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.pvp:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        case 'online':
            if(valeur){
                $('th.online:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.online:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        case 'hot_seat':
            if(valeur){
                $('th.hot_seat:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.hot_seat:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        case 'votes':
            if(valeur){
                $('th.votes:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
            }else{
                $('th.votes:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
            }
            break;
        default:
            return 0;
    }
}

function ordre_li(ou){
    liste_noms = $(ou).get();
    liste_noms.sort(function(a,b){
        if($(a).text().trim() < $(b).text().trim()) return -1;
        if($(a).text().trim() > $(b).text().trim()) return 1;
        return 0;
    });
    $(liste_noms).each(function(i,li){
        $(ou).parent().append(li);
    });
}

function chercher_jeu(){
    texte_cherche = $('#chercher_amis').val().toLowerCase();
    $("tr.jeu th.nom").each(function(){
        if(texte_cherche.trim()){
            if($(this).text().toLowerCase().indexOf(texte_cherche) == -1){
                $(this).parent().hide();
            }
        }
    });
    $("li.ami").each(function(){
        if(!texte_cherche.trim()){
            $(this).show();
            $(this).children('.jeu_ami').children('li').each(function(){
                $(this).show();
            });
            $(this).children('.jeu_ami').hide();
        }else{
            $(this).children('.jeu_ami').each(function(){
                $(this).children('li').each(function(){
                    if ($(this).text().toLowerCase().indexOf(texte_cherche) == -1){
                        $(this).hide();
                    }else{
                        $(this).parent().show();
                        $(this).show();
                    }
                });
            });
        }
    });
}

function update_liste_jeux(amis_presents, liste_jeux){
    var hot_seat_enabled = $('#hot_seat_enabled').is(':checked')
    if (amis_presents.length > 0){
        for ( i = 0; i < liste_jeux.length; i++){
            les_presents_lont = true;
            for ( j = 0; j < amis_presents.length; j++){
                if($.inArray(amis_presents[j], liste_jeux[i].possede_par) == -1 && !liste_jeux[i].f2p){
                    $("#"+liste_jeux[i].ident).hide();
                    les_presents_lont = false;
                    liste_jeux[i].cache = true;
                }
            }
            if(hot_seat_enabled){
                if(les_presents_lont || amis_presents.length +1 <= liste_jeux[i].max_hot_seat){
                    $("#"+liste_jeux[i].ident).show();
                    liste_jeux[i].get_real_vote(amis_presents);
                    liste_jeux[i].cache = false;
                }
                if(amis_presents.length +1 > liste_jeux[i].max_online 
                    && amis_presents.length +1 > liste_jeux[i].max_hot_seat){
                    $("#"+liste_jeux[i].ident).hide();
                    liste_jeux[i].cache = true;
                }
            }else{
                if(les_presents_lont){
                    $("#"+liste_jeux[i].ident).show();
                    liste_jeux[i].get_real_vote(amis_presents);
                    liste_jeux[i].cache = false;
                }
                if(amis_presents.length +1 > liste_jeux[i].max_online){
                    $("#"+liste_jeux[i].ident).hide();
                    liste_jeux[i].cache = true;
                }
            }
        }
    }else{
        $(".jeu").each(function(i){
            $(this).show();
        });
    }
    chercher_jeu();
    ordre_table('table tr.jeu',tri['last'], tri[tri['last']]);
}

function random_game(){
    test = 0;
    highest = 0;
    selected = 0;
    for ( i = 0; i < liste_jeux.length; i++){
        if(!liste_jeux[i].cache && liste_jeux[i].selectable.is(':checked')){
            test = Math.random() * liste_jeux[i].real_vote;
            // console.log(test+" obtenu avec "+ liste_jeux[i].votes+" votes.")
            if (test > highest){
                highest = test;
                selected = i;
            }
        }
    }
    $('#random-game').html(liste_jeux[selected].nom);
}

$(".toggle_jeux_ami").on('click', function(){
    $("#" + $(this).attr('id')+".jeu_ami").toggle(1000);
});


$(document).ready(function(){
    for ( i = 0; i < $(".jeu").length; i++ ){
        liste_jeux[i] = new Jeu($(".jeu:eq("+i+")").attr('id'));
        liste_jeux[i].remplir_info();
    }
    if(window.location.pathname === '/accueil'){
        $("#link-accueil").addClass('active');
    }
    $(".jeu_ami").each(function(i){
        return $(this).children('li').each(function(j){
            $(this).html($(this).text().split("|")[0]);
        });
    });
    ordre_table('table tr.jeu','nom', true);
    liste_noms = $('span.ami').parent('li').get();
    liste_noms.sort(function(a,b){
        if($(a).text().trim() < $(b).text().trim()) return -1;
        if($(a).text().trim() > $(b).text().trim()) return 1;
        return 0;
    });
    $(liste_noms).each(function(i, li){
        $('span.ami').parent('li').parent('ul').append(li);
    });
    $('li.ami > ul').each(function(){
        ordre_li($(this).children('li'));
    });
    $("#hot_seat_enabled").on('click', function(e){
        var e = e || window.event
        e.stopPropagation();
        update_liste_jeux(amis_presents, liste_jeux);
    });
});

$("span.ami").on('click', function(){
    if (!$(this).parent().hasClass('selected')) {
        $(this).parent().addClass('selected');
        $(this).parent().find("i:first").attr('class', checkmark);
        if ($.inArray($(this).parent().attr('id'), amis_presents) == -1){
            amis_presents.push($(this).parent().attr('id'));
        }
    }else{
        $(this).parent().removeClass('selected');
        $(this).parent().find("i:first").attr('class', uncheckmark);
        if($.inArray($(this).parent().attr('id'), amis_presents) != -1){
            amis_presents.splice($.inArray($(this).parent().attr('id'), amis_presents), 1);
        }
    }
    update_liste_jeux(amis_presents, liste_jeux);
});

$("#chercher_amis").on('keyup', function(){
    update_liste_jeux(amis_presents, liste_jeux);
    chercher_jeu();
});

$('tr.tete').children('th.nom').on('click', function(){
    tri['nom'] = !tri['nom'];
    ordre_table('table tr.jeu', 'nom', tri['nom']);
    tri['last'] = 'nom';
});

$('tr.tete').children('th.pvp').on('click', function(){
    tri['pvp'] = !tri['pvp'];
    ordre_table('table tr.jeu', 'pvp', tri['pvp']);
    tri['last'] = 'pvp';
});

$('tr.tete').children('th.coop').on('click', function(){
    tri['coop'] = !tri['coop'];
    ordre_table('table tr.jeu', 'coop', tri['coop']);
    tri['last'] = 'coop';
});

$('tr.tete').children('th.f2p').on('click', function(){
    tri['f2p'] = !tri['f2p'];
    ordre_table('table tr.jeu', 'f2p', tri['f2p']);
    tri['last'] = 'f2p';
});

$('tr.tete').children('th.hot_seat').on('click', function(){
    tri['hot_seat'] = !tri['hot_seat'];
    ordre_table('table tr.jeu', 'hot_seat', tri['hot_seat']);
    tri['last'] = 'hot_seat';
});

$('tr.tete').children('th.online').on('click', function(){
    tri['online'] = !tri['online'];
    ordre_table('table tr.jeu', 'online', tri['online']);
    tri['last'] = 'online';
});

$('tr.tete').children('th.votes').on('click', function(){
    tri['votes'] = !tri['votes'];
    ordre_table('table tr.jeu', 'votes', tri['votes']);
    tri['last'] = 'votes';
});

$('tr.tete').children('th.selectable').children('input').on('click', function(){
    if($(this).is(':checked')){
        $(".jeu").each(function(i){
            $(this).children('th.selectable').children('input').prop("checked", true);
        });
    }else{
        $(".jeu").each(function(i){
            $(this).children('th.selectable').children('input').prop("checked", false);
        });
    }
});

$('#btn-random-game').on('click', function(){
    random_game();
});