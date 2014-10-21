
var flag;
//complaint form
$(function() {
    $('#complaint_form').submit(function() {// catch the form's submit event

        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: "/tellmeaboutit/complaints/", // the file to call
            success: function(response) { // on success..
                $('#Complaints_List').html(response);
                document.getElementById("complaint_form").reset();
            }
        });
        return false;
    });
});

//logout
function logout(){
    window.location = '/tellmeaboutit/logout/';
}

//display most popular
function mostpopular(){
    $.get('/tellmeaboutit/popular/', function(data){
        $('#Complaints_List').html(data);


    });
}

//display most recent
function mostrecent(){
        $.get('/tellmeaboutit/recent/', function(data){
            $('#Complaints_List').html(data);


        });
}



//resize dynamically the textarea
    window.onload = function() {
        var t = document.getElementsByTagName('textarea')[0];
        var offset= !window.opera ? (t.offsetHeight - t.clientHeight) : (t.offsetHeight + parseInt(window.getComputedStyle(t, null).getPropertyValue('border-top-width'))) ;
        var resize  = function(t) {
            t.style.height = 'auto';
            t.style.height = (t.scrollHeight  + offset ) + 'px';
        }
        t.addEventListener && t.addEventListener('input', function(event) {
            resize(t);
        });

        t['attachEvent']  && t.attachEvent('onkeyup', function() {
            resize(t);
        });

            $.get('/tellmeaboutit/mostCommenting/', function(data){
                $('#chart_div').html(data);


            });



    }

//redirect to register
$(function() {
    $("#btn_Register").click( function()
        {

            window.location.replace("/tellmeaboutit/register/");
        }
    );
});

//search
$(function() {
    $('#form_search').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: "/tellmeaboutit/search/", // the file to call
            success: function(response) { // on success..
                $('#Complaints_List').html(response);
            }
        });
        return false;
    });
});

//post comment
$(function() {
    $('#postComment').submit(function() { // catch the form's submit event
        var cid=$(flag).parent().children('div').attr("id");

        var text_comment =$('#textarea-comment').val();
        $.get('/tellmeaboutit/postComment/', {comment_id: cid, comment_cnt: text_comment}, function(data){
            $('#comments').html(data);
            document.getElementById("postComment").reset();

        });
        return false;
    });
});








//popup

function toggle(div_id) {
    var el = document.getElementById(div_id);
    if ( el.style.display == 'none' ) {	el.style.display = 'block';}
    else {el.style.display = 'none';}
}
function blanket_size(popUpDivVar) {
    if (typeof window.innerWidth != 'undefined') {
        viewportheight = window.innerHeight;
    } else {
        viewportheight = document.documentElement.clientHeight;
    }
    if ((viewportheight > document.body.parentNode.scrollHeight) && (viewportheight > document.body.parentNode.clientHeight)) {
        blanket_height = viewportheight;
    } else {
        if (document.body.parentNode.clientHeight > document.body.parentNode.scrollHeight) {
            blanket_height = document.body.parentNode.clientHeight;
        } else {
            blanket_height = document.body.parentNode.scrollHeight;
        }
    }
    var blanket = document.getElementById('blanket');
    blanket.style.height = blanket_height + 'px';
    var popUpDiv = document.getElementById(popUpDivVar);
    popUpDiv_height=blanket_height/2-200;//200 is half popup's height
    popUpDiv.style.top = popUpDiv_height + 'px';
}
function window_pos(popUpDivVar) {
    if (typeof window.innerWidth != 'undefined') {
        viewportwidth = window.innerHeight;
    } else {
        viewportwidth = document.documentElement.clientHeight;
    }
    if ((viewportwidth > document.body.parentNode.scrollWidth) && (viewportwidth > document.body.parentNode.clientWidth)) {
        window_width = viewportwidth;
    } else {
        if (document.body.parentNode.clientWidth > document.body.parentNode.scrollWidth) {
            window_width = document.body.parentNode.clientWidth;
        } else {
            window_width = document.body.parentNode.scrollWidth;
        }
    }
    var popUpDiv = document.getElementById(popUpDivVar);
    window_width=window_width/2-200;//200 is half popup's width
    popUpDiv.style.left = window_width + 'px';
}
function popup(windowname) {
    blanket_size(windowname);
    window_pos(windowname);
    toggle('blanket');
    toggle(windowname);

}

//displayComments

var secondClick=false;
function showDiv(e)
{
    var compid;
    flag=e;


    if (flag.text == "Hide Comments")
    {
        //document.getElementById("CommentBox").style.display = "none";
        flag.innerHTML ="Show Comments";

        $(e).parent().children('div').css('display', 'none');    }
    else
    {
        compid = $(e).parent().children('div').attr("id");

        $.get('/tellmeaboutit/showComments/', {complaint_id: compid}, function(data){

            $(e).parent().children('div').html('');
            $(e).parent().children('div').html(data);
            //document.getElementById("CommentBox").style.display="inline";
            $(e).parent().children('div').css('display', 'inline');

            e.innerHTML ="Hide Comments";

            //popup('popUpDiv');
        });

    }
}

//see all comments
function showAllComments(e)
{
    flag2=e
    catid = $(flag2).parent().children('div').attr("id");
    $.get('/tellmeaboutit/PopuPcomments/', {comment_id: catid}, function(data){
        $('#Complaints_List2').html(data);
        popup('popUpDiv');
    });

}

//rating
function rating(e,id){
    var vote=e;


    var userid=$(id).attr('value');
    var complaint_id=$(id).attr('id');
    var id_likes = complaint_id + 'k'

    $.get('/tellmeaboutit/rating/', {complaint_id: complaint_id, vote: vote, user_id: userid}, function(data){
        $(id).parent('div').hide()

        document.getElementById(id_likes).appendChild(document.createTextNode(data));
        document.getElementById(id_likes).style.display='inline'
    });

}

