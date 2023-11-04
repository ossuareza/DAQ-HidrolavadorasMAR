html_content = """
<!DOCTYPE html>

<html>
<head>
    <meta charset="UTF-8">
	<style type="text/css">

		@import url('https://fonts.googleapis.com/css?family=Montserrat|Open+Sans|Roboto');
		table{
			width: 100%; 
			border-collapse: collapse;
			border: 1px solid black;

		}
.break-after {
    page-break-after: always;
}
		.new-page {
		page-break-before: always;
		}
		td , th{
			padding: 15px 20px;
			border-collapse: collapse;
			border: 1px solid black;;

		}
		.td_top{
			vertical-align: top;
		}
		tr{
			font-family: 'Montserrat', sans-serif;
			font-size: x-small;
		}

	</style>
	
</head>



<body>
<table cellspacing="0" >
	<colgroup span="8" ></colgroup>
	<tr>
		<td colspan=2 height="50"><img src="../../data/imgs/logo.png" alt="Hidrolavadoras MAR Image" width="200" height="34"></td>
		<td class="td_top" align="center">Velocidad n (rpm)<br><br>0</td>
		<td class="td_top" align="center">Potencia P(kW)<br><br>0</td>
		<td class="td_top" colspan=2>Número del parqueadero:<br><br><br>0</td>
		<td class="td_top" colspan=2>Número serial de la bomba:<br><br><br></td>
		</tr>
	<tr class="td_top">
		<td height="50" colspan=2 align="left">Fecha de la prueba:<br><br></td>
		<td colspan=2 align="left">Encargado:<br><br></td>
		<td colspan=2 align="left">Número de modelo de la bomba:<br></td>
		<td colspan=2 align="left">Test número:<br><br>0</td>
		</tr>
	<tr>
		<td rowspan=2 align="center">Medición No.</td>
		<td rowspan=2 align="center">Flujo Q(m²/s)</td>
		<td colspan=4 align="center">Cabeza</td>
		<td rowspan=2 align="center">Potencia de entrada P(kW)</td>
		<td rowspan=2 align="center">Eficiencia de la bomba (%)</td>
	</tr>
	<tr>
		<td align="center">Presión estática p(kPa)</td>
		<td align="center">Velocidad h_v(m)</td>
		<td align="center">Elevación z(m)</td>
		<td align="center">Cabeza total H(m)</td>
		</tr>
	<tr>
		<td align="center">1</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
	</tr>
	<tr>
		<td align="center">2</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
	</tr>
	<tr>
		<td align="center">3</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
	</tr>
	<tr>
		<td align="center">4</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
	</tr>
	<tr>
		<td align="center">5</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
		<td align="center">0</td>
	</tr>
	<tr>
		<td colspan=3 align="center" >Punto de garantía</td>
		<td colspan=5 rowspan=5 align="left"><font size=4>Este test fue desarrollado con agua limpia a (Inserte Temperatura) (temperatura ambiente). La cabeza, el flujo y la potencia fueron medidas con instrumentación electrónica y la exactitud de los resultados ha sido corroborada</font></td>
		</tr>
	<tr>
		<td align="center" >Flujo</td>
		<td align="center" >0</td>
		<td align="center" >m²/s</td>
		</tr>
	<tr>
		<td align="center" >Cabeza</td>
		<td align="center" >0</td>
		<td align="center" >m</td>
		</tr>
	<tr >
		<td align="center" >Eficiencia</td>
		<td align="center" >0</td>
		<td align="center" >%</td>
		</tr>
	<tr class="break-after">
		<td align="center" >Cabeza Máxima</td>
		<td align="center" >0</td>
		<td align="center" >m</td>
		</tr>
</table>
<table class="new-page" cellspacing="0" >
	<colgroup span="8" ></colgroup>
	<tr >
		<td colspan=8 height="50" align="center" ><img src="../../data/imgs/FlowVsPower.png" alt="Flujo vs Potencia" width="900" height="300"></td>
		</tr>
	<tr>
		<td colspan=8 height="50" align="center" ><img src="../../data/imgs/FlowVsHead.png" alt="Flujo vs Cabeza" width="900" height="300"></td>
		</tr>
	<tr>
		<td colspan=8 height="50" align="center" ><img src="../../data/imgs/FlowVsEfficiency.png" alt="Flujo vs Eficiencia" width="900" height="300"></td>
		</tr>
</table>
<!-- ************************************************************************** -->
</body>

</html>
"""

file_name = "report.html"
with open(file_name, "w") as html_file:
    # Write the HTML content to the file
    html_file.write(html_content)

print(f"HTML file '{file_name}' generated successfully.")