from base64 import a85encode
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QPdfWriter, QPainter, QPageSize, QIntValidator
from PySide6.QtWidgets import QApplication
from __feature__ import snake_case, true_property
from datetime import datetime, date, time, timedelta
import calendar
import math

from styles import estilos_menu # Se hace el llamado de la hoja de estilos como en CSS

class Liquidacion_empleados(QMainWindow): #Se crea una clase para la ventana para heredar
    
    def setup_ui(self): #Se crea el metodo de la VENTANA como tal
        self.size = QSize(1500, 900) # define el tamano de la ventana
        self.set_window_title("Liquidacion de empleados")

        self.root_layout = QVBoxLayout()

        self.fr_titulo = QFrame()
        self.fr_datos_basicos_empleados = QFrame()
        self.fr_conceptos_a_pagar = QFrame()
        self.fr_siguiente_frame = QFrame()
        
        self.root_layout.add_widget(self.fr_titulo, 5)
        self.root_layout.add_widget(self.fr_datos_basicos_empleados,20)
        self.root_layout.add_widget(self.fr_conceptos_a_pagar,40)
        self.root_layout.add_widget(self.fr_siguiente_frame,35)


        self.widget = QWidget()
        self.widget.set_layout(self.root_layout)

        self.set_central_widget(self.widget)
        self.style_sheet = estilos_menu

        self.setup_title_frame()
        self.setup_datos_empleado_frame()
        self.setup_conceptos_a_pagar_frame()
        
        
        self.guardar_datos_basicos_btn.clicked.connect(self.setup_total_dias_contrato) # Se conecta el metodo para que se ejecute la accion
        self.guardar_datos_basicos_btn.clicked.connect(self.setup_datos_empl_variable) # Se conecta el metodo para que se ejecute la accion
        self.generar_calculos_btn.clicked.connect(self.setup_calculos_conceptos_a_pagar) # Se conecta el metodo para que se ejecute la accion
        self.generar_calculos_btn.clicked.connect(self.setup_descuento_sancion) # Se conecta el metodo para que se ejecute la accion
        
        

        
        
                
        


    def setup_title_frame(self):
        self.titulo_title = QLabel("LIQUIDACION DE EMPLEADOS POR FINALIZACION DE CONTRATO", object_name="titulo_principal", alignment = Qt.AlignCenter)

        self.titulo_layout = QVBoxLayout()
        self.titulo_layout.add_widget(self.titulo_title)
     
        self.fr_titulo.set_layout(self.titulo_layout)

    def setup_datos_empleado_frame(self):
        self.grid_datos_empleado = QGridLayout()
        
        self.titulo_datos_empleado = QLabel("Digite los datos del empleado: ", object_name="subtitulos_principales", alignment = Qt.AlignLeft)
        self.nombre_label = QLabel("Nombre completo: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.nombre_input = QLineEdit(placeholder_text = "Nombre", alignment = Qt.AlignLeft)
        self.cedula_label = QLabel("Cedula: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.cedula_input = QLineEdit(placeholder_text = "Cedula", alignment = Qt.AlignLeft)
        self.cargo_label = QLabel("Cargo: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.cargo_input = QLineEdit(placeholder_text = "Cargo", alignment = Qt.AlignLeft)
        self.tipo_retiro_label = QLabel("Tipo de retiro: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.tipo_retiro_combox = QComboBox()
        self.tipo_retiro_combox.add_items(["Retiro Voluntario", "Terminacion de contrato con justa causa", "Abandono de puesto"])
        self.fecha_ini_label = QLabel("Fecha inicio contrato: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_ini_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.fecha_fin_label = QLabel("Fecha final contrato: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_fin_input = QLineEdit(placeholder_text = "dd-mm-aaaa",alignment = Qt.AlignLeft)
        self.salario_base_label = QLabel("Salario base del empleado: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.salario_base_input = QLineEdit(placeholder_text = "Valor sin puntos ni comas", alignment = Qt.AlignLeft)
        self.auxilio_trans_label = QLabel("Auxilio de transporte: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.auxilio_trans_input = QLineEdit(placeholder_text = "Valor sin puntos ni comas", alignment = Qt.AlignLeft)
        self.titulo_dias_trabajados_label = QLabel("Total dias trabajados: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_trabajados_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.dias_trabajados_label.hide()
        self.guardar_datos_basicos_btn = QPushButton()
        self.guardar_datos_basicos_btn.text = "Guardar Datos"
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
        self.grid_datos_empleado.add_widget(self.fecha_ini_label, 4, 1)
        self.grid_datos_empleado.add_widget(self.fecha_ini_input, 4, 2)
        self.grid_datos_empleado.add_widget(self.fecha_fin_label, 4, 3)
        self.grid_datos_empleado.add_widget(self.fecha_fin_input, 4, 4)
        self.grid_datos_empleado.add_widget(self.salario_base_label, 5, 1)
        self.grid_datos_empleado.add_widget(self.salario_base_input, 5, 2)
        self.grid_datos_empleado.add_widget(self.auxilio_trans_label, 5, 3)
        self.grid_datos_empleado.add_widget(self.auxilio_trans_input, 5, 4)
        self.grid_datos_empleado.add_widget(self.titulo_dias_trabajados_label, 6, 1)
        self.grid_datos_empleado.add_widget(self.dias_trabajados_label, 6, 2)
        self.grid_datos_empleado.add_widget(self.guardar_datos_basicos_btn, 6, 6)

        self.fr_datos_basicos_empleados.set_layout(self.grid_datos_empleado)
        self.inputs_empleado_layout = QVBoxLayout()
        self.inputs_empleado_layout.add_stretch() # Relleno o push para empujar los inputs hacia el frente
        
        self.fr_datos_basicos_empleados.set_layout(self.inputs_empleado_layout)

        
    def setup_conceptos_a_pagar_frame(self):
        self.grid_conceptos_a_pagar = QGridLayout()
        
        self.titulo_conceptos_a_pagar = QLabel("Conceptos a pagar: ", object_name="subtitulos_principales", alignment = Qt.AlignLeft)
        self.fecha_ini_salario_pend_label = QLabel("Fecha inicio de ultimo salario: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_ini_salario_pend_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.fecha_fin_salario_pend_label = QLabel("Fecha final de ultimo salario: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_fin_salario_pend_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.titulo_dias_pendientes_salario = QLabel("Total dias del ultimo salario: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_pendientes_salario_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.dias_pendientes_salario_label.hide()
        self.titulo_dias_pendientes_auxilio = QLabel("Auxilio de transporte por dias del ultimo salario: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_pendientes_auxilio_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.dias_pendientes_auxilio_label.hide()
        self.dias_sancion_label = QLabel("Dias de sanción: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_sancion_input = QLineEdit(placeholder_text = "Cantidad de dias de sancion", alignment = Qt.AlignLeft)
        self.dias_sancion_input.set_validator(QIntValidator(0, 9999, self.dias_sancion_input))
        self.horas_extras_label = QLabel("Horas Extras: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.horas_extras_input = QLineEdit(placeholder_text = "Cantidad de horas extras", alignment = Qt.AlignLeft)
        self.horas_extras_input.set_validator(QIntValidator(0, 9999, self.horas_extras_input))
        self.fecha_ini_prima_label = QLabel("Fecha inicio de periodo para prima: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_ini_prima_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.fecha_fin_prima_label = QLabel("Fecha final de periodo para prima: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_fin_prima_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.titulo_dias_pendientes_prima = QLabel("Total dias a pagar por prima: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_pendientes_prima_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.dias_pendientes_prima_label.hide()
        self.fecha_ini_cesantias_label = QLabel("Fecha inicio de periodo para cesatias: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_ini_cesantias_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.fecha_fin_cesantias_label = QLabel("Fecha final de periodo para cesantias: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.fecha_fin_cesantias_input = QLineEdit(placeholder_text = "dd-mm-aaaa", alignment = Qt.AlignLeft)
        self.titulo_dias_pendientes_cesantias = QLabel("Total dias a pagar por cesantias: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_pendientes_cesantias_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.dias_pendientes_cesantias_label.hide()
        self.titulo_dias_total_vacaciones_label = QLabel("Total dias de vacaciones: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_total_vacaciones_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.titulo_dias_usados_vacaciones_label = QLabel("Dias de vacaciones disfrutados: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_usados_vacaciones_input = QLineEdit(placeholder_text = "Cantidad de dias de vacaciones disfrutados", alignment = Qt.AlignLeft)
        self.dias_usados_vacaciones_input.set_validator(QIntValidator(0, 9999, self.dias_usados_vacaciones_input))
        self.titulo_dias_pendientes_vacaciones_label = QLabel("Dias de vacaciones pendientes: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.dias_pendientes_vacaciones_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.dias_pendientes_vacaciones_label.hide()
        self.generar_calculos_btn = QPushButton()
        self.generar_calculos_btn.text = "Generar Calculos"
        self.generar_calculos_btn.style_sheet = "background: #2A88C1"
        
        self.grid_conceptos_a_pagar.add_widget(self.titulo_conceptos_a_pagar, 1, 1)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_ini_salario_pend_label, 2, 1)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_ini_salario_pend_input, 2, 2)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_fin_salario_pend_label, 2, 3)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_fin_salario_pend_input, 2, 4)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_pendientes_salario, 2, 5)
        self.grid_conceptos_a_pagar.add_widget(self.dias_pendientes_salario_label, 2, 6)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_pendientes_auxilio, 3, 1)
        self.grid_conceptos_a_pagar.add_widget(self.dias_pendientes_auxilio_label, 3, 2)
        self.grid_conceptos_a_pagar.add_widget(self.dias_sancion_label, 3, 3)
        self.grid_conceptos_a_pagar.add_widget(self.dias_sancion_input, 3, 4)
        self.grid_conceptos_a_pagar.add_widget(self.horas_extras_label, 3, 5)
        self.grid_conceptos_a_pagar.add_widget(self.horas_extras_input, 3, 6)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_ini_prima_label, 5, 1)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_ini_prima_input, 5, 2)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_fin_prima_label, 5, 3)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_fin_prima_input, 5, 4)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_pendientes_prima, 5, 5)
        self.grid_conceptos_a_pagar.add_widget(self.dias_pendientes_prima_label, 5, 6)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_ini_cesantias_label, 6, 1)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_ini_cesantias_input, 6, 2)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_fin_cesantias_label, 6, 3)
        self.grid_conceptos_a_pagar.add_widget(self.fecha_fin_cesantias_input, 6, 4)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_pendientes_cesantias, 6, 5)
        self.grid_conceptos_a_pagar.add_widget(self.dias_pendientes_cesantias_label, 6, 6)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_total_vacaciones_label, 7, 1)
        self.grid_conceptos_a_pagar.add_widget(self.dias_total_vacaciones_label, 7, 2)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_usados_vacaciones_label, 7, 3)
        self.grid_conceptos_a_pagar.add_widget(self.dias_usados_vacaciones_input, 7, 4)
        self.grid_conceptos_a_pagar.add_widget(self.titulo_dias_pendientes_vacaciones_label, 7, 5)
        self.grid_conceptos_a_pagar.add_widget(self.dias_pendientes_vacaciones_label, 7, 6)
        self.grid_conceptos_a_pagar.add_widget(self.generar_calculos_btn, 8, 6)
        
        self.fr_conceptos_a_pagar.set_layout(self.grid_conceptos_a_pagar)
        self.inputs_conceptos_a_pagar_layout = QVBoxLayout()
        self.inputs_conceptos_a_pagar_layout.add_stretch()
        


    def setup_crea_pdf(self):    
    
        pdf = QPdfWriter(f"Liquidacion de {self.nombre_input.text}.pdf")
        pdf.set_page_size(QPageSize.Letter)
        painter = QPainter(pdf)
        painter.draw_text(4000, 1000, "RESULTADO DE LA LIQUIDACION")
        painter.draw_text(0, 1200, "_____________________________________________________________________________________________________________________________________________________________")
        painter.draw_text(800, 1500, "DATOS DEL EMPLEADO: ")
        painter.draw_text(800, 1900, f"NOMBRE:      {self.nombre_input.text}")
        painter.draw_text(5500, 1900, f"DOCUMENTO:               {self.cedula_input.text}")
        painter.draw_text(800, 2200, f"CARGO:        {self.cargo_input.text}")
        painter.draw_text(5500, 2200, f"MOTIVO DE RETIRO:       {self.tipo_retiro_combox.current_text}")
        painter.draw_text(800, 2500, f"FECHA INICIO DE CONTRATO:        {self.fecha_ini_input.text}")
        painter.draw_text(5500, 2500, f"FECHA FIN DE CONTRATO:       {self.fecha_fin_input.text}")
        painter.draw_text(800, 2800, f"SALARIO BASE DEL EMPLEADO:        $ {self.salario_base_input.text}")
        painter.draw_text(5500, 2800, f"AUXILIO DE TRANSPORTE:       $ {self.auxilio_trans_input.text}")
        #painter.window().width()//2,
        #painter.window().height()//2,
        painter.end()

    def setup_datos_empl_variable(self):
        """
        self.guardar_datos_basicos_btn.clicked.connect(self.setup_datos_empl_variable) # Se conecta el metodo para que se ejecute la accion
        self.variable_nombre = self.nombre_input.text
        self.variable_cedula = self.cedula_input.text
        self.variable_cargo = self.cargo_input.text
        self.variable_retiro = self.tipo_retiro_combox.current_text
        self.variable_fecha_ini = self.fecha_ini_input.text
        self.variable_fecha_fin = self.fecha_fin_input.text
        self.variable_salario_base = self.salario_base_input.text
        self.variable_auxilio_trans = self.auxilio_trans_input.text
        """
        #self.setup_crea_pdf()

    def setup_total_dias_contrato(self):
        
        self.formato_fecha = "%d-%m-%Y"
        self.variable_fecha_ini_contrato = datetime.strptime(self.fecha_ini_input.text, self.formato_fecha)
        self.variable_fecha_fin_contrato = datetime.strptime(self.fecha_fin_input.text, self.formato_fecha)
        self.dias_total_contrato = self.variable_fecha_fin_contrato - self.variable_fecha_ini_contrato
        
        if self.dias_total_contrato.days >= 0:
            
            self.dias_total_contrato = self.dias_total_contrato.days
            self.dias_trabajados_label.show()
            self.dias_trabajados_label.set_text(f"{self.dias_total_contrato}")
            self.dias_total_contrato_360 = (self.dias_total_contrato / 365) * 360
            
        else:
            self.setup_warning()


    def setup_calculos_conceptos_a_pagar(self):
        self.formato_fecha = "%d-%m-%Y"
        self.variable_fecha_ini_salario_pend = datetime.strptime(self.fecha_ini_salario_pend_input.text, self.formato_fecha)
        self.variable_fecha_fin_salario_pend = datetime.strptime(self.fecha_fin_salario_pend_input.text, self.formato_fecha)
        self.variable_dias_pendientes_salario = self.variable_fecha_fin_salario_pend - self.variable_fecha_ini_salario_pend
        self.variable_dias_pendientes_salario = self.variable_dias_pendientes_salario.days + 1
        print(self.variable_dias_pendientes_salario)
        self.variable_dias_pendientes_auxilio = self.variable_dias_pendientes_salario
        print(self.variable_dias_pendientes_auxilio)
        self.variable_fecha_ini_prima = datetime.strptime(self.fecha_ini_prima_input.text, self.formato_fecha)
        self.variable_fecha_fin_prima = datetime.strptime(self.fecha_fin_prima_input.text, self.formato_fecha)
        self.variable_dias_pendientes_prima = self.variable_fecha_fin_prima - self.variable_fecha_ini_prima
        self.variable_dias_pendientes_prima = self.variable_dias_pendientes_prima.days + 3 # ultimo dia laborado mas 2 dias de febrero
        if "-01-" in self.fecha_ini_prima_input.text or "-02-" in self.fecha_ini_prima_input.text or "-03-" in self.fecha_ini_prima_input.text or "-04-" in self.fecha_ini_prima_input.text or "-05-" in self.fecha_ini_prima_input.text or "-06-" in self.fecha_ini_prima_input.text:
            self.variable_dias_pendientes_prima = (self.variable_dias_pendientes_prima / 365) * 361
            self.variable_dias_pendientes_prima = math.floor(self.variable_dias_pendientes_prima)
            print(self.variable_dias_pendientes_prima)
        else:
            if "-07-" in self.fecha_ini_prima_input.text or "-08-" in self.fecha_ini_prima_input.text or "-09-" in self.fecha_ini_prima_input.text or "-10-" in self.fecha_ini_prima_input.text or "-11-" in self.fecha_ini_prima_input.text or "-12-" in self.fecha_ini_prima_input.text:
                self.variable_dias_pendientes_prima = self.variable_dias_pendientes_prima - 2 # por ser el segundo semestre se le restan los dos dias que se agregaron de Febrero
                self.variable_dias_pendientes_prima = (self.variable_dias_pendientes_prima / 365) * 359
                self.variable_dias_pendientes_prima = math.floor(self.variable_dias_pendientes_prima)
                print(self.variable_dias_pendientes_prima)
            
        self.variable_fecha_ini_cesantias = datetime.strptime(self.fecha_ini_cesantias_input.text, self.formato_fecha)
        self.variable_fecha_fin_cesantias = datetime.strptime(self.fecha_fin_cesantias_input.text, self.formato_fecha)
        self.variable_dias_pendientes_cesantias = self.variable_fecha_fin_cesantias - self.variable_fecha_ini_cesantias
        self.variable_dias_pendientes_cesantias = self.variable_dias_pendientes_cesantias.days + 3 #ultimo dia laborado mas 2 dias de febrero
        if self.variable_dias_pendientes_cesantias <= 183:
            self.variable_dias_pendientes_cesantias = (self.variable_dias_pendientes_cesantias / 365) * 361
            self.variable_dias_pendientes_cesantias = math.floor(self.variable_dias_pendientes_cesantias)
            print(self.variable_dias_pendientes_cesantias)
        else:
            self.variable_dias_pendientes_cesantias = self.variable_dias_pendientes_cesantias - 1
            self.variable_dias_pendientes_cesantias = (self.variable_dias_pendientes_cesantias / 365) * 360
            self.variable_dias_pendientes_cesantias = math.floor(self.variable_dias_pendientes_cesantias)
            print(self.variable_dias_pendientes_cesantias)


        self.variable_dias_total_vacaciones = (self.dias_total_contrato_360 / 360) * 15
        self.variable_dias_usados_vacaciones_input_int = int(self.dias_usados_vacaciones_input.text)
        self.variable_dias_pendientes_vacaciones = self.variable_dias_total_vacaciones - self.variable_dias_usados_vacaciones_input_int
        print(self.variable_dias_pendientes_vacaciones)

        if self.variable_dias_pendientes_salario > 0 and self.variable_dias_pendientes_auxilio > 0 and self.variable_dias_pendientes_prima > 0 and self.variable_dias_pendientes_cesantias > 0:
            self.dias_pendientes_salario_label.show()
            self.dias_pendientes_salario_label.set_text(f"{self.variable_dias_pendientes_salario}")
            self.dias_pendientes_auxilio_label.show()
            self.dias_pendientes_auxilio_label.set_text(f"{self.variable_dias_pendientes_auxilio}")
            self.dias_pendientes_prima_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_prima}")
            self.dias_pendientes_cesantias_label.show()
            self.dias_pendientes_cesantias_label.set_text(f"{self.variable_dias_pendientes_cesantias}")
            self.dias_total_vacaciones_label.set_text("{:.2f}".format(self.variable_dias_total_vacaciones))
            self.dias_pendientes_vacaciones_label.show()
            self.dias_pendientes_vacaciones_label.set_text("{:.2f}".format(self.variable_dias_pendientes_vacaciones))

        else:
            self.setup_warning()
        """
        self.formato_fecha = "%d-%m-%Y"
        self.variable_fecha_ini_salario_pend = datetime.strptime(self.fecha_ini_salario_pend_input.text, self.formato_fecha)
        self.variable_fecha_fin_salario_pend = datetime.strptime(self.fecha_fin_salario_pend_input.text, self.formato_fecha)
        self.variable_dias_pendientes_salario = (self.variable_fecha_fin_salario_pend - self.variable_fecha_ini_salario_pend)
        self.variable_dias_sancion_input_int = int(self.dias_sancion_input.text)
        
        if self.variable_dias_sancion_input_int > self.variable_dias_pendientes_salario.days:
            self.variable_dias_pendientes_salario = 0
        else:
            self.variable_dias_pendientes_salario = (self.variable_dias_pendientes_salario.days - self.variable_dias_sancion_input_int)
        
        self.variable_dias_pendientes_auxilio = self.variable_dias_pendientes_salario
        self.variable_fecha_ini_prima = datetime.strptime(self.fecha_ini_prima_input.text, self.formato_fecha)
        self.variable_fecha_fin_prima = datetime.strptime(self.fecha_fin_prima_input.text, self.formato_fecha)
        self.variable_dias_pendientes_prima = self.variable_fecha_fin_prima - self.variable_fecha_ini_prima
        self.variable_fecha_ini_cesantias = datetime.strptime(self.fecha_ini_cesantias_input.text, self.formato_fecha)
        self.variable_fecha_fin_cesantias = datetime.strptime(self.fecha_fin_cesantias_input.text, self.formato_fecha)
        self.variable_dias_pendientes_cesantias = self.variable_fecha_fin_cesantias - self.variable_fecha_ini_cesantias
        self.variable_dias_total_vacaciones = (self.dias_total_contrato / 360) * 15
        self.variable_dias_usados_vacaciones_input_int = int(self.dias_usados_vacaciones_input.text)
        self.variable_dias_pendientes_vacaciones = self.variable_dias_total_vacaciones - self.variable_dias_usados_vacaciones_input_int
        

        if self.variable_dias_pendientes_salario > 0 and self.variable_dias_pendientes_auxilio > 0 and self.variable_dias_pendientes_prima.days > 0 and self.variable_dias_pendientes_cesantias.days > 0:
            self.dias_pendientes_salario_label.show()
            self.dias_pendientes_salario_label.set_text(f"{self.variable_dias_pendientes_salario}")
            self.dias_pendientes_auxilio_label.show()
            self.dias_pendientes_auxilio_label.set_text(f"{self.variable_dias_pendientes_auxilio}")
            self.dias_pendientes_prima_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_prima.days}")
            self.dias_pendientes_cesantias_label.show()
            self.dias_pendientes_cesantias_label.set_text(f"{self.variable_dias_pendientes_cesantias.days}")
            self.dias_total_vacaciones_label.set_text("{:.2f}".format(self.variable_dias_total_vacaciones))
            self.dias_pendientes_vacaciones_label.show()
            self.dias_pendientes_vacaciones_label.set_text("{:.2f}".format(self.variable_dias_pendientes_vacaciones))


        else:
            self.setup_warning()
        """    
        
    def setup_descuento_sancion(self):
        self.variable_dias_sancion_input_int = int(self.dias_sancion_input.text)
        
        if self.variable_dias_sancion_input_int >= self.variable_dias_pendientes_salario:
            self.variable_dias_pendientes_salario = 0
            self.dias_pendientes_salario_label.show()
            self.dias_pendientes_salario_label.set_text(f"{self.variable_dias_pendientes_salario}")
            self.variable_dias_pendientes_auxilio = self.variable_dias_pendientes_salario 
            self.dias_pendientes_auxilio_label.show()
            self.dias_pendientes_auxilio_label.set_text(f"{self.variable_dias_pendientes_auxilio}")
            
            
        else:
            self.variable_dias_pendientes_salario = (self.variable_dias_pendientes_salario - self.variable_dias_sancion_input_int)
            self.dias_pendientes_salario_label.show()
            self.dias_pendientes_salario_label.set_text(f"{self.variable_dias_pendientes_salario}")
            print(self.variable_dias_pendientes_salario)
            self.variable_dias_pendientes_auxilio = self.variable_dias_pendientes_salario
            self.dias_pendientes_auxilio_label.show()
            self.dias_pendientes_auxilio_label.set_text(f"{self.variable_dias_pendientes_auxilio}")
            print(self.variable_dias_pendientes_auxilio)

        if self.variable_dias_sancion_input_int >= self.variable_dias_pendientes_prima:
            self.variable_dias_pendientes_prima = 0
            self.dias_pendientes_prima_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_prima}")
        else:
            self.variable_dias_pendientes_prima = self.variable_dias_pendientes_prima - self.variable_dias_sancion_input_int 
            self.dias_pendientes_prima_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_prima}")
            print(self.variable_dias_pendientes_prima)

        if self.variable_dias_sancion_input_int >= self.variable_dias_pendientes_cesantias:
            self.variable_dias_pendientes_cesantias = 0
            self.dias_pendientes_cesantias_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_cesantias}")
        else:
            self.variable_dias_pendientes_cesantias = self.variable_dias_pendientes_cesantias - self.variable_dias_sancion_input_int 
            self.dias_pendientes_cesantias_label.show()
            self.dias_pendientes_cesantias_label.set_text(f"{self.variable_dias_pendientes_cesantias}")
            print(self.variable_dias_pendientes_cesantias)
        
    def setup_warning(self):
        dialogo = QMessageBox.warning(self, "Error en escritura de fechas", "La fecha inicial no puede ser mayor que la fecha final")

    

    


    





    
        








        
        
        





# Ejecutar la aplicacion Qt
import sys # se importa la libreria sys
app = QApplication(sys.argv)

window = Liquidacion_empleados() # se hace el llamado a la clase
window.setup_ui() # se aplica el tamano definido
window.show() # se muestra






# Cerrar la aplicacion Qt
sys.exit(app.exec())
