from typing import List
import math

def to_signed(value,size=16):
    # Check if the MSB is 1 (negative value)
    if value & (1 << (size-1)):
        # Invert all bits and add 1
        value = -((2**size) - value)
    return value

def encode_signed(value):
    # Check if the value is negative
    if value < 0:
        # Convert to unsigned by adding 65536
        value = 65536 + value
    return value

def dxl_encode_value(value: int, size: int) -> List[int]:
    result = [value % 256]

    for i in range(1, size):
        tmp = value >> (8 * i)
        if tmp == -1:
            result.append(0xff)
        else:
            result.append(tmp)

    return result

def dxl_decode_value(data: List[int]) -> int:
    result = data[0]

    for i in range(1, len(data)):
        result += data[i] << 8 * i

    return result

def read_from_file(filename):
    try:
        # Ouvrir le fichier en mode lecture
        with open(filename, "r") as fichier:
            # Lire les lignes du fichier et convertir chaque valeur en float
            values = [float(ligne.strip()) for ligne in fichier.readlines()]

        return values

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None


def write_in_file(array, filename):
    try:
        # Ouvrir le fichier en mode écriture
        with open(filename, "w") as fichier:
            # Écrire chaque valeur dans une nouvelle ligne
            for value in array:
                fichier.write(str(value) + "\n")

        print(f"Les values ont été écrites dans le fichier {filename} avec succès.")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def rpm_to_rad_s(value):
    return (value * 2 * math.pi) / 60