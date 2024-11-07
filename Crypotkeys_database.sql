    CREATE TABLE employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        public_key TEXT
    );

    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        employee_id INT REFERENCES employees(id),
        document_data BYTEA,
        signature BYTEA,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
