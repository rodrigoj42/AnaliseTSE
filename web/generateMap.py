def genMap():
	htmlID = "\"mapdiv\""


	json = '{ \n\
		"type": "map",\n\
		"theme": "light",\n\
		\n\
		colorSteps: 10,\n\
	  /**\n\
	   * create data provider object\n\
	   * map property is usually the same as the name of the map file.\n\
	   * getAreasFromMap indicates that amMap should read all the areas available\n\
	   * in the map data and treat them as they are included in your data provider.\n\
	   * in case you dont set it to true, all the areas except listed in data\n\
	   * provider will be treated as unlisted.\n\
	   */\n\
	\n\
		"dataProvider": {\n\
			"map": "brazilLow",\n\
			areas: [{\n\
				id: "BR-AC",\n\
				value: 167499,\n\
				balloonText: "Acre: 167.499"\n\
			}, {	\n\
				id: "BR-AL",\n\
				value: 356632,\n\
				balloonText: "Alagoas: 356.632"\n\
			}, {	\n\
	\n\
				id: "BR-AM",\n\
				value: 361234,\n\
				balloonText: "Amazonas: 361.234"\n\
			}, {	\n\
				id: "BR-AP",\n\
				value: 77702,\n\
				balloonText: "Amapa: 77.702"\n\
			}, {\n\
				id: "BR-BA",\n\
				value: 1284185,\n\
				balloonText: "Bahia: 1.284.185"\n\
			}, {\n\
				id: "BR-CE",\n\
				value: 638115,\n\
				balloonText: "Ceara: 638.115"\n\
			}, {\n\
				id: "BR-DF",\n\
				value: 563830,\n\
				balloonText: "Distrito Federal: 563.830"\n\
			}, {\n\
				id: "BR-ES",\n\
				value: 567421,\n\
				balloonText: "Espirito Santo: 567.421"\n\
			}, {\n\
				id: "BR-GO",\n\
				value: 771157,\n\
				balloonText: "Goias: 771.157"\n\
			}, {\n\
				id: "BR-MA",\n\
				value: 534824,\n\
				balloonText: "Maranhao: 534.824"\n\
			}, {\n\
				id: "BR-MG",\n\
				value: 1554511,\n\
				balloonText: "Minas Gerais: 1.554.511"\n\
			}, {\n\
				id: "BR-MS",\n\
				value: 257805,\n\
				balloonText: "Mato Grosso do Sul: 257.805"\n\
			}, {\n\
				id: "BR-MT",\n\
				value: 219908,\n\
				balloonText: "Mato Grosso: 219.908"\n\
			}, {\n\
				id: "BR-PA",\n\
				value: 627012,\n\
				balloonText: "Para: 627.012"\n\
			}, {\n\
				id: "BR-PB",\n\
				value: 393390,\n\
				balloonText: "Paraiba: 393.390"\n\
			}, {\n\
				id: "BR-PE",\n\
				value: 2310700,\n\
				balloonText: "Pernambuco: 2.310.700"\n\
			}, {\n\
				id: "BR-PI",\n\
				value: 246121,\n\
				balloonText: "Piaui: 246.121"\n\
			}, {\n\
				id: "BR-PR",\n\
				value: 860685,\n\
				balloonText: "Parana: 860.685"\n\
			}, {\n\
				id: "BR-RJ",\n\
				value: 2590871,\n\
				balloonText: "Rio de Janeiro: 2.590.871"\n\
			}, {\n\
				id: "BR-RN",\n\
				value: 286061,\n\
				balloonText: "Rio Grande do Norte: 286.061"\n\
			}, {\n\
				id: "BR-RO",\n\
				value: 86148,\n\
				balloonText: "Rondonia: 86.148"\n\
			}, {\n\
				id: "BR-RR",\n\
				value: 46936,\n\
				balloonText: "Roraima: 46.936"\n\
			}, {\n\
				id: "BR-RS",\n\
				value: 732148,\n\
				balloonText: "Rio Grande do Sul: 732.148"\n\
			}, {\n\
				id: "BR-SC",\n\
				value: 475599,\n\
				balloonText: "Santa Catarina: 475.599"\n\
			}, {	\n\
				id: "BR-SE",\n\
				value: 203188,\n\
				balloonText: "Sergipe: 203.188"\n\
			}, {	\n\
				id: "BR-SP",\n\
				value: 5761174,\n\
				balloonText: "Sao Paulo: 5.761.174"\n\
			}, {\n\
				id: "BR-TO",\n\
				value: 150568,\n\
				balloonText: "Tocantins: 150.568"\n\
			}]\n\
		},\n\
	\n\
	  /** \n\
	   * create areas settings\n\
	   * autoZoom set to true means that the map will zoom-in when clicked on the area\n\
	   * selectedColor indicates color of the clicked area.\n\
	   */\n\
	   \n\
		"areasSettings": {\n\
			"autoZoom": true,\n\
		},\n\
	\n\
		valueLegend: {\n\
	   		right: 10,\n\
	    		minValue: "poucos votos",\n\
	    		maxValue: "muitos votos!"\n\
		},\n\
	\n\
	  /**\n\
	   * lets say we want a small map to be displayed, so lets create it\n\
	   */\n\
	   \n\
		"smallMap": {}\n\
	}'

	lines = ['var icon = "M21.25,8.375V28h6.5V8.375H21.25zM12.25,28h6.5V4.125h-6.5V28zM3.25,28h6.5V12.625h-6.5V28z";\n\n','AmCharts.makeChart('+htmlID+','+json+');']

	worldmap = open("./static/assets/js/worldmap.js",'w')

	worldmap.writelines(lines)

	worldmap.close()