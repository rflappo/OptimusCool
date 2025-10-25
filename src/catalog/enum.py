from enum import Enum


class CatalogReference(str, Enum):
    HT = "Termo Huabon"
    TR = "Refrigeración de techo"
    F = "Congelados"
    A = "Alimentación del AC"
    B = "Batería"
    STB = "Modo de espera dividido"
    E = "Eléctrico"
    T = "Montaje en techo"
    N = "Montaje frontal"
    U = "Montaje inferior"
    M = "Monobloque"
    C = "Cobre"
    D = "Alimentación de DC"
    S = "Modo de espera"
    DS = "Unidad diésel con modo de espera"
    TS = "Modo de espera y de techo"
    EV = "Vehículo eléctrico"
