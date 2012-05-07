/* on startup */
$("#metric-link").click(function() {
	$.getScript("/static_media/data/metrics.js", function(data, textStatus, jqxhr) {
		eval(data);

	    var options = { 
	        url: '/getMetricsOfTypeForExperiments',
	        success: showResponse
	    }; 
		$("#argForm").ajaxSubmit(options);
	});
});

/* populate the metrics list with valid metric types */
function showResponse(responseText, statusText, xhr, $form)  {
	console.log(responseText);	
	responseText = responseText.replace(/\'/g,"\"").replace(/u/g,"")
	var myjsonObject = JSON.parse(responseText);
	console.log(myjsonObject);
	if (myjsonObject.metrics.length == 0) {
		$("#tab2 label").hide();
		$("#metrics_list").hide();
		$("#metric-error-message").show();
	} else {
		$("#tab2 label").show();
		var metrics_list = $('#metrics_list');
		metrics_list.empty();
		for (var i=0; i < myjsonObject.metrics.length; i++) {
			var metric = myjsonObject.metrics[i];
			var metric_element = $('<option>').append(document.createTextNode(metric));
			metrics_list.append(metric_element);
		}
		metrics_list.show();
		$("#metric-error-message").hide();
	}
}

function selectMetricType(context) {
	console.log($(context).attr("value"))
	var options = { 
        url: '/getMetricsOfTypeForExperiments',
        success: showResponse
    }; 
	$("#argForm").ajaxSubmit(options);
	/*
	$.ajax({
		type: 'POST',
		url: '/getMetricsOfTypeForExperiments',
		data: {
			metric_type: $(context).attr("value")
		},
		success: showResponse
	})*/
}