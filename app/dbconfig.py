conn_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'ns1234',
    'port': '5432'
}

create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS Patients (
        patient_id SERIAL PRIMARY KEY,
        patient_name VARCHAR(100),
        birth_date DATE,
        sex CHAR(1),
        other_details TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Studies (
        study_id SERIAL PRIMARY KEY,
        study_datetime TIMESTAMP,
        patient_id INT REFERENCES Patients(patient_id),
        modality VARCHAR(50),
        description TEXT,
        physician_name VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Series (
        series_id SERIAL PRIMARY KEY,
        study_id INT REFERENCES Studies(study_id),
        modality VARCHAR(50),
        series_number INT,
        body_part_examined VARCHAR(100),
        protocol_name VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Instances (
        instance_id SERIAL PRIMARY KEY,
        series_id INT REFERENCES Series(series_id),
        sop_instance_uid VARCHAR(100),
        image_type VARCHAR(50),
        image_path TEXT
    )
    """
]