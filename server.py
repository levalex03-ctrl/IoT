from flask import Flask, request, jsonify
import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

app = Flask(__name__)

# Хранилище данных
devices = {}

print("=" * 60)
print("🚀 IOT FLASK SERVER FOR SMART GARAGE")
print("Server: http://localhost:5000")
print("Endpoints: POST /api/data , GET /api/logs")
print("=" * 60)

@app.route('/api/data', methods=['POST'])
def receive_data():
    """Получение данных от IoT устройств"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data"}), 400
        
        device_id = data.get('device_id', 'unknown')
        device_type = data.get('device_type', 'unknown')
        status = data.get('status', 'unknown')
        
        # Логирование
        log_msg = f"Device: {device_id} | Type: {device_type} | Status: {status}"
        print(f"📡 {log_msg}")
        
        # Сохранение
        devices[device_id] = {
            'type': device_type,
            'status': status,
            'last_update': datetime.datetime.now().isoformat()
        }
        
        # Ответ
        response = {
            "success": True,
            "message": "Data received",
            "device_id": device_id,
            "server_time": datetime.datetime.now().strftime("%H:%M:%S"),
            "total_devices": len(devices)
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Получить информацию о всех устройствах"""
    return jsonify({
        "devices": devices,
        "count": len(devices),
        "server_time": datetime.datetime.now().isoformat()
    })

@app.route('/')
def home():
    """Главная страница"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IoT Server</title>
        <style>
            body { font-family: Arial; padding: 30px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f0f0f0; padding: 15px; margin: 15px 0; border-radius: 8px; }
            code { background: #ddd; padding: 4px 8px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏠 IoT Server for Smart Garage</h1>
            <p>Flask server for IoT devices communication</p>
            
            <div class="endpoint">
                <h3>📨 Send device data (POST)</h3>
                <p><code>POST /api/data</code></p>
                <pre>{
  "device_id": "garage_door_01",
  "device_type": "garage_door",
  "status": "opened"
}</pre>
            </div>
            
            <div class="endpoint">
                <h3>📊 Get devices info (GET)</h3>
                <p><code>GET /api/logs</code></p>
            </div>
            
            <p><strong>Status:</strong> ✅ Server is running</p>
            <p><strong>Time:</strong> ''' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("✅ Starting Flask server...")
    print("✅ Waiting for device connections...")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
