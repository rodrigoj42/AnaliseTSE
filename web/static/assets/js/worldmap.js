var icon = "M21.25,8.375V28h6.5V8.375H21.25zM12.25,28h6.5V4.125h-6.5V28zM3.25,28h6.5V12.625h-6.5V28z";

AmCharts.makeChart("mapdiv",{ 
		"type": "map",
		"theme": "light",
		
		colorSteps: 10,
	  /**
	   * create data provider object
	   * map property is usually the same as the name of the map file.
	   * getAreasFromMap indicates that amMap should read all the areas available
	   * in the map data and treat them as they are included in your data provider.
	   * in case you dont set it to true, all the areas except listed in data
	   * provider will be treated as unlisted.
	   */
	
		"dataProvider": {
			"map": "brazilLow",
			areas: [{
				id: "BR-AC",
				value: 167499,
				balloonText: "Acre: 167.499"
			}, {	
				id: "BR-AL",
				value: 356632,
				balloonText: "Alagoas: 356.632"
			}, {	
	
				id: "BR-AM",
				value: 361234,
				balloonText: "Amazonas: 361.234"
			}, {	
				id: "BR-AP",
				value: 77702,
				balloonText: "Amapa: 77.702"
			}, {
				id: "BR-BA",
				value: 1284185,
				balloonText: "Bahia: 1.284.185"
			}, {
				id: "BR-CE",
				value: 638115,
				balloonText: "Ceara: 638.115"
			}, {
				id: "BR-DF",
				value: 563830,
				balloonText: "Distrito Federal: 563.830"
			}, {
				id: "BR-ES",
				value: 567421,
				balloonText: "Espirito Santo: 567.421"
			}, {
				id: "BR-GO",
				value: 771157,
				balloonText: "Goias: 771.157"
			}, {
				id: "BR-MA",
				value: 534824,
				balloonText: "Maranhao: 534.824"
			}, {
				id: "BR-MG",
				value: 1554511,
				balloonText: "Minas Gerais: 1.554.511"
			}, {
				id: "BR-MS",
				value: 257805,
				balloonText: "Mato Grosso do Sul: 257.805"
			}, {
				id: "BR-MT",
				value: 219908,
				balloonText: "Mato Grosso: 219.908"
			}, {
				id: "BR-PA",
				value: 627012,
				balloonText: "Para: 627.012"
			}, {
				id: "BR-PB",
				value: 393390,
				balloonText: "Paraiba: 393.390"
			}, {
				id: "BR-PE",
				value: 2310700,
				balloonText: "Pernambuco: 2.310.700"
			}, {
				id: "BR-PI",
				value: 246121,
				balloonText: "Piaui: 246.121"
			}, {
				id: "BR-PR",
				value: 860685,
				balloonText: "Parana: 860.685"
			}, {
				id: "BR-RJ",
				value: 2590871,
				balloonText: "Rio de Janeiro: 2.590.871"
			}, {
				id: "BR-RN",
				value: 286061,
				balloonText: "Rio Grande do Norte: 286.061"
			}, {
				id: "BR-RO",
				value: 86148,
				balloonText: "Rondonia: 86.148"
			}, {
				id: "BR-RR",
				value: 46936,
				balloonText: "Roraima: 46.936"
			}, {
				id: "BR-RS",
				value: 732148,
				balloonText: "Rio Grande do Sul: 732.148"
			}, {
				id: "BR-SC",
				value: 475599,
				balloonText: "Santa Catarina: 475.599"
			}, {	
				id: "BR-SE",
				value: 203188,
				balloonText: "Sergipe: 203.188"
			}, {	
				id: "BR-SP",
				value: 5761174,
				balloonText: "Sao Paulo: 5.761.174"
			}, {
				id: "BR-TO",
				value: 150568,
				balloonText: "Tocantins: 150.568"
			}]
		},
	
	  /** 
	   * create areas settings
	   * autoZoom set to true means that the map will zoom-in when clicked on the area
	   * selectedColor indicates color of the clicked area.
	   */
	   
		"areasSettings": {
			"autoZoom": true,
		},
	
		valueLegend: {
	   		right: 10,
	    		minValue: "poucos votos",
	    		maxValue: "muitos votos!"
		},
	
	  /**
	   * lets say we want a small map to be displayed, so lets create it
	   */
	   
		"smallMap": {}
	});