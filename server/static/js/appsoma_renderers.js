renderFunctions['appsoma_test_alive'] = render_web_response_time;

function render_appsoma_cpu( data, notes, element, time ) 
{
	if( data.length < 1 ) return;
	
	var types = [];

	for( var i in data[0]['value'] )
	{
		types.push( i );
	}
	
	blank = {};
	for( var i = 0; i < types.length; i++ ) { blank[types[i]] = 0; }
	data = add_zero_data_in_gaps( data, blank, time );

	var palette = new Rickshaw.Color.Palette();
	var series = [];
	
	for( var type in types )
	{
		var type = types[type];
		var rickData = [];
		for( var i = 0; i < data.length; i++ )
		{
			var x = data[i]['time'];
			var y = data[i]['value'][type];
			rickData.push( { x: x, y: y } );
		}
		series.push( { name: type, data: rickData, color: palette.color() } );
	}	
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'stack',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );
	
	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['appsoma_cpu'] = render_appsoma_cpu;