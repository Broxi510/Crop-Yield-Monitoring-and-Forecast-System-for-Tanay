USE crop_monitoring;

CREATE TABLE IF NOT EXISTS records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    barangay VARCHAR(100),
    crop VARCHAR(50),
    area FLOAT,
    yield_amt FLOAT,
    yield_per_hectare FLOAT
);

SELECT * FROM records;