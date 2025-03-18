# Müşteri Kaybı Tahmin MLOps Projesi

Bu proje, müşteri kaybı tahminlemesi için geliştirilmiş kurumsal düzeyde bir MLOps çözümüdür.

## Proje Bileşenleri

- **FastAPI**: Model servis etme ve API endpoints
- **MLflow**: Model versiyonlama ve deney takibi
- **Airflow**: Model eğitim pipeline'larının otomasyonu
- **Docker**: Tüm servislerin konteynerizasyonu

## Başlangıç

### Ön Koşullar

- Docker ve Docker Compose
- Git

### Kurulum

1. Projeyi klonlayın:
```bash
git clone [repo-url]
cd [repo-directory]
```

2. Docker container'larını başlatın:
```bash
docker-compose up -d
```

### Servis Portları

- FastAPI: http://localhost:8000
- Airflow: http://localhost:8080
- MLflow: http://localhost:5000

## API Endpoints

### Tahmin API'si

- `POST /predict`: Müşteri kaybı tahmini yapar
- `GET /model/info`: Aktif model bilgilerini döndürür

### Örnek İstek

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "tenure": 12,
           "monthly_charges": 50.0,
           "total_charges": 600.0,
           "contract_type": "Month-to-month",
           "payment_method": "Electronic check",
           "internet_service": "Fiber optic",
           "online_security": "No",
           "tech_support": "No"
         }'
```

## MLOps Pipeline

1. Airflow DAG'ı günlük olarak çalışır
2. Yeni veriler toplanır ve işlenir
3. Model yeniden eğitilir
4. Performans metrikleri MLflow'da kaydedilir
5. Model başarılı ise production'a alınır

## Geliştirme

### Yeni Model Versiyonu Ekleme

1. `src/models/` altında yeni model sınıfını oluşturun
2. Airflow DAG'ını güncelleyin
3. MLflow deneyini çalıştırın
4. Performans metriklerini değerlendirin
5. Production'a alma kararı verin

## Lisans

MIT 