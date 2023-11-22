import sqlite3
import random

# Connect to the SQLite database (replace 'your_database.db' with your actual database file)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Sample brand names
brand_names = ['Sony', 'Samsung', 'Apple', 'Logitech', 'LG', 'Corsair', 'Xiaomi', 'Razer']

# Insert brand names into the Marca table
for brand in brand_names:
    sql = '''
        INSERT INTO tienda_marca (nombre)
        VALUES (?)
    '''
    cursor.execute(sql, (brand,))

# Commit the changes to the Marca table
conn.commit()

# Sample product categories
categories = ['TV', 'Phone', 'Mouse', 'Keyboard', 'Headset']

# Insert 100 random technology products into the Producto table
for _ in range(100):
    marca = random.choice(brand_names)
    category = random.choice(categories)
    nombre = f'{marca} {category} {random.randint(1, 20)}'
    modelo = nombre.split(' ')
    modelo = ''.join(word[0] for word in modelo)
    unidades = random.randint(50, 200)
    precio = round(random.uniform(50.0, 1000.0), 2)
    vip = random.choice([True, False])

    print(f'{marca},{nombre},{modelo},{unidades},{precio},{vip}')

    # SQL query to insert a product
    sql = '''
        INSERT INTO tienda_producto (marca_id, nombre, modelo, unidades, precio, vip)
        VALUES ((SELECT id FROM tienda_marca WHERE nombre = ?), ?, ?, ?, ?, ?)
    '''

    try:
        # Execute the query with parameters
        cursor.execute(sql, (marca, nombre, modelo, unidades, precio, vip))
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}. Skipping duplicate entry.")

# Commit the changes and close the connection
conn.commit()
conn.close()
