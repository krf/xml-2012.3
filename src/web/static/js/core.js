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
            
            $("li.twitterlist").each(function(idx, para) {
               console.log($(this).html());
               var searchstring  = $(this).find("span.tsearch").html();
               
               console.log(idx+" "+para);
               
               var items = []
               var baseurl = "http://search.twitter.com/search.json?callback=?&q="+searchstring+"&lang=de&rpp=5&include_entities=true&result_type=mixed";
                console.log(baseurl);
                $.getJSON(baseurl, function(data) { 
                    
//                $.ajax({
//                  url: baseurl,
//                  dataType: 'json',
//                  data: "",
//                  async: false,
//                  success: function(data) {
//                        console.log("return from req"+idx);
//                    console.log("return from req"+idx);
//                    items[idx] = [];
//                    for (i=0; i < data.results.length; i++){
//                        row = data.results[i];
//                        items[idx].push('<li><span class="label">'+row.from_user+'</span>' +row.text+ '</li>');                
//                    }
//                    $($("li.twitterlist").get(idx)).find(".tweets").html(items[idx].join(''));
//                  }
//                });            
                    console.log("return from req"+idx);
                    items[idx] = [];
                    for (i=0; i < data.results.length; i++){
                        row = data.results[i];
                        items[idx].push('<li><span class="label">'+row.from_user+'</span>' +row.text+ '</li>');                
                    }
                    $($("li.twitterlist").get(idx)).find(".tweets").html(items[idx].join(''));                    
                                      
                });
               
               
            });
           
            
            
//            var baseurl = "http://search.twitter.com/search.json?callback=?&q="+$("div.detail #tsearch").html()+"&lang=de&rpp=5&include_entities=true&result_type=mixed";
//            console.log(baseurl);
//            $.getJSON(baseurl, function(data) {         
//                
//                var items = [];
//                for (i=0; i < data.results.length; i++){
//                    row = data.results[i];
//                    items.push('<li><span class="label">'+row.from_user+'</span>' +row.text+ '</li>');                
//                }
//                $("#twitterresultlist").html(items.join(''));
//                
////                $('<ul/>', {
////                    'class': 'my-new-list',
////                    html: items.join('')
////                }).appendTo('#tresults');
////                
//                
//                                  
//            });
        });
    }); 
});
