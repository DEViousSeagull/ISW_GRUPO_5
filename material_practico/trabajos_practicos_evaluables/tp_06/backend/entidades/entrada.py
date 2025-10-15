from entidades.tipoEntrada import TipoEntrada
class Entrada:
    def __init__(self,tipo_Entrada: TipoEntrada, id: int, edad_Visitante: int, precio: float):
        self.tipo_Entrada = tipo_Entrada
        self.id = id
        self.edad_Visitante = edad_Visitante
        self.precio = precio