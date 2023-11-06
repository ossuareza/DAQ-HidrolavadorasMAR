from guizero import App, TextBox, PushButton, Text, info, error, Picture, ButtonGroup, Box

def change_screen(screens):

    global screen_counter
    screen_counter += 1
    # Hide all screens
    for s in screens:
        s.hide()
    # Show the selected screen
    screens[screen_counter % len(screens)].show()

# Function to update measurements
def update_measurements():
    # Replace these with actual measurements
    flow_display.value = f"Flujo: {42.5} m³/s"
    head_display.value = f"Cabeza: {3.2} m"
    efficiency_display.value = f"Eficiencia: {93.8}%"
    temperature_display.value = f"Temperatura: {25.5} °C"

# Initialize the app
app = App("Test Interface", width=600, height=400)

initial_information = Box(app, layout="grid")
show_measurements = Box(app, layout="grid")
generate_report = Box(app, layout="grid")


logo = Picture(app, image="data/imgs/logo.png")

title = Text(app, text="Caracterizador de hidrolavadoras")

subtitle = Text(initial_information, text="Información inicial", grid=[0,1,3,1])

# Create string input fields
pump_type = Text(initial_information, text="¿Qué tipo de bomba se va a caracterizar?", grid=[0,1,3,1])
choice = ButtonGroup(initial_information, options=["Rotodinámica", "Desplazamiento lineal"], grid=[0,1,3,1])

date = Text(initial_information, text="Fecha de prueba:", grid=[0,2], align="left")
date_input = TextBox(initial_information, text="Fecha de prueba:", grid=[1,2], align="left")

delegate = Text(initial_information, text="Nombre del encargado:", grid=[2,2], align="left")
delegate_input = TextBox(initial_information, text="Nombre del encargado:", grid=[3,2], align="left")

pump_model = Text(initial_information, text="Modelo de la bomba:", grid=[4,2], align="left")
pump_modelo_input = TextBox(initial_information, text="Modelo de la bomba:", grid=[5,2], align="left")

# Create measurement displays
flow_display = Text(show_measurements, text="Flujo: 0 m³/s", grid=[0,4,3,1])
head_display = Text(show_measurements, text="Cabeza: 0 m", grid=[0,5,3,1])
efficiency_display = Text(show_measurements, text="Eficiencia: 0 %", grid=[0,6,3,1])
temperature_display = Text(show_measurements, text="Temperatura: 0 °C", grid=[0,7,3,1])


# Create a button to update measurements
update_button = PushButton(show_measurements, update_measurements, text="Actualizar Medidas", grid=[0,8])

# Create a button for the step process
step_button = PushButton(show_measurements, text="Iniciar Proceso", grid=[0,9])

# Function to handle the step process
def next_step():
    # Replace this with your step logic
    info("Siguiente paso", "Cierre la válvula")
    info("Siguiente paso", "Tome la medición")
    info("Siguiente paso", "Cierre la válvula")
    info("Siguiente paso", "Tome la medición")
    info("Siguiente paso", "Genere informe")

# Set the function to execute when the step button is clicked
step_button.when_clicked = next_step

# Function to handle high pressure alert
def high_pressure_alert():
    # Replace this with your high pressure alert logic
    error("Alerta de Presión Alta", "La presión ha alcanzado un nivel crítico")

# Create a button to trigger high pressure alert
alert_button = PushButton(show_measurements, high_pressure_alert, text="Alerta de Presión Alta", grid=[0,10])


# Define a list of screens
screens = [initial_information, show_measurements, generate_report]

screen_counter = -1

# Initially, hide all screens except the first one
change_screen(screens)

screen_changer = PushButton(app, text="Show Screen 1", command=lambda: change_screen(screens))
# Display the app
app.display()



