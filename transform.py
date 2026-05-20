import pandas as pd
import os

df = pd.read_csv("./data_lake/bronze/movimientos_hospital_raw.csv")

df["cama_tiene_sabana"] = df["cama_tiene_sabana"].fillna("no")
df["personal_especialidad"] = df["personal_especialidad"].fillna("")
df["cama_tipo"] = df["cama_tipo"].fillna("")
df = df.drop_duplicates(subset=["id_registro"], keep="first")

mapping_rows = []

for row in df.iloc :
        
    new_row = {
        "id_registro": row["id_registro"],
        "fecha_movimiento": row["fecha_movimiento"],
        "personal_rol": row["personal_rol"].lower(),
        "personal_especialidad": row["personal_especialidad"].lower(),
        "area_nombre": row["area_nombre"].lower(),
        "cama_serie": row["cama_serie"],
        "cama_tipo": row["cama_tipo"].lower(),
        "cama_tiene_sabana": row["cama_tiene_sabana"].lower() == "si",
        "cama_esta_ocupada": row["cama_esta_ocupada"].lower() == "ocupada",
    }

    mapping_rows.append(new_row) 

  
df_mapped = pd.DataFrame(mapping_rows)

path = "data_lake/sirver/movimientos_hospital_clean.csv"
folder_destiny = os.path.dirname(path)
os.makedirs(folder_destiny, exist_ok=True)

df_mapped.to_csv(path, index=False, encoding="utf-8")
