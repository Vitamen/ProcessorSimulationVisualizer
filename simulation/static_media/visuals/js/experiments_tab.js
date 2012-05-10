$(".experiment_checkbox").each(function() {
	$(this).click(function() {
		metric_should_update = true;
		benchmark_should_update = true;
	})
})