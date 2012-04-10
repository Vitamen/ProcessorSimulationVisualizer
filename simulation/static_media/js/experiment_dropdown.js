var maxHeight = 600;
var experiment_id = document.getElementById('experiment_id').getAttribute('value');

var $_GET = getQueryParams(document.location.search);
var experiments_list = $("#experiment_list");
var experiment_form = $("form#experiment_form");

for (var i=0; i < experiments.length; i++) {
	var experiment = experiments[i];
	
	var experiment_element = $('<li>');
	var experiment_div = $('<div>').attr({
		id: experiment,
		class: "experiment"
	})
	experiment_element.append(experiment_div);
	
	var experiment_element_link_text = document.createTextNode(experiment);
	var experimentpound = "#"+experiment;
	experiment_div.click(function() {
		var experiment = $(this).attr('id');	
		var form_element = $('<input>').attr({
		    type: 'hidden',
		    name: 'experiment',
		    value: experiment
		}).appendTo(experiment_form);
		experiment_form.submit();
	});
	
	experiment_div.append(experiment_element_link_text);
	
	experiments_list.append(experiment_element);
}

$(function(){

    $(".dropdown > li").hover(function() {
    
         var $container = $(this),
             $list = $container.find("ul"),
             $anchor = $container.find("a"),
             height = $list.height(),       // make sure there is enough room at the bottom
             multiplier = height / maxHeight;     // needs to move faster if list is taller
        
        // need to save height here so it can revert on mouseout            
        $container.data("origHeight", $container.height());
        
        // so it can retain it's rollover color all the while the dropdown is open
        $anchor.addClass("hover");
        
        // make sure dropdown appears directly below parent list item    
        $list
            .show()
            .css({
                paddingTop: $container.data("origHeight")
            });
        
        // don't do any animation if list shorter than max
        if (multiplier > 1) {
            $container
                .css({
                    height: maxHeight,
                    overflow: "hidden"
                })
                .mousemove(function(e) {
                    var offset = $container.offset();
                    var relativeY = ((e.pageY - offset.top) * multiplier) - ($container.data("origHeight") * multiplier);
                    if (relativeY > $container.data("origHeight")) {
                        $list.css("top", -relativeY + $container.data("origHeight"));
                    };
                });
        }
        
    }, function() {
    
        var $el = $(this);
        
        // put things back to normal
        $el
            .height($(this).data("origHeight"))
            .find("ul")
            .css({ top: 0 })
            .hide()
            .end()
            .find("a")
            .removeClass("hover");
    
    });
    
    // Add down arrow only to menu items with submenus
    /*
    $(".dropdown > li:has('ul')").each(function() {
        $(this).find("a:first").append("<img src='images/down-arrow.png' />");
    });
    */
    
});