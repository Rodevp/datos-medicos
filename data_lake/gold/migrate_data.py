import psycopg2

DB_LOCAL_CONFIG = {
    "dbname": "hospital",
    "user": "postgres",
    "password": "[PASSWORD]",
    "host": "localhost",
    "port": "5432"
}

SUPABASE_URI = "postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-1-us-east-2.pooler.supabase.com:5432/postgres"
TABLES_TO_MIGRATE = ["dim_personal", "dim_beds", "dim_movements"]

def migrate_data():
    conn_local = None
    conn_supa = None
    
    try:
        print("🔌 Conectando a las bases de datos...")
        conn_local = psycopg2.connect(**DB_LOCAL_CONFIG)
        conn_supa = psycopg2.connect(SUPABASE_URI)
        
        cursor_local = conn_local.cursor()
        cursor_supa = conn_supa.cursor()
        
        print("✅ Conexiones establecidas con éxito.\n")
        
        for tabla in TABLES_TO_MIGRATE:
            print(f"⏳ Migrando tabla: {tabla}...")
            
            # 1. Validar que la tabla exista en Supabase
            cursor_supa.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = %s
                );
            """, (tabla,))
            
            if not cursor_supa.fetchone()[0]:
                print(f"❌ Error: La tabla '{tabla}' no existe en Supabase.")
                continue

            # 2. Limpiar datos preexistentes
            print(f"   Limpiando datos preexistentes en Supabase para {tabla}...")
            cursor_supa.execute(f"TRUNCATE TABLE {tabla} CASCADE;") 
            
            # 3. Transferencia de registros usando un buffer en memoria
            print(f"   Transfiriendo registros...")
            import io
            buffer = io.StringIO()
            
            # Extraer de local al buffer (usando tabulador como separador y manejando nulos)
            cursor_local.copy_to(buffer, tabla, sep='\t', null='\\N')
            buffer.seek(0) # Mover el puntero al inicio del archivo en memoria
            
            # Subir del buffer a Supabase
            cursor_supa.copy_from(buffer, tabla, sep='\t', null='\\N')
            
            print(f"🎉 Tabla '{tabla}' migrada exitosamente.")
            
        # Confirmar los cambios si todo salió bien
        conn_supa.commit()
        print("\n🚀 ¡Migración completada con éxito en Supabase!")

    except Exception as e:
        print(f"\n❌ Ocurrió un error durante la migración: {e}")
        if conn_supa:
            conn_supa.rollback()
            print("🔄 Se realizó un rollback en Supabase para mantener la consistencia.")
            
    finally:
        if conn_local:
            conn_local.close()
        if conn_supa:
            conn_supa.close()
        print("🔌 Conexiones cerradas.")

if __name__ == "__main__":
    migrate_data()