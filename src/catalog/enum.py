from enum import Enum


class CatalogReference(str, Enum):
    HT = "Termo;Huabon"
    TR = "Refrigera;techo"
    F = "Congelad"
    A = "AC"
    B = "Batería"
    STB = "espera;dividido"
    E = "Eléctric"
    T = "techo"
    N = "frontal;frente"
    U = "inferior"
    M = "Monobloque"
    C = "Cobre"
    D = "DC"
    S = "espera"
    DS = "diésel;espera"
    TS = "espera;techo"
    EV = "Vehículo;eléctric"
