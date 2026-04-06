import time
import json
import random
from awscrt import mqtt
from awsiot import mqtt_connection_builder


ENDPOINT = "alqhes97pfg54-ats.iot.eu-north-1.amazonaws.com"
CLIENT_ID = "BulutProjesi_Cihaz_1"
PATH_TO_CERT = "ba0d12e6933456f0b7360eba685523e55e2b484fb4a1b1e78e66c0d9b032bcfc-certificate.pem.crt"
PATH_TO_KEY = "ba0d12e6933456f0b7360eba685523e55e2b484fb4a1b1e78e66c0d9b032bcfc-private.pem.key"
PATH_TO_ROOT = "AmazonRootCA1.pem"
TOPIC = "proje/veri/sicaklik"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print(f"{ENDPOINT} adresine bağlanılıyor...")
connect_future = mqtt_connection.connect()
connect_future.result() 
print("AWS IoT Core'a başarıyla bağlanıldı!")

try:
    while True:
  
        sicaklik_verisi = round(random.uniform(20.0, 30.0), 2)
        

        mesaj = {"sicaklik": sicaklik_verisi, "zaman": int(time.time())}

        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(mesaj),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        print(f"Gönderilen veri: {mesaj}")
    
        time.sleep(2)

except KeyboardInterrupt:

    print("\nVeri gönderimi durduruldu.")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()