-- Create the Cultura table
CREATE TABLE Cultura (
    id SERIAL PRIMARY KEY,     
    nombre VARCHAR(255) NOT NULL 
);

-- Create the Festividad table
CREATE TABLE Festividad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

-- Create the Deidad table
CREATE TABLE Deidad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    simbolismo TEXT NOT NULL,  
    festividad INTEGER,        
    cultura INTEGER,           
    FOREIGN KEY (festividad) REFERENCES Festividad(id) ON DELETE SET NULL,
    FOREIGN KEY (cultura) REFERENCES Cultura(id) ON DELETE SET NULL
);
