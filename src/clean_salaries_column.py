# import re
# from src.database.connection import get_connection
#
# amounts_dict = {
#     "$6 a $8 millones": 7000000,
#     "$8 a $10 millones": 9000000,
#     "$2 a $2,5 millones": 2250000,
#     "$5,5 a $6 millones": 5750000,
#     "$1,5 a $2 millones": 1750000,
#     "$4,5 a $5,5 millones": 5000000,
#     "$3,5 a $4 millones": 3750000,
#     "$2,5 a $3 millones": 2750000,
#     "$4 a $4,5 millones": 4250000,
#     "$10 a $12,5 millones": 11250000,
#     "$12,5 a $15 millones": 13750000,
#     "$3 a $3,5 millones": 3250000,
#     "$1 a $1,5 millones": 1250000,
#     "$15 a $18 millones": 16500000,
#     "Más de $21 millones": 21000000
# }
#
# def clean_amount(amount):
#     # Reemplazar ,00 con una cadena vacía
#     amount_cleaned = amount.replace(',00', '')
#     # Eliminar todos los puntos
#     amount_cleaned = amount_cleaned.replace('.', '')
#     # Extraer solo los números
#     amount_cleaned = ''.join(re.findall(r'\d+', amount_cleaned))
#     return amount_cleaned
#
#
# def update_cleaned_amounts():
#     conn = get_connection()
#     cur = conn.cursor()
#
#     # Seleccionar solo los valores de la columna amount que contienen ",00"
#     cur.execute("SELECT id, amount FROM salaries WHERE amount LIKE '%,00%'")
#     salaries = cur.fetchall()
#
#     for salary in salaries:
#         id, amount = salary
#         amount_cleaned = clean_amount(amount)
#
#         # Actualizar la columna amount_cleaned solo para los registros seleccionados
#         cur.execute("UPDATE salaries SET amount_cleaned = %s WHERE id = %s", (amount_cleaned, id))
#
#     conn.commit()
#     cur.close()
#     conn.close()
#
#
# if __name__ == "__main__":
#     update_cleaned_amounts()
import re
from src.database.connection import get_connection

# Diccionario con rangos de montos y su valor medio aproximado
amounts_dict = {
    "$6 a $8 millones": 7000000,
    "$8 a $10 millones": 9000000,
    "$2 a $2,5 millones": 2250000,
    "$5,5 a $6 millones": 5750000,
    "$1,5 a $2 millones": 1750000,
    "$4,5 a $5,5 millones": 5000000,
    "$3,5 a $4 millones": 3750000,
    "$2,5 a $3 millones": 2750000,
    "$4 a $4,5 millones": 4250000,
    "$10 a $12,5 millones": 11250000,
    "$12,5 a $15 millones": 13750000,
    "$3 a $3,5 millones": 3250000,
    "$1 a $1,5 millones": 1250000,
    "$15 a $18 millones": 16500000,
    "Más de $21 millones": 21000000
}

def clean_amount(amount):
    # Normalizar y limpiar el monto
    amount_cleaned = amount.replace(',00', '').replace('.', '')
    amount_cleaned = ''.join(re.findall(r'\d+', amount_cleaned))
    return amount_cleaned

def update_cleaned_amounts():
    conn = get_connection()
    cur = conn.cursor()

    # Seleccionar todos los registros
    cur.execute("SELECT id, amount FROM salaries")
    salaries = cur.fetchall()

    for salary in salaries:
        id, amount = salary
        # Verificar si el monto está en el diccionario y actualizar directamente
        if amount in amounts_dict:
            amount_cleaned = amounts_dict[amount]
            cur.execute("UPDATE salaries SET amount_cleaned = %s WHERE id = %s", (amount_cleaned, id))
        elif ',00' in amount:  # Limpieza adicional para montos con ',00'
            amount_cleaned = clean_amount(amount)
            cur.execute("UPDATE salaries SET amount_cleaned = %s WHERE id = %s", (amount_cleaned, id))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_cleaned_amounts()
