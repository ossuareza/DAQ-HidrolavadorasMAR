import os

def generate_html(pump):

    path_to_imgs = os.path.join("data", "imgs")

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

    """
    print(path_to_imgs)
    html_content += f"""

    <body>
    <table cellspacing="0" >
        <colgroup span="8" ></colgroup>
        <tr>
            <td colspan=2 height="50"><img src="../../data/imgs/logo.png" alt="Hidrolavadoras MAR Image" width="200" height="34"></td>
            <td class="td_top" align="center">Velocidad n (rpm)<br><br>{pump["motor_speed"]}</td>
            <td class="td_top" align="center">Potencia P(kW)<br><br>{pump["power"]}</td>
            <td class="td_top" colspan=2>Número del parqueadero:<br><br><br>{pump["parking_slot"]}</td>
            <td class="td_top" colspan=2>Número orden del servicio:<br><br><br>{pump["service_order"]}</td>
            </tr>
        <tr class="td_top">
            <td height="50" colspan=2 align="left">Fecha de la prueba:<br><br>{pump["date"]}</td>
            <td colspan=2 align="left">Encargado:<br><br>{pump["delegate"]}</td>
            <td colspan=2 align="left">Número de modelo de la bomba:<br>{pump["model"]}</td>
            <td colspan=2 align="left">Test número:<br><br>{pump["test_number"]}</td>
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

    """

    for i in range(len(pump["flow"])):
        html_content += f"""
            <tr>
                <td align="center">{i+1}</td>
                <td align="center">{pump["flow"][i]}</td>
                <td align="center">{pump["pressure"][i]}</td>
                <td align="center">{pump["velocity"][i]}</td>
                <td align="center">{pump["elevation"][i]}</td>
                <td align="center">{pump["pump_total"][i]}</td>
                <td align="center">{pump["pump_power"][i]}</td>
                <td align="center">{pump["pump_efficiency"][i]}</td>
            </tr>
            """
    html_content += f"""
        <tr>
            <td colspan=3 align="center" >Punto de garantía</td>
            <td colspan=5 rowspan=5 align="left"><font size=4>Este test fue desarrollado con agua limpia a (Inserte Temperatura) (temperatura ambiente). La cabeza, el flujo y la potencia fueron medidas con instrumentación electrónica y la exactitud de los resultados ha sido corroborada</font></td>
            </tr>
        <tr>
            <td align="center" >Flujo</td>
            <td align="center" >{pump["final_flow"]}</td>
            <td align="center" >m²/s</td>
            </tr>
        <tr>
            <td align="center" >Cabeza</td>
            <td align="center" >{pump["final_head"]}</td>
            <td align="center" >m</td>
            </tr>
        <tr >
            <td align="center" >Eficiencia</td>
            <td align="center" >{pump["final_efficiency"]}</td>
            <td align="center" >%</td>
            </tr>
        <tr class="break-after">
            <td align="center" >Cabeza Máxima</td>
            <td align="center" >{max(pump["pressure"])}</td>
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
    path_to_file = os.path.join("data", "html", file_name)

    print(path_to_file)

    with open(path_to_file, "w") as html_file:
        # Write the HTML content to the file
        html_file.write(html_content)

    print(f"HTML file '{file_name}' generated successfully.")