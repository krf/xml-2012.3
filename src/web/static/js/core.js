$(document).ready(function() {
    console.log('start');    
    
    
    /* load detailinfo of route */
    /* catch every klick on an <a>tag and perform ajaxrequest with href */
    $("div.summary a.ajax").click(function (evt) {
        evt.preventDefault();
        var target = $(this).attr('href');
        console.log(target);
        
        $.get(target, function(data) {
            $("div.detail").html(data);
            
            /* retrieve some twitterinfo */
            var baseurl = "http://search.twitter.com/search.json?callback=?&q="+$("div.detail #tsearch").html()+"&rpp=5&include_entities=true&result_type=mixed";
            console.log(baseurl);
            $.getJSON(baseurl, function(data) {         
                
                var items = [];
                for (i=0; i < data.results.length; i++){
                    row = data.results[i];
                    items.push('<li>' + row.from_user + ' said:' +row.text+ '</li>');                
                }
                
                $('<ul/>', {
                    'class': 'my-new-list',
                    html: items.join('')
                }).appendTo('#tresults');
                
                
                                  
            });
        });
    }); 
});
