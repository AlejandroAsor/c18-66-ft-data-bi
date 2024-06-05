import re
from src.database.connection import get_connection


def clean_amount(amount):
    # Reemplazar ,00 con una cadena vacía
    amount_cleaned = amount.replace(',00', '')
    # Eliminar todos los puntos
    amount_cleaned = amount_cleaned.replace('.', '')
    # Extraer solo los números
    amount_cleaned = ''.join(re.findall(r'\d+', amount_cleaned))
    return amount_cleaned


def update_cleaned_amounts():
    conn = get_connection()
    cur = conn.cursor()

    # Seleccionar solo los valores de la columna amount que contienen ",00"
    cur.execute("SELECT id, amount FROM salaries WHERE amount LIKE '%,00%'")
    salaries = cur.fetchall()

    for salary in salaries:
        id, amount = salary
        amount_cleaned = clean_amount(amount)

        # Actualizar la columna amount_cleaned solo para los registros seleccionados
        cur.execute("UPDATE salaries SET amount_cleaned = %s WHERE id = %s", (amount_cleaned, id))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    update_cleaned_amounts()
