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

def save_movements(id_record, date_movement, name_area, bed_is_occuped, personal_id, bed_serial, cursor, conexion):

    query = """
        INSERT INTO dim_movements(id_record, date_movement, name_area, bed_is_occuped, personal_id, bed_serial)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    cursor.execute(query, (id_record, date_movement, name_area, bed_is_occuped, personal_id, bed_serial))
    conexion.commit()

    print("Movimiento guardado correctamente")


cursor, conexion = init_db()

roles_and_specialities = []
beds = []
movements = []

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

    # movimientos
    id_record = row["id_registro"]
    date_movement = row["fecha_movimiento"]
    name_area = row["area_nombre"]
    bed_is_occuped = row["cama_esta_ocupada"]
    bed_serial = row["cama_serie"]

    movements.append({
        "id_record": id_record,
        "date_movement": date_movement,
        "name_area": name_area,
        "bed_is_occuped": bed_is_occuped,
        "bed_serial": bed_serial
    })


for index, movement in enumerate(movements) :
    save_movements(
        movement["id_record"],
        movement["date_movement"],
        movement["name_area"],
        bool(movement["bed_is_occuped"]),
        index + 1,
        movement["bed_serial"],
        cursor,
        conexion
    )


for role_and_speciality in roles_and_specialities:
    save_role(
        role_and_speciality["role"],
        role_and_speciality["speciality"],
        cursor,
        conexion
    )


for bed in beds:
    save_beds(
        bed["id"],
        bed["type"],
        bool(bed["have_sheet"]),
        cursor,
        conexion
    )


if cursor is not None: 
    conexion.close()
    cursor.close()

    