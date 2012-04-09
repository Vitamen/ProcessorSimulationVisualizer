var chart;
var parsed_names = new Array();
var parsed_data = new Array();

var i = 0;

for (var key in core_data) {
	var data_item = core_data[key];
	for (var parsed_key in data_item) {
		parsed_names[i] = parsed_key.replace("Z",".");
		parsed_data[i++] = data_item[parsed_key];
	}
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container4',
            type: 'line'
        },
        title: {
            text: '100M_np_base benchmark chart for core_insn_fetched'
        },
        xAxis: {
            categories:parsed_names,
            labels: {
                rotation: -90,
                align: 'right'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Metric'
            }
        },
        legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
        },
        tooltip: {
            formatter: function() {
                return ''+
                    this.x +': '+ this.y +' mm';
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
            series: [{
            name: 'Experiment 1',
            data: parsed_data

        },]
    });
});