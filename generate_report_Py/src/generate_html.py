import os
import sys

def generate_html(pump):

    script_path = os.path.abspath(sys.argv[0])
    src_path = os.path.dirname(script_path)
    directory_path = os.path.dirname(src_path)

    path_to_imgs = os.path.join(directory_path, "data", "imgs")

    flow_vs_power_path = os.path.join(directory_path, "data", "imgs", "FlowVsPower.png")
    flow_vs_efficiency_path = os.path.join(directory_path, "data", "imgs", "FlowVsEfficiency.png")
    flow_vs_head_path = os.path.join(directory_path, "data", "imgs", "FlowVsHead.png")

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
            <td class="td_top" align="center">Potencia P(W)<br><br>{pump["power"]}</td>
            <td class="td_top" colspan=2>Número del parqueadero:<br><br><br>{pump["parking_slot"]}</td>
            <td class="td_top" colspan=2>Número orden del servicio:<br><br><br>{pump["service_order"]}</td>
            </tr>
        <tr class="td_top">
            <td height="50" colspan=2 align="left">Fecha de la prueba:<br><br>{pump["date"]}</td>
            <td colspan=2 align="left">Encargado:<br><br>{pump["delegate"]}</td>
            <td colspan=2 align="left">Modelo de la bomba:<br>{pump["model"]}</td>
            <td colspan=2 align="left">Test número:<br><br>{pump["test_number"]}</td>
            </tr>
        <tr>
            <td rowspan=2 align="center">Medición No.</td>
            <td rowspan=2 align="center">Flujo Q(L/min)</td>
            <td colspan=4 align="center">Cabeza</td>
            <td rowspan=2 align="center">Potencia de entrada P(W)</td>
            <td rowspan=2 align="center">Eficiencia de la bomba (%)</td>
        </tr>
        <tr>
            <td align="center">Presión estática de descarga p(psi)</td>
            <td align="center">Velocidad h_v(m)</td>
            <td align="center">Elevación z(m)</td>
            <td align="center">Cabeza total H(m)</td>
            </tr>

    """

    for i in range(len(pump["flow"])):
        html_content += f"""
            <tr>
                <td align="center">{i+1}</td>
                <td align="center">{round(pump["flow"][i], 2)}</td>
                <td align="center">{round(pump["pressure"][i], 2)}</td>
                <td align="center">{round(pump["velocity"][i], 2)}</td>
                <td align="center">{round(pump["elevation"][i], 2)}</td>
                <td align="center">{round(pump["pump_total"][i], 2)}</td>
                <td align="center">{round(pump["pump_power"][i], 2)}</td>
                <td align="center">{round(pump["pump_efficiency"][i], 2)}</td>
            </tr>
            """
    html_content += f"""
        <tr>
            <td colspan=3 align="center" >Punto de máxima eficiencia</td>
            <td colspan=5 rowspan=5 align="left"><font size=4>Este test fue desarrollado con agua limpia a {pump["temperature"]} °C (temperatura ambiente). La cabeza, el flujo y la potencia fueron medidas con instrumentación electrónica y la exactitud de los resultados ha sido corroborada</font></td>
            </tr>
        <tr>
            <td align="center" >Flujo</td>
            <td align="center" >{round(pump["final_flow"], 2)}</td>
            <td align="center" >L/min</td>
            </tr>
        <tr>
            <td align="center" >Cabeza</td>
            <td align="center" >{round(pump["final_head"], 2)}</td>
            <td align="center" >m</td>
            </tr>
        <tr >
            <td align="center" >Eficiencia</td>
            <td align="center" >{round(pump["final_efficiency"], 2)}</td>
            <td align="center" >%</td>
            </tr>
        <tr class="break-after">
            <td align="center" >Cabeza Máxima</td>
            <td align="center" >{round(max(pump["pressure"]), 2)}</td>
            <td align="center" >m</td>
            </tr>
    </table>
    <table class="new-page" cellspacing="0" >
        <colgroup span="8" ></colgroup>
        <tr >
            <td colspan=8 height="50" align="center" ><img src="{flow_vs_power_path}" alt="Flujo vs Potencia" width="900" height="300"></td>
            </tr>
        <tr>
            <td colspan=8 height="50" align="center" ><img src="{flow_vs_head_path}" alt="Flujo vs Cabeza" width="900" height="300"></td>
            </tr>
        <tr>
            <td colspan=8 height="50" align="center" ><img src="{flow_vs_efficiency_path}" alt="Flujo vs Eficiencia" width="900" height="300"></td>
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