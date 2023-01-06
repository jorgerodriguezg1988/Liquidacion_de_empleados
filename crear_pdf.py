#from Liquidacion_de_empleados import Liquidacion_empleados
from PySide6.QtGui import QPdfWriter, QPainter, QPageSize
from PySide6.QtWidgets import QApplication
from __feature__ import snake_case, true_property


class crear_pdf:
    
    
    app = QApplication()
    #pdf = QPdfWriter(setup_datos_empleado_frame.prueba_pdf)
    #pdf = QPdfWriter(f"{prueba_pdf}.pdf")
    pdf = QPdfWriter('example.pdf')
    pdf.set_page_size(QPageSize.Letter)
    painter = QPainter(pdf)
    painter.draw_text(painter.window().width()//2,
                    painter.window().height()//2,
                    'https://donkirkby.github.io')
    painter.end()



