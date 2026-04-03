-- =============================================================
-- HBnB - Initial Data Script
-- =============================================================

-- Administrator User
-- Password: admin1234 hashed with bcrypt
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$WqNaFMBGEqDDDcFd1O4KWOSofkbXCuFbXBLcMNn1POWiUlpYqCLuS',
    TRUE
);

-- Initial Amenities
INSERT INTO Amenity (id, name)
VALUES
    ('4c7e8044-7135-422e-9ea0-22e70d0dfc4d', 'WiFi'),
    ('81cd3646-d8f4-432e-ab1b-f87998ced1cc', 'Swimming Pool'),
    ('78059967-06fe-4b39-ae2b-bc3697393dc3', 'Air Conditioning');
    