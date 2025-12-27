import requests
import time
import random
import datetime

print("=" * 60)
print("🤖 IOT DEVICE EMULATOR - SMART GARAGE")
print("=" * 60)

class SmartDevice:
    def __init__(self, device_id, device_type):
        self.id = device_id
        self.type = device_type
        self.status = "idle"
    
    def send_to_server(self, server_url="http://localhost:5000"):
        """Отправка данных на сервер"""
        # Генерация статуса
        statuses = ["active", "idle", "error", "maintenance"]
        self.status = random.choice(statuses)
        
        # Данные для отправки
        data = {
            "device_id": self.id,
            "device_type": self.type,
            "status": self.status,
            "timestamp": datetime.datetime.now().isoformat(),
            "battery_level": random.randint(30, 100)
        }
        
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📤 Sending: {self.id} = {self.status}")
        
        try:
            response = requests.post(
                f"{server_url}/api/data",
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=3
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Response: {result['message']}")
                print(f"   ⏰ Server time: {result['server_time']}")
                return True
            else:
                print(f"   ❌ Error {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            return False

def main():
    """Основная функция эмуляции"""
    # Создаем устройства
    devices = [
        SmartDevice("garage_door_01", "garage_door"),
        SmartDevice("light_01", "light"),
        SmartDevice("camera_01", "security_camera"),
        SmartDevice("sensor_01", "temperature_sensor")
    ]
    
    server_url = "http://localhost:5000"
    
    print(f"🔗 Server URL: {server_url}")
    print(f"📱 Devices: {len(devices)}")
    print("-" * 60)
    
    # Цикл эмуляции
    for cycle in range(1, 6):  # 5 циклов
        print(f"\n🔄 CYCLE {cycle}/5")
        print("-" * 40)
        
        for device in devices:
            device.send_to_server(server_url)
            time.sleep(1)  # Пауза между устройствами
        
        time.sleep(2)  # Пауза между циклами
    
    print("\n" + "=" * 60)
    print("✅ EMULATION COMPLETED!")
    print("=" * 60)
    
    # Проверяем логи
    try:
        print("\n📋 Checking server logs...")
        response = requests.get(f"{server_url}/api/logs")
        if response.status_code == 200:
            data = response.json()
            print(f"Total devices in server: {data['count']}")
    except:
        print("Cannot connect to server logs")

if __name__ == "__main__":
    main()
