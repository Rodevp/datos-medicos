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

    print("Rol y especialidad guardados correctamente")

def save_beds(bed_id, bed_type, have_sheet, cursor, conexion):

    query = """
        INSERT INTO dim_beds(id, bed_type, bed_have_sheet)
        VALUES (%s, %s, %s);
    """

    cursor.execute(query, (bed_id, bed_type, have_sheet))
    conexion.commit()

    print("Cama guardada correctamente")

cursor, conexion = init_db()

roles_and_specialities = []
beds = []

for row in df.iloc:
    role = row["personal_rol"]
    speciality = row["personal_especialidad"]

    roles_and_specialities.append({
        "role": role,
        "speciality": speciality
    })

    # camas
    bed_id = row["cama_serie"]
    bed_type = row["cama_tipo"]
    have_sheet = row["cama_tiene_sabana"]

    beds.append({
        "id": bed_id,
        "type": bed_type,
        "have_sheet": have_sheet
    })


for bed in beds :
    #save_beds(bed["id"], bed["type"], bool(bed["have_sheet"]), cursor, conexion)
    #print(bed)
    if bed["id"] == "CAM-649": 
        print("ya existe")

if cursor is not None: 
    conexion.close()
    cursor.close()

    