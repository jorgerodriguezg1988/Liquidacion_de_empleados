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

#subtitulos{

    font-size: 20px;
    
    
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


    


'''


estilos_juego = estilos_generales +'''

QPushButton {
    height: 100%;
}

QPushButton:disabled{
color: white;
}


'''




