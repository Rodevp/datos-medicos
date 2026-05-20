CREATE TABLE dim_personal (
    id SERIAL PRIMARY KEY,
    personal_role VARCHAR(50) NOT NULL,
    personal_especiality VARCHAR(50) NOT NULL
);

CREATE TABLE dim_beds (
    id VARCHAR(20) PRIMARY KEY,
    bed_type VARCHAR(50) NOT NULL,
    bed_have_sheet BOOLEAN NOT NULL
);

CREATE TABLE dim_movements (
    id_record VARCHAR(20) PRIMARY KEY,
    date_movement TIMESTAMP NOT NULL,
    name_area VARCHAR(100) NOT NULL,
    bed_is_occupied BOOLEAN NOT NULL,

    personal_id INT REFERENCES dim_personal(id),
    bed_serial VARCHAR(20) REFERENCES dim_beds(id)
);