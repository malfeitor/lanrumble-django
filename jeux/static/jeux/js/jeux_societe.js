var checkmark = "fas fa-check";
var uncheckmark = "fas fa-times";
var liste_jeux = [];
var amis_presents = [];
var cerveau = "<i class='fas fa-brain'></i>";
var tri_nom = true;
var tri_temps = false;
var tri_complexite = false;
var tri_joueurs_min = false;
var tri_joueurs_max = false;

function Jeu(id, nom, temps_prevu_h, temps_prevu_m, complexite, 
            joueurs_min, joueurs_max, possede_par, contexte){
    this.ident = id
    this.nom = nom;
    this.temps_prevu_h = temps_prevu_h;
    this.temps_prevu_m = temps_prevu_m;
    this.complexite = complexite;
    this.joueurs_min = joueurs_min;
    this.joueurs_max = joueurs_max;
    this.possede_par = possede_par;
    this.contexte = contexte;
}

Jeu.prototype.remplir_info = function(){
    this.nom = $('#'+this.ident+" .nom").text();
    temps_prevu_text = $('#'+this.ident+" .temps").text();
    this.temps_prevu_h = parseInt(temps_prevu_text.slice(0,temps_prevu_text.indexOf('h')));
    this.temps_prevu_m = parseInt(temps_prevu_text.slice(temps_prevu_text.indexOf('h')+2,temps_prevu_text.indexOf('m')));
    this.complexite = parseInt($('#'+this.ident+" .complexite").text());
    $('#'+this.ident+" .complexite").text("");
    switch(this.complexite){
        case 5:
            $('#'+this.ident+" .complexite").css("color", "red");
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            break;
        case 4:
            $('#'+this.ident+" .complexite").css("color", "orange");
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            break;
        case 3:
            $('#'+this.ident+" .complexite").css("color", "yellow");
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            break;
        case 2:
            $('#'+this.ident+" .complexite").css("color", "green");
            $('#'+this.ident+" .complexite").append(cerveau);
            $('#'+this.ident+" .complexite").append(cerveau);
            break;
        case 1:
            $('#'+this.ident+" .complexite").css("color", "white");
            $('#'+this.ident+" .complexite").append(cerveau);
            break;
    }
    this.joueurs_min = parseInt($('#'+this.ident+" .joueurs_min").text());
    this.joueurs_max = parseInt($('#'+this.ident+" .joueurs_max").text());
    this.possede_par = [];
    possession = [];
    my_name = this.nom;
    $(".jeu_ami").each(function(i){
        return $(this).children('li').each(function(j){
            if ($(this).text() === my_name){
                possession.push($(this).parent().attr('id'));
            }
        });
    });
    this.possede_par = possession;
    this.contexte = $('#'+this.ident);
}

function update_jeux(liste_jeux, amis_presents){
    $(liste_jeux).each(function(){
        if(this.joueurs_min <= parseInt($("#joueurs_presents").val()) &&
            this.joueurs_max >= parseInt($("#joueurs_presents").val())){
            personnes_qui_lont = 0;
            for(j=0;j<this.possede_par.length; j++){
                if($.inArray(this.possede_par[j], amis_presents) != -1){
                    personnes_qui_lont ++;
                }
            }
            if(personnes_qui_lont > 0){
                $("#"+this.ident).show();
            }else{
                $("#"+this.ident).hide();
            }
        }else{
            $("#"+this.ident).hide();
        }
    });
}

