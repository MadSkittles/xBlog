$("#show-tags").click(function(){
    if  ($(".tags").css("overflow") == "hidden"){
        $(".tags").css("height", 'auto')
        $(".tags").css("overflow", 'visible')
    }else{
        $(".tags").css("overflow", 'hidden')
        $(".tags").css("height", '40px')
    }
    $('#show-tags > a').toggleClass('icon-chevron-down icon-chevron-up');
    return false;
});


$('#today-visitors').next().hide()
$('#online-visitors').next().hide()
$('#visit-count').next().hide()
function today_visitors(csrf_token){
    var today_visitors_ol = $('#today-visitors').next();
    if (today_visitors_ol.attr('style').indexOf('none') > 0){
        $.post('/today-visitors/',
            {'csrfmiddlewaretoken':csrf_token},
            function(data){
                console.info(data.data)
                for (var i in data.data){
                    var v = data.data[i];
                    var html = '<small><li>'+v.nickname+'<span class="pull-right">'+v.date_time+'</span></li></small>';
                    today_visitors_ol.append(html);
                }
            }
        );
    }
    today_visitors_ol.empty().toggle();
};
function online_visitors(csrf_token){
    var online_visitors_ol = $('#online-visitors').next();
    if (online_visitors_ol.attr('style').indexOf('none') > 0){
        $.post('/online-visitors/',
            {'csrfmiddlewaretoken':csrf_token},
            function(data){
                for (var i in data.data){
                    var v = data.data[i];
                    var html = '<small><li>'+v.nickname+'<span class="pull-right">'+''+'</span></li></small>';
                    online_visitors_ol.append(html);
                }
            }
        );
    }
    online_visitors_ol.empty().toggle();
};
function visit_count(csrf_token){
    var count_ul = $('#visit-count').next();
    if (count_ul.attr('style').indexOf('none') > 0){
        $.post('/visit-count/',
            {'csrfmiddlewaretoken':csrf_token},
            function(data){
                var pv = '<small><li>PV<span class="pull-right">'+data.pv+'</span></li></small>';
                var uv = '<small><li>UV<span class="pull-right">'+data.uv+'</span></li></small>';
                count_ul.append(uv).append(pv);
            }
        );
    }
    count_ul.empty().toggle();
};

$('#show-visitor-profile').click(function(){
    $("#visitor-profile").toggle();
});

$('.clear-form').click(function(){
    $('#comment-content').val('');
    $reply_to_who_id = null;
})

function init_reply($reply_button){
    var $floor = $reply_button.parent().children('small:first').text().trim();
    var $who = $reply_button.parent().children('a:first').text().trim();
    $reply_to_who_id = $reply_button.parent().children('span:first').text();
    reply = '回复 '+$floor+' '+$who+' ';
    $('#comment-content').val(reply);
    $('#comment-content').focus(function (event) {
        if($('#comment-content').val()==reply) {
            $('#comment-content').val('');
        }
    });
    $('#comment-content').blur(function (event) {
        if($('#comment-content').val()=='') {
            $('#comment-content').val(reply);
        }
    });
}

$('.reply-button').click(function(){
    var $reply_button = $(this);
    init_reply($reply_button);
    $('#tip').hide();
});

function comment(article_id, csrf_token){
    var $nickname = $('#nickname').val().trim();
    var $email = $('#email').val().trim();
    var $url = $('#url').val().trim();
    var $comment_content = $('#comment-content').val().trim();
    var $forloop = $('.comment:last').children('small:first').text().substr(1)*1+1;
    if (isNaN($forloop)){$forloop = 1};

    if ('' == $comment_content){
        $('#tip').show();
        return false;
    }
    $("#cbtn").attr('disabled', 'disabled');
    $.post('/comment/'+article_id+'/',
           {
            'nickname':$nickname,
            'email':$email,
            'url':$url,
            'content':$comment_content,
            'reply_to_who_id':$reply_to_who_id,
            'csrfmiddlewaretoken':csrf_token
           },
           function(data){
               if (typeof(data) == 'object'){
                   if (data.reply_to == null){
                       $html = '<div class="comment" id="' + $forloop + '"><small>#' + $forloop + '</small> <a href="' + data.url + '" target="_blank"><img src="/static/img/avatar.jpg" width=14>' + data.author + '</a><span class="hide">' + data.id + '</span> : <blockquote>' + data.content + '</blockquote><small>' + data.submit_time + '</small><small class="pull-right" onclick="init_reply($(this));"><a data-toggle="modal" href="#comment-modal" title="回复该条评论">回复</a></small></div>'
                   }else{
                       $html = '<div class="comment" id="' + $forloop + '"><small>#' + $forloop + '</small> <a href="' + data.url + '" target="_blank"><img src="/static/img/avatar.jpg" width=14>' + data.author + '</a><span class="hide">' + data.id + '</span> <a href="#' + data.reply_to_id + '" class="reply-to" onclick="hightlight(\'' + data.reply_to_id + '\')">' + data.reply_to + '</a> : <blockquote>' + data.content + '</blockquote><small>' + data.submit_time + '</small><small class="pull-right" onclick="init_reply($(this));"><a data-toggle="modal" href="#comment-modal" title="回复该条评论">回复</a></small></div>'
                   }
                   $('#comment-list').append($html)
                   $('#comment-count').text($('#comment-count').text()*1+1)
                   $(".close").trigger('click');
               }else{
                   alert(data)
               }
               $('#cbtn').removeAttr('disabled');
           }
        );
};

function hightlight(reply_to_id){
    $('#'+reply_to_id).addClass('comment-hightlight').siblings().removeClass('comment-hightlight')
};

$('#display_links').click(function(){
    $(this).prevAll('.hide').toggle();
    $('#display_links > center > a').toggleClass('icon-chevron-down icon-chevron-up');
});

$('#display_links').hover(
    function(){$(this).attr('style', 'background-color:#21252A;')},
    function(){$(this).removeAttr('style')}
);


$('#display_archives').click(function(){
    $(this).prevAll('.hide').toggle();
    $('#display_archives > center > a').toggleClass('icon-chevron-down icon-chevron-up');
});

$('#display_archives').hover(
    function(){$(this).attr('style', 'background-color:#21252A;')},
    function(){$(this).removeAttr('style')}
);

$('#display_categories').click(function(){
    $(this).prevAll('.hide').toggle();
    $('#display_categories > center > a').toggleClass('icon-chevron-down icon-chevron-up');
});

$('#display_categories').hover(
    function(){$(this).attr('style', 'background-color:#21252A;')},
    function(){$(this).removeAttr('style')}
);


$('#mrashin').addClass('animated fadeInDownBig');
$('#idarticle').addClass('animated rotateInDownRight');
$('#idlist').addClass('animated rotateInDownLeft');
$('#idprofile').addClass('animated rubberBand');
$('#idicon').addClass('animated rotateIn');


$('#l0').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
$('#l1').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
$('#l2').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
$('#l3').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
$('#l4').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
$('#l5').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
$('#l6').click(function(){
    $(this).addClass('active').siblings().removeClass('active')
});
