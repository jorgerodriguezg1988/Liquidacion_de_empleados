from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QPdfWriter, QPainter, QPageSize
from PySide6.QtWidgets import QApplication
from __feature__ import snake_case, true_property

from styles import estilos_menu # Se hace el llamado de la hoja de estilos como en CSS



class Liquidacion_empleados(QMainWindow): #Se crea una clase para la ventana para heredar
    
    

    def setup_ui(self): #Se crea el metodo de la VENTANA como tal
        self.size = QSize(1500, 900) # define el tamano de la ventana
        self.set_window_title("Liquidacion de empleados")

        self.root_layout = QVBoxLayout()

        self.fr_titulo = QFrame()
        self.fr_datos_basicos_empleados = QFrame()
        self.fr_periodo_liquidacion = QFrame()
        
        self.root_layout.add_widget(self.fr_titulo, 5)
        self.root_layout.add_widget(self.fr_datos_basicos_empleados,10)
        self.root_layout.add_widget(self.fr_periodo_liquidacion,85)

        self.widget = QWidget()
        self.widget.set_layout(self.root_layout)

        self.set_central_widget(self.widget)
        self.style_sheet = estilos_menu

        self.setup_title_frame()
        self.setup_datos_empleado_frame()
        
        self.guardar_datos_basicos_btn.clicked.connect(self.setup_datos_empl_variable) # Se conecta el metodo para que se ejecute la accion
        #self.setup_datos_empl_variable()
                
        


    def setup_title_frame(self):
        self.titulo_title = QLabel("LIQUIDACION DE EMPLEADOS POR FINALIZACION DE CONTRATO", object_name="titulo_principal", alignment = Qt.AlignCenter)

        self.titulo_layout = QVBoxLayout()
        self.titulo_layout.add_widget(self.titulo_title)
     
        self.fr_titulo.set_layout(self.titulo_layout)

        



    def setup_datos_empleado_frame(self):
        self.grid_datos_empleado = QGridLayout()
        
        
        self.titulo_datos_empleado = QLabel("Digite los datos del empleado: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.nombre_label = QLabel("Nombre completo: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.nombre_input = QLineEdit(placeholder_text = "Nombre", alignment = Qt.AlignLeft)
        self.cedula_label = QLabel("Cedula: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.cedula_input = QLineEdit(placeholder_text = "Cedula", alignment = Qt.AlignLeft)
        self.cargo_label = QLabel("Cargo: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.cargo_input = QLineEdit(placeholder_text = "Cargo", alignment = Qt.AlignLeft)
        self.tipo_retiro_label = QLabel("Tipo de retiro: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.tipo_retiro_combox = QComboBox()
        self.tipo_retiro_combox.add_items(["Opción 1", "Opción 2", "Opción 3"])
        self.guardar_datos_basicos_btn = QPushButton()
        self.guardar_datos_basicos_btn.text = "Guardar Datos de Empleado"
        self.guardar_datos_basicos_btn.style_sheet = "background: #2A88C1"
        
        


        self.grid_datos_empleado.add_widget(self.titulo_datos_empleado, 1, 1)
        self.grid_datos_empleado.add_widget(self.nombre_label, 2, 1)
        self.grid_datos_empleado.add_widget(self.nombre_input, 2, 2)
        self.grid_datos_empleado.add_widget(self.cedula_label, 2, 3)
        self.grid_datos_empleado.add_widget(self.cedula_input, 2, 4)
        self.grid_datos_empleado.add_widget(self.cargo_label, 3, 1)
        self.grid_datos_empleado.add_widget(self.cargo_input, 3, 2)
        self.grid_datos_empleado.add_widget(self.tipo_retiro_label, 3, 3)
        self.grid_datos_empleado.add_widget(self.tipo_retiro_combox, 3, 4)
        self.grid_datos_empleado.add_widget(self.guardar_datos_basicos_btn, 3, 5)


        self.fr_datos_basicos_empleados.set_layout(self.grid_datos_empleado)
        self.inputs_layout = QVBoxLayout()

                

        self.inputs_layout.add_stretch() # Relleno o push para empujar los inputs hacia el frente

        self.fr_datos_basicos_empleados.set_layout(self.inputs_layout)



    def setup_crea_pdf(self):    
    
        #app = QApplication()
        #pdf = QPdfWriter(setup_datos_empleado_frame.prueba_pdf)
        #pdf = QPdfWriter(f"{prueba_pdf}.pdf")
        pdf = QPdfWriter(f"Liquidacion de {self.variable_nombre}.pdf")
        pdf.set_page_size(QPageSize.Letter)
        painter = QPainter(pdf)
        painter.draw_text(4000, 1000, "RESULTADO DE LA LIQUIDACION")
        painter.draw_text(800, 1300, "DATOS DEL EMPLEADO: ")
        painter.draw_text(800, 1800, f"NOMBRE:          {self.variable_nombre}")
        painter.draw_text(2000, 1800, f"DOCUMENTO:       {self.variable_cedula}")
        painter.draw_text(800, 2500, f"CARGO:       {self.variable_cargo}")
        painter.draw_text(2000, 2500, f"MOTIVO DE RETIRO:       {{self.variable_retiro}}")
        #painter.window().width()//2,
        #painter.window().height()//2,
        painter.end()

    def setup_datos_empl_variable(self):
        
        #self.guardar_datos_basicos_btn.clicked.connect(self.setup_datos_empl_variable) # Se conecta el metodo para que se ejecute la accion
        self.variable_nombre = self.nombre_input.text
        self.variable_cedula = self.cedula_input.text
        self.variable_cargo = self.cargo_input.text
        #self.variable_retiro = self.tipo_retiro_combox.text
        self.setup_crea_pdf()










    
        








        
        
        





# Ejecutar la aplicacion Qt
import sys # se importa la libreria sys
app = QApplication(sys.argv)

window = Liquidacion_empleados() # se hace el llamado a la clase
window.setup_ui() # se aplica el tamano definido
window.show() # se muestra






# Cerrar la aplicacion Qt
sys.exit(app.exec())