function ordre_table(ou, quoi, valeur){
    liste_noms = $(ou).get();
    liste_noms.sort(function(a,b){
    $('tr.tete').find('.fa-caret-down').remove();
    $('tr.tete').find('.fa-caret-up').remove();
        switch(quoi){
            case 'nom':
                if(valeur){
                    $('th.nom:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].nom < liste_jeux[$(b).attr('id')].nom)return -1;
                    if(liste_jeux[$(a).attr('id')].nom > liste_jeux[$(b).attr('id')].nom) return 1;
                    return 0;
                }else{
                    $('th.nom:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].nom > liste_jeux[$(b).attr('id')].nom)return -1;
                    if(liste_jeux[$(a).attr('id')].nom < liste_jeux[$(b).attr('id')].nom) return 1;
                    return 0;
                }
                break;
            case 'complexite':
                if (valeur) {
                    $('th.complexite:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].complexite < liste_jeux[$(b).attr('id')].complexite)return -1;
                    if(liste_jeux[$(a).attr('id')].complexite > liste_jeux[$(b).attr('id')].complexite)return 1;
                    return 0;
                }else{
                    $('th.complexite:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].complexite > liste_jeux[$(b).attr('id')].complexite)return -1;
                    if(liste_jeux[$(a).attr('id')].complexite < liste_jeux[$(b).attr('id')].complexite)return 1;
                    return 0;
                }
                break;
            case 'joueurs_min':
                if (valeur) {
                    $('th.joueurs_min:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].joueurs_min < liste_jeux[$(b).attr('id')].joueurs_min)return -1;
                    if(liste_jeux[$(a).attr('id')].joueurs_min > liste_jeux[$(b).attr('id')].joueurs_min)return 1;
                    return 0;
                }else{
                    $('th.joueurs_min:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].joueurs_min > liste_jeux[$(b).attr('id')].joueurs_min)return -1;
                    if(liste_jeux[$(a).attr('id')].joueurs_min < liste_jeux[$(b).attr('id')].joueurs_min)return 1;
                    return 0;
                }
                break;
            case 'joueurs_max':
                if (valeur) {
                    $('th.joueurs_max:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].joueurs_max < liste_jeux[$(b).attr('id')].joueurs_max)return -1;
                    if(liste_jeux[$(a).attr('id')].joueurs_max > liste_jeux[$(b).attr('id')].joueurs_max)return 1;
                    return 0;
                }else{
                    $('th.joueurs_max:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].joueurs_max > liste_jeux[$(b).attr('id')].joueurs_max)return -1;
                    if(liste_jeux[$(a).attr('id')].joueurs_max < liste_jeux[$(b).attr('id')].joueurs_max)return 1;
                    return 0;
                }
                break;
            case 'temps':
                if (valeur) {
                    $('th.temps:first').append('<i class="fas fa-caret-down" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].temps_prevu_h < liste_jeux[$(b).attr('id')].temps_prevu_h)return -1;
                    if(liste_jeux[$(a).attr('id')].temps_prevu_h > liste_jeux[$(b).attr('id')].temps_prevu_h)return 1;
                    if(liste_jeux[$(a).attr('id')].temps_prevu_m < liste_jeux[$(b).attr('id')].temps_prevu_m)return -1;
                    if(liste_jeux[$(a).attr('id')].temps_prevu_m > liste_jeux[$(b).attr('id')].temps_prevu_m)return 1;
                    return 0;
                }else{
                    $('th.temps:first').append('<i class="fas fa-caret-up" style="margin-left: 5px;"></i>');
                    if(liste_jeux[$(a).attr('id')].temps_prevu_h > liste_jeux[$(b).attr('id')].temps_prevu_h)return -1;
                    if(liste_jeux[$(a).attr('id')].temps_prevu_h < liste_jeux[$(b).attr('id')].temps_prevu_h)return 1;
                    if(liste_jeux[$(a).attr('id')].temps_prevu_m > liste_jeux[$(b).attr('id')].temps_prevu_m)return -1;
                    if(liste_jeux[$(a).attr('id')].temps_prevu_m < liste_jeux[$(b).attr('id')].temps_prevu_m)return 1;
                    return 0;
                }
                break;
            default:
                return 0;
        }
    });
    $(liste_noms).each(function(i, tr){
        $(ou).parent().append(tr);
    });
}

function order_select(ou){
    liste_noms = ou.children('option').get();
    liste_noms.sort(function(a, b){
        if($(a).text()<$(b).text())return -1;
        if($(a).text()>$(b).text())return 1;
        return 0;
    });
    $(liste_noms).each(function(i, selecting){
        ou.append(selecting);
    });
}

$(".toggle_jeux_ami").on('click', function(){
    $("#" + $(this).attr('id')+".jeu_ami").toggle(1000);
});

$("#joueurs_presents").on('keyup', function(){
    if($.isNumeric($("#joueurs_presents").val())){
        update_jeux(liste_jeux, amis_presents);
    }
});
$("#joueurs_presents").on('change', function(){
    if($.isNumeric($("#joueurs_presents").val())){
        update_jeux(liste_jeux, amis_presents);
    }
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
    update_jeux(liste_jeux, amis_presents);
});

$("#chercher_jeu").on('keyup', function(){
    texte_cherche = $('#chercher_jeu').val().toLowerCase();
    $(".jeu_ami li[id]").each(function(i){
        if(!texte_cherche.trim()){
            $(this).parent().hide();
            $(this).hide();
        }else{
            if($(this).text().toLowerCase().indexOf(texte_cherche) == -1){
                $(this).hide();
            }else{
                if($(this).parent().is(":hidden")){
                    $(this).parent().show()
                }
                $(this).show();
            }
        }
    });
});

$(document).ready(function(){
    console.log("jQuery OK");
    if(window.location.pathname === '/jeux_societe'){
        $("#link-societe").addClass('active');
    }
    for ( i=0; i<$(".jeu").length; i++){
        liste_jeux[$(".jeu:eq("+i+")").attr('id')] = new Jeu($(".jeu:eq("+i+")").attr('id'));
        liste_jeux[$(".jeu:eq("+i+")").attr('id')].remplir_info();
    }
    // On chope la ligne de l'utilisateur, 
    // on l'ajoute forcement dans la liste des amis presents
    amis_presents.push($("#user_name").text().trim());
    $("#"+$("#user_name").text().trim()+" i:first").remove();
    $("#"+$("#user_name").text().trim()+" span.ami").off('click');
    $("#"+$("#user_name").text().trim()+" span").text("  Vos jeux : ");
    temp = $("#"+$("#user_name").text().trim()).next();
    $("#"+$("#user_name").text().trim()).insertBefore("#chercher_jeu");
    temp.insertAfter("#"+$("#user_name").text().trim()+":first");
    $('<li><br></li>').insertAfter(temp);
    update_jeux(liste_jeux, amis_presents);
    ordre_table('table tr.jeu', 'nom', tri_nom);
    $("#liste_possesseurs_ajouter").append('<option value="'+$("#user_name").text().trim()+'">'+$("#user_name").text().trim()+'</option>');
    order_select($("#liste_possesseurs_ajouter"));
});

$(document).keypress(function(e) {
    if(e.which == 13) {
        e.preventDefault();
        e.stopPropagation();
    }
});

$('tr.tete').children('th.nom').on('click', function(){
    tri_nom = !tri_nom;
    ordre_table('table tr.jeu', 'nom', tri_nom);
});

$('tr.tete').children('th.temps').on('click', function(){
    tri_temps = !tri_temps;
    ordre_table('table tr.jeu', 'temps', tri_temps);
});

$('tr.tete').children('th.complexite').on('click', function(){
    tri_complexite = !tri_complexite;
    ordre_table('table tr.jeu', 'complexite', tri_complexite);
});

$('tr.tete').children('th.joueurs_min').on('click', function(){
    tri_joueurs_min = !tri_joueurs_min;
    ordre_table('table tr.jeu', 'joueurs_min', tri_joueurs_min);
});

$('tr.tete').children('th.joueurs_max').on('click', function(){
    tri_joueurs_max = !tri_joueurs_max;
    ordre_table('table tr.jeu', 'joueurs_max', tri_joueurs_max);
});
