var chart;
var parsed_names = new Array();
var parsed_data = new Array();

var parsed_names_2 = new Array();
var parsed_data_2 = new Array();

var i=0;
for (var key in core_data) {
	var data_item = core_data[key];
	for (var parsed_key in data_item) {
		parsed_names[i] = parsed_key.replace("Z",".");
		parsed_data[i++] = data_item[parsed_key];
	}
}

i=0;
for (var key in core_data_2) {
	var data_item_2 = core_data_2[key];
	for (var parsed_key_2 in data_item_2) {
		parsed_names_2[i] = parsed_key_2.replace("Z",".");
		parsed_data_2[i++] = data_item_2[parsed_key_2];
	}
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container2',
            type: 'column'
        },
        title: {
            text: '100M_np_base benchmark chart for core_insn_fetched and core_insn_fetched_onpath'
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
                text: 'Rainfall (mm)'
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

        }, {
            name: 'Experiment 2',
            data: parsed_data_2
        },
        ]
    });
});