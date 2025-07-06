// MongoDB initialization script for refrigeration maintenance system
db = db.getSiblingDB('refrigeration_maintenance');

// Create collections
db.createCollection('predictions');
db.createCollection('alerts');
db.createCollection('sensors_data');
db.createCollection('maintenance_logs');

// Create indexes for better performance
db.predictions.createIndex({ "timestamp": 1 });
db.predictions.createIndex({ "machine_id": 1 });
db.predictions.createIndex({ "prediction": 1 });

db.alerts.createIndex({ "timestamp": 1 });
db.alerts.createIndex({ "machine_id": 1 });
db.alerts.createIndex({ "severity": 1 });

db.sensors_data.createIndex({ "timestamp": 1 });
db.sensors_data.createIndex({ "machine_id": 1 });
db.sensors_data.createIndex({ "operating_mode": 1 });

db.maintenance_logs.createIndex({ "timestamp": 1 });
db.maintenance_logs.createIndex({ "machine_id": 1 });
db.maintenance_logs.createIndex({ "maintenance_type": 1 });

// Insert sample data
db.predictions.insertMany([
    {
        "timestamp": new Date(),
        "machine_id": 1,
        "temp_evaporator": -10.5,
        "temp_condenser": 40.5,
        "pressure_high": 12.5,
        "pressure_low": 2.1,
        "superheat": 8.5,
        "subcooling": 5.2,
        "compressor_current": 8.2,
        "vibration": 0.020,
        "prediction": 0,
        "probability": 0.15,
        "operating_mode": "normal"
    }
]);

db.alerts.insertMany([
    {
        "timestamp": new Date(),
        "machine_id": 1,
        "message": "Système de surveillance initialisé",
        "severity": "info",
        "type": "system",
        "acknowledged": false
    }
]);

print("✅ Base de données refrigeration_maintenance initialisée avec succès");
