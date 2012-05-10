/* on startup */
$("#metric-link").click(function() {
	if (metric_should_update) {
		populateMetricsList();
		metric_should_update = false;
	}
});

/* populate the metrics list with valid metric types */
function showResponse(responseText, statusText, xhr, $form)  {
	var metric_id = $('#metric_id').attr("value");
	responseText = responseText.replace(/\'/g,"\"").replace(/u/g,"")
	var myjsonObject = JSON.parse(responseText);
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
		if (!metric_loaded) {
			metrics_list.val(metric_id);
		}
		metrics_list.show();
		$("#metric-error-message").hide();
	}
	metric_loaded = true;
}

function populateMetricsList() {
	var options = { 
        url: '/getMetricsOfTypeForExperiments',
        success: showResponse
    }; 
	$("#argForm").ajaxSubmit(options);
}

function selectMetricType(context) {
	var options = { 
        url: '/getMetricsOfTypeForExperiments',
        success: showResponse
    }; 
	$("#argForm").ajaxSubmit(options);
}