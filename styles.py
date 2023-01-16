estilos_generales = '''   

QWidget {
    background: gray;
    
}

QFrame {
    background: #242526;
    border-radius: 10px;
}

QLabel {
    color: #2A88C1;
    font-size: 16px;

}

QComboBox QAbstractItemView{
    background-color: white;
    border: 2px solid white;
    selection-background-color: white;
    font-size: 16px;
}

#titulo_principal{
    font-size: 50px;
    font-weight: bold;
}

#subtitulos_principales{

    font-size: 25px;
    font-weight: bold;
    
    
}

#subtitulos{

    font-size: 20px;   
}

#labels_vacios{
    background-color: #242526;
    color: #ffffff;
    font-size: 22px;   
}


'''


estilos_menu = estilos_generales +'''
    
    
    QLineEdit{
        background: white;
        border-radius: 5px;
        padding: 10px;
    }

    QPushButton {
        border-radius: 5px;
        padding: 10px;
    }

    QMessageBox {
        background-color: #D5DBDB;
}

    QMessageBox QLabel {
        background-color: #D5DBDB;    
        color: #1A5276;
}

    QMessageBox QPushButton {
        background-color: #2A88C1;
        color: black;
}


    


'''


estilos_juego = estilos_generales +'''

QPushButton {
    height: 100%;
}

QPushButton:disabled{
color: white;
}


'''




