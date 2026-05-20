import psycopg2
import pandas as pd

df = pd.read_csv("./data_lake/silver/movimientos_hospital_clean.csv")

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
        return None, None

def save_role(role, speciality, cursor, conexion): 
    query = """
        INSERT INTO dim_personal(personal_role, personal_speciality)
        VALUES (%s, %s);
    """

    cursor.execute(query, (role, speciality))
    conexion.commit()


cursor, conexion = init_db()

roles_and_specialities = []

for row in df.iloc:
    role = row["personal_rol"]
    speciality = row["personal_especialidad"]

    roles_and_specialities.append({
        "role": role,
        "speciality": speciality
    })


for data in roles_and_specialities:
    save_role(data["role"], data["speciality"], cursor, conexion)

if cursor is not None: 
    conexion.close()
    cursor.close()

    