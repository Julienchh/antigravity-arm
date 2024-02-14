from typing import List
import math
from sys import stderr


def to_signed(value: int, size=16) -> int:
    """
    Decodes a two's complement encoded signed integer.

    Parameters:
    - value (int): The encoded number to decode.
    - size (int): The number of bits used to encode the value.

    Returns:
    - int: The decoded signed integer value.
    """
    if value & (1 << (size - 1)):
        value = -((2**size) - value)

    return value


def encode_signed(value: int) -> int:
    """
    Encodes a signed integer.

    Parameters:
    - value (int): The integer value to encode.

    Returns:
    - int: The encoded value.
    """
    if value < 0:
        value = 65536 + value
    return value


def dxl_encode_value(value: int, size: int) -> List[int]:
    """
    Encodes an integer into a list of bytes.

    Parameters:
    - value (int): The integer value to encode.
    - size (int): The number of bytes to use for encoding.

    Returns:
    - List[int]: The list of bytes representing the encoded value.
    """
    result = [value % 256]

    for i in range(1, size):
        tmp = value >> (8 * i)
        if tmp == -1:
            result.append(0xFF)
        else:
            result.append(tmp)

    return result


def dxl_decode_value(data: List[int]) -> int:
    """
    Decodes a list of bytes into an integer value.

    Parameters:
    - data (List[int]): The list of bytes to decode.

    Returns:
    - int: The decoded integer value.
    """
    result = data[0]

    for i in range(1, len(data)):
        result += data[i] << 8 * i

    return result


def read_from_file(filename: str) -> List[float]:
    """
    Deserialize floating-point values from a file.

    Parameters:
    - filename (str): The name of the file to read from.

    Returns:
    - List[float] or None: A list of floating-point values read from the file,
    or None if an error occurs.
    """
    try:
        with open(filename, "r") as fichier:
            values = [float(ligne.strip()) for ligne in fichier.readlines()]

        return values

    except Exception as e:
        print(f"[Read from file] An error occurred: {e}", file=stderr)
        return None


def write_in_file(array: List[float], filename: str) -> None:
    """
    Serializes values to a file.

    Parameters:
    - array (Iterable): An iterable containing the values to write.
    - filename (str): The name of the file to write to.
    """
    try:
        with open(filename, "w") as fichier:
            for value in array:
                fichier.write(str(value) + "\n")

    except Exception as e:
        print(f"[Write in file] An error occurred: {e}", file=stderr)


def rpm_to_rad_s(value: float) -> float:
    """
    Converts RPM (Revolutions Per Minute) to radians per second.

    Parameters:
    - value (float): The value in RPM to convert.

    Returns:
    - float: The equivalent value in radians per second.
    """
    return (value * 2 * math.pi) / 60
