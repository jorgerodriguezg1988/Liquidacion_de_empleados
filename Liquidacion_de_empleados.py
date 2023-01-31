from base64 import a85encode
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QPdfWriter, QPainter, QPageSize, QIntValidator
from PySide6.QtWidgets import QApplication
from __feature__ import snake_case, true_property
from datetime import datetime, date, time, timedelta
import os
import getpass
import math

from styles import estilos_menu # Se hace el llamado de la hoja de estilos como en CSS

class Liquidacion_empleados(QMainWindow): #Se crea una clase para la ventana para heredar
    
    def setup_ui(self): #Se crea el metodo de la VENTANA como tal
        self.show_maximized()
        #self.show_normal()
        self.size = QSize(1500, 900) # define el tamano de la ventana
        self.set_window_title("Liquidacion de empleados")

        self.root_layout = QVBoxLayout()

        self.fr_titulo = QFrame()
        self.fr_datos_basicos_empleados = QFrame()
        self.fr_conceptos_a_pagar = QFrame()
        self.fr_conceptos_a_descontar = QFrame()
        self.fr_resumen = QFrame()
        
        self.root_layout.add_widget(self.fr_titulo, 5)
        self.root_layout.add_widget(self.fr_datos_basicos_empleados,20)
        self.root_layout.add_widget(self.fr_conceptos_a_pagar,40)
        self.root_layout.add_widget(self.fr_conceptos_a_descontar,20)
        self.root_layout.add_widget(self.fr_resumen,15)


        self.widget = QWidget()
        self.widget.set_layout(self.root_layout)

        self.set_central_widget(self.widget)
        self.style_sheet = estilos_menu

        self.setup_title_frame()
        self.setup_datos_empleado_frame()
        self.setup_conceptos_a_pagar_frame()
        self.setup_conceptos_a_descontar_frame()
        self.setup_resumen_frame()
        
        
        self.guardar_datos_basicos_btn.clicked.connect(self.setup_total_dias_contrato) # Se conecta el metodo para que se ejecute la accion
        self.generar_calculos_btn.clicked.connect(self.setup_calculos_conceptos_a_pagar) 
        self.generar_calculos_btn.clicked.connect(self.setup_descuento_sancion) 
        self.generar_descuentos_btn.clicked.connect(self.setup_aplicar_descuentos) 
        self.generar_pdf_btn.clicked.connect(self.setup_crea_pdf) 
        
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
        self.salario_base_input.set_validator(QIntValidator(0, 999999999, self.salario_base_input))
        self.auxilio_trans_label = QLabel("Auxilio de transporte: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.auxilio_trans_input = QLineEdit(placeholder_text = "Valor sin puntos ni comas", alignment = Qt.AlignLeft)
        self.auxilio_trans_input.set_validator(QIntValidator(0, 999999999, self.auxilio_trans_input))
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
         

    def setup_conceptos_a_descontar_frame(self):
        self.grid_conceptos_a_descontar = QGridLayout()

        self.titulo_conceptos_a_descontar = QLabel("Conceptos a descontar: ", object_name="subtitulos_principales", alignment = Qt.AlignLeft)
        self.salud_label = QLabel("Aporte a salud - 4 %: $ ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.salud_porcen_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.pension_label = QLabel("Aporte a pension - 4 %: $ ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.pension_porcen_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.prestamo_label = QLabel("Prestamos o anticipos: ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.prestamo_input = QLineEdit(placeholder_text = "Valor de prestamos o anticipos a descontar", alignment = Qt.AlignLeft)
        self.prestamo_input.set_validator(QIntValidator(0, 999999999, self.prestamo_input))
        self.generar_descuentos_btn = QPushButton()
        self.generar_descuentos_btn.text = "Generar Descuentos"
        self.generar_descuentos_btn.style_sheet = "background: #2A88C1"
        

        self.grid_conceptos_a_descontar.add_widget(self.titulo_conceptos_a_descontar, 1, 1)
        self.grid_conceptos_a_descontar.add_widget(self.salud_label, 2, 1)
        self.grid_conceptos_a_descontar.add_widget(self.salud_porcen_label, 2, 2)
        self.grid_conceptos_a_descontar.add_widget(self.pension_label, 2, 3)
        self.grid_conceptos_a_descontar.add_widget(self.pension_porcen_label, 2, 4)
        self.grid_conceptos_a_descontar.add_widget(self.prestamo_label, 3, 1)
        self.grid_conceptos_a_descontar.add_widget(self.prestamo_input, 3, 2, 1, 2)
        self.grid_conceptos_a_descontar.add_widget(self.generar_descuentos_btn, 4, 5)


        self.fr_conceptos_a_descontar.set_layout(self.grid_conceptos_a_descontar)
        self.inputs_conceptos_a_descontar_layout = QVBoxLayout()
        self.inputs_conceptos_a_descontar_layout.add_stretch()


    def setup_resumen_frame(self):
        self.grid_resumen = QGridLayout()

        self.titulo_resumen_liquidacion = QLabel("Resumen de la liquidacion: ", object_name="subtitulos_principales", alignment = Qt.AlignLeft)
        self.titulo_subtotal_a_pagar_label = QLabel("Subtotal a pagar: $ ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.subtotal_a_pagar_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.titulo_subtotal_a_descontar_label = QLabel("Subtotal a descontar: $ ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.subtotal_a_descontar_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.titulo_valor_final_a_pagar_label = QLabel("Total a pagar: $ ", object_name="subtitulos", alignment = Qt.AlignLeft)
        self.valor_final_a_pagar_label = QLabel("", object_name="labels_vacios", alignment = Qt.AlignLeft)
        self.generar_pdf_btn = QPushButton()
        self.generar_pdf_btn.text = "Generar y Descargar PDF"
        self.generar_pdf_btn.style_sheet = "background: white"

        self.grid_resumen.add_widget(self.titulo_resumen_liquidacion, 1, 1)
        self.grid_resumen.add_widget(self.titulo_subtotal_a_pagar_label, 2, 1)
        self.grid_resumen.add_widget(self.subtotal_a_pagar_label, 2, 2)
        self.grid_resumen.add_widget(self.titulo_subtotal_a_descontar_label, 2, 3)
        self.grid_resumen.add_widget(self.subtotal_a_descontar_label, 2, 4)
        self.grid_resumen.add_widget(self.titulo_valor_final_a_pagar_label, 2, 5)
        self.grid_resumen.add_widget(self.valor_final_a_pagar_label, 2, 6)
        self.grid_resumen.add_widget(self.generar_pdf_btn, 3, 7)


        self.fr_resumen.set_layout(self.grid_resumen)
        self.inputs_resumen_layout = QVBoxLayout()
        self.inputs_resumen_layout.add_stretch()

        
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


        self.salario_base = int(self.salario_base_input.text)
        self.auxilio_trans = int(self.auxilio_trans_input.text)
        self.salario_mas_auxilio = self.salario_base + self.auxilio_trans
        
    def setup_calculos_conceptos_a_pagar(self):
        self.formato_fecha = "%d-%m-%Y"
        self.variable_fecha_ini_salario_pend = datetime.strptime(self.fecha_ini_salario_pend_input.text, self.formato_fecha)
        self.variable_fecha_fin_salario_pend = datetime.strptime(self.fecha_fin_salario_pend_input.text, self.formato_fecha)
        self.variable_dias_pendientes_salario = self.variable_fecha_fin_salario_pend - self.variable_fecha_ini_salario_pend
        self.variable_dias_pendientes_salario = self.variable_dias_pendientes_salario.days + 1
        
        self.variable_dias_pendientes_auxilio = self.variable_dias_pendientes_salario
        
        self.variable_fecha_ini_prima = datetime.strptime(self.fecha_ini_prima_input.text, self.formato_fecha)
        self.variable_fecha_fin_prima = datetime.strptime(self.fecha_fin_prima_input.text, self.formato_fecha)
        self.variable_dias_pendientes_prima = self.variable_fecha_fin_prima - self.variable_fecha_ini_prima
        self.variable_dias_pendientes_prima = self.variable_dias_pendientes_prima.days + 3 # ultimo dia laborado mas 2 dias de febrero
        if "-01-" in self.fecha_ini_prima_input.text or "-02-" in self.fecha_ini_prima_input.text or "-03-" in self.fecha_ini_prima_input.text or "-04-" in self.fecha_ini_prima_input.text or "-05-" in self.fecha_ini_prima_input.text or "-06-" in self.fecha_ini_prima_input.text:
            self.variable_dias_pendientes_prima = (self.variable_dias_pendientes_prima / 365) * 361
            self.variable_dias_pendientes_prima = math.floor(self.variable_dias_pendientes_prima)
            
        else:
            if "-07-" in self.fecha_ini_prima_input.text or "-08-" in self.fecha_ini_prima_input.text or "-09-" in self.fecha_ini_prima_input.text or "-10-" in self.fecha_ini_prima_input.text or "-11-" in self.fecha_ini_prima_input.text or "-12-" in self.fecha_ini_prima_input.text:
                self.variable_dias_pendientes_prima = self.variable_dias_pendientes_prima - 2 # por ser el segundo semestre se le restan los dos dias que se agregaron de Febrero
                self.variable_dias_pendientes_prima = (self.variable_dias_pendientes_prima / 365) * 359
                self.variable_dias_pendientes_prima = math.floor(self.variable_dias_pendientes_prima)
                
            
        self.variable_fecha_ini_cesantias = datetime.strptime(self.fecha_ini_cesantias_input.text, self.formato_fecha)
        self.variable_fecha_fin_cesantias = datetime.strptime(self.fecha_fin_cesantias_input.text, self.formato_fecha)
        self.variable_dias_pendientes_cesantias = self.variable_fecha_fin_cesantias - self.variable_fecha_ini_cesantias
        self.variable_dias_pendientes_cesantias = self.variable_dias_pendientes_cesantias.days + 3 #ultimo dia laborado mas 2 dias de febrero
        if self.variable_dias_pendientes_cesantias <= 183:
            self.variable_dias_pendientes_cesantias = (self.variable_dias_pendientes_cesantias / 365) * 361
            self.variable_dias_pendientes_cesantias = math.floor(self.variable_dias_pendientes_cesantias)
            
        else:
            self.variable_dias_pendientes_cesantias = self.variable_dias_pendientes_cesantias - 1
            self.variable_dias_pendientes_cesantias = (self.variable_dias_pendientes_cesantias / 365) * 360
            self.variable_dias_pendientes_cesantias = math.floor(self.variable_dias_pendientes_cesantias)
            
        self.variable_dias_total_vacaciones = (self.dias_total_contrato_360 / 360) * 15
        self.variable_dias_usados_vacaciones_input_int = int(self.dias_usados_vacaciones_input.text)
        self.variable_dias_pendientes_vacaciones = self.variable_dias_total_vacaciones - self.variable_dias_usados_vacaciones_input_int
        

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
            
            self.variable_dias_pendientes_auxilio = self.variable_dias_pendientes_salario
            self.dias_pendientes_auxilio_label.show()
            self.dias_pendientes_auxilio_label.set_text(f"{self.variable_dias_pendientes_auxilio}")
            

        if self.variable_dias_sancion_input_int >= self.variable_dias_pendientes_prima:
            self.variable_dias_pendientes_prima = 0
            self.dias_pendientes_prima_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_prima}")
        else:
            self.variable_dias_pendientes_prima = self.variable_dias_pendientes_prima - self.variable_dias_sancion_input_int 
            self.dias_pendientes_prima_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_prima}")
            

        if self.variable_dias_sancion_input_int >= self.variable_dias_pendientes_cesantias:
            self.variable_dias_pendientes_cesantias = 0
            self.dias_pendientes_cesantias_label.show()
            self.dias_pendientes_prima_label.set_text(f"{self.variable_dias_pendientes_cesantias}")
        else:
            self.variable_dias_pendientes_cesantias = self.variable_dias_pendientes_cesantias - self.variable_dias_sancion_input_int 
            self.dias_pendientes_cesantias_label.show()
            self.dias_pendientes_cesantias_label.set_text(f"{self.variable_dias_pendientes_cesantias}")


        self.valor_ultimo_salario_a_pagar = (self.salario_base / 30) * self.variable_dias_pendientes_salario
        self.valor_ultimo_auxilio_a_pagar = (self.auxilio_trans / 30) * self.variable_dias_pendientes_salario
        self.horas_extras_input_int = int(self.horas_extras_input.text)
        self.valor_extras_a_pagar = (((self.salario_base / 30) / 8) * self.horas_extras_input_int) * 1.25
        self.valor_prima_a_pagar = ((self.salario_mas_auxilio / 2) / 180) * self.variable_dias_pendientes_prima
        self.valor_cesantias_a_pagar = (self.salario_mas_auxilio / 360) * self.variable_dias_pendientes_cesantias
        self.valor_intereses_cesantias_a_pagar = ((self.valor_cesantias_a_pagar / 360) * self.variable_dias_pendientes_cesantias) * 0.12
        self.valor_vacaciones_a_pagar = ((self.salario_mas_auxilio / 2) / 15) * self.variable_dias_pendientes_vacaciones

        self.subtotal_a_pagar = self.valor_ultimo_salario_a_pagar + self.valor_ultimo_auxilio_a_pagar + self.valor_extras_a_pagar + self.valor_prima_a_pagar + self.valor_cesantias_a_pagar + self.valor_intereses_cesantias_a_pagar + self.valor_vacaciones_a_pagar
        
    def setup_aplicar_descuentos(self):
        self.descuento_salud = (self.valor_ultimo_salario_a_pagar + self.valor_ultimo_auxilio_a_pagar + self.valor_extras_a_pagar) * 0.04
        self.descuento_pension = (self.valor_ultimo_salario_a_pagar + self.valor_ultimo_auxilio_a_pagar + self.valor_extras_a_pagar) * 0.04
        self.descuento_prestamo = int(self.prestamo_input.text)
        self.salud_porcen_label.set_text("{:,.2f}".format(self.descuento_salud))
        self.pension_porcen_label.set_text("{:,.2f}".format(self.descuento_pension))

        self.subtotal_descuentos = self.descuento_salud + self.descuento_pension + self.descuento_prestamo
        self.total_liquidacion = self.subtotal_a_pagar - self.subtotal_descuentos
        
        self.subtotal_a_pagar_label.set_text("{:,.2f}".format(self.subtotal_a_pagar))
        self.subtotal_a_descontar_label.set_text("{:,.2f}".format(self.subtotal_descuentos))
        self.valor_final_a_pagar_label.set_text("{:,.2f}".format(self.total_liquidacion))


    def setup_crea_pdf(self):    
        
        user = getpass.getuser()
        os.chdir("C:/Users/"+ user +"/Downloads")
               
        pdf = QPdfWriter(f"Liquidacion de {self.nombre_input.text}.pdf")     #painter.draw_text(5000, 12300, "$  {:,.2f}" .format(self.valor_vacaciones_a_pagar))
        pdf.set_page_size(QPageSize.Legal)
        painter = QPainter(pdf)
        painter.draw_text(4000, 1000, "RESULTADO DE LA LIQUIDACION")
        painter.draw_text(0, 1200, "_____________________________________________________________________________________________________________________________________________________________")
        painter.draw_text(1000, 1500, "DATOS DEL EMPLEADO: ")
        painter.draw_text(800, 1900, f"NOMBRE:      {self.nombre_input.text}")
        painter.draw_text(5500, 1900, f"DOCUMENTO:               {self.cedula_input.text}")
        painter.draw_text(800, 2200, f"CARGO:        {self.cargo_input.text}")
        painter.draw_text(5500, 2200, f"MOTIVO DE RETIRO:       {self.tipo_retiro_combox.current_text}")
        painter.draw_text(800, 2500, f"FECHA INICIO DE CONTRATO:        {self.fecha_ini_input.text}")
        painter.draw_text(5500, 2500, f"FECHA FIN DE CONTRATO:       {self.fecha_fin_input.text}")
        painter.draw_text(800, 2800, "SALARIO BASE DEL EMPLEADO:        $ {:,.2f}".format(self.salario_base))
        painter.draw_text(5500, 2800, "AUXILIO DE TRANSPORTE:       $ {:,.2f}".format(self.auxilio_trans))
        painter.draw_text(800, 3100, f"TOTAL DIAS TRABAJADOS:        {self.dias_trabajados_label.text}")
        painter.draw_text(0, 3300, "_____________________________________________________________________________________________________________________________________________________________")
        painter.draw_text(1000, 3600, "CONCEPTOS A PAGAR: ")
        painter.draw_text(800, 4000, "ULTIMO SALARIO: ")
        painter.draw_text(800, 4300, f"Fecha Inicio:              {self.fecha_ini_salario_pend_input.text}")
        painter.draw_text(5500, 4300, f"Fecha Final:              {self.fecha_fin_salario_pend_input.text}")
        painter.draw_text(800, 4500, f"Días de sanción:                                                            - {self.dias_sancion_input.text} días")
        painter.draw_text(800, 4700, f"Días pendientes de pago por salario:                              {self.dias_pendientes_salario_label.text} días")
        painter.draw_text(800, 4900, f"Días pendientes de pago por auxilio de transporte:       {self.dias_pendientes_auxilio_label.text} días")
        painter.draw_text(800, 5100, f"Horas extras pendientes de pago:                                  {self.horas_extras_input.text} horas")
        painter.draw_text(800, 5500, f"PRIMA LEGAL: ")
        painter.draw_text(800, 5800, f"Fecha Inicio:              {self.fecha_ini_prima_input.text}")
        painter.draw_text(5500, 5800, f"Fecha Final:              {self.fecha_fin_prima_input.text}")
        painter.draw_text(800, 6000, f"Días pendientes de pago por prima legal:                      {self.dias_pendientes_prima_label.text} días")
        painter.draw_text(800, 6400, f"CESANTIAS: ")
        painter.draw_text(800, 6700, f"Fecha Inicio:              {self.fecha_ini_cesantias_input.text}")
        painter.draw_text(5500, 6700, f"Fecha Final:              {self.fecha_fin_cesantias_input.text}")
        painter.draw_text(800, 7000, f"Días pendientes de pago por cesantias:                      {self.dias_pendientes_cesantias_label.text} días")
        painter.draw_text(800, 7400, f"VACACIONES: ")
        painter.draw_text(800, 7700, f"Días de vacaciones merecidos:              {self.dias_total_vacaciones_label.text} días")
        painter.draw_text(5500, 7700, f"Días de vacaciones disfrutados:              {self.dias_usados_vacaciones_input.text} días")
        painter.draw_text(800, 8000, f"Días pendientes de pago por vacaciones:                      {self.dias_pendientes_vacaciones_label.text} días")
        painter.draw_text(1000, 8500, "CONCEPTOS A DESCONTAR: ")
        painter.draw_text(800, 8800, f"Aporte a Salud:                                           4 % sobre salario y auxilio de transporte")
        painter.draw_text(800, 9100, f"Aporte a Pensión:                                       4 % sobre salario y auxilio de transporte")
        painter.draw_text(800, 9400, "Prestamos o anticipos a descontar:             $ {:,.2f}".format(self.descuento_prestamo))
        painter.draw_text(0, 9600, "_____________________________________________________________________________________________________________________________________________________________")
        painter.draw_text(1000, 9900, "DETALLE DE CONCEPTOS LIQUIDADOS: ")
        painter.draw_text(5000, 10200, "DEVENGADO")
        painter.draw_text(8000, 10200, "DEDUCIDO")
        painter.draw_text(500, 10500, f"Salario:")
        painter.draw_text(5000, 10500, "$  {:,.2f}" .format(self.valor_ultimo_salario_a_pagar))
        painter.draw_text(500, 10800, f"Auxilio de transporte:")
        painter.draw_text(5000, 10800, "$  {:,.2f}" .format(self.valor_ultimo_auxilio_a_pagar))
        painter.draw_text(500, 11100, f"Horas extras (25% adicional a la hora de trabajo ordinaria):")
        painter.draw_text(5000, 11100, "$  {:,.2f}" .format(self.valor_extras_a_pagar))
        painter.draw_text(500, 11400, f"Prima legal:")
        painter.draw_text(5000, 11400, "$  {:,.2f}" .format(self.valor_prima_a_pagar))
        painter.draw_text(500, 11700, f"Cesantias:")
        painter.draw_text(5000, 11700, "$  {:,.2f}" .format(self.valor_cesantias_a_pagar))
        painter.draw_text(500, 12000, f"Intereses de cesantias (12% de interes sobre las cesantias):")
        painter.draw_text(5000, 12000, "$  {:,.2f}" .format(self.valor_intereses_cesantias_a_pagar))
        painter.draw_text(500, 12300, f"Vacaciones:")
        painter.draw_text(5000, 12300, "$  {:,.2f}" .format(self.valor_vacaciones_a_pagar))
        painter.draw_text(500, 12600, f"Aporte a Salud:")
        painter.draw_text(8000, 12600, "$  {:,.2f}" .format(self.descuento_salud))
        painter.draw_text(500, 12900, f"Aporte a Pensión:")
        painter.draw_text(8000, 12900, "$  {:,.2f}" .format(self.descuento_pension))
        painter.draw_text(500, 13200, f"Descuento prestamo / anticipo:")
        painter.draw_text(8000, 13200, "$  {:,.2f}" .format(self.descuento_prestamo))
        painter.draw_text(500, 13700, "SUBTOTALES:")
        painter.draw_text(5000, 13700, "$  {:,.2f}" .format(self.subtotal_a_pagar))
        painter.draw_text(8000, 13700, "$  {:,.2f}" .format(self.subtotal_descuentos))
        painter.draw_text(500, 14200, "TOTAL A PAGAR:")
        painter.draw_text(3000, 14200, "$  {:,.2f}" .format(self.total_liquidacion))
        #painter.window().width()//2,
        #painter.window().height()//2,
        painter.end()
        
        self.setup_information()

    def setup_information(self):
        dialogo = QMessageBox.information(self, "Generacion de PDF", "Archivo PDF generado exitosamente")


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
