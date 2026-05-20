import psycopg2

def init_db():

    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="hospital",
            user="postgres",
            password="admin",
            port="5432"
        )

        cursor = conexion.cursor()
        print("Conexión exitosa a la base de datos")

        return cursor, conexion
    except Exception as e:

        print("Error al conectar a la base de datos:", e)
        return None


cursor, conexion = init_db()

query = """
    INSERT INTO dim_personal(personal_role, personal_especiality)
    VALUES (%s, %s);
"""

if cursor is not None: 
    cursor.execute(query, ('medico', 'cardiologio'))

    conexion.commit()
    print("Datos insertados correctamente")
    
    conexion.close()
    cursor.close()

    