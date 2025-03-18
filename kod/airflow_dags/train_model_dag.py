from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def prepare_data(**context):
    # Örnek veri yükleme - gerçek uygulamada veritabanından çekilecek
    # Burada örnek veri oluşturuyoruz
    data = pd.DataFrame({
        'tenure': range(1000),
        'monthly_charges': [50 + i * 0.1 for i in range(1000)],
        'total_charges': [500 + i for i in range(1000)],
        'contract_type': ['Month-to-month'] * 1000,
        'payment_method': ['Electronic check'] * 1000,
        'internet_service': ['Fiber optic'] * 1000,
        'online_security': ['No'] * 1000,
        'tech_support': ['No'] * 1000,
        'churn': [i % 2 for i in range(1000)]
    })
    
    return data

def train_model(**context):
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("customer_churn_prediction")
    
    data = context['task_instance'].xcom_pull(task_ids='prepare_data')
    
    # Veri hazırlığı
    X = data.drop('churn', axis=1)
    y = data['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with mlflow.start_run():
        # Model eğitimi
        model = xgb.XGBClassifier(
            objective='binary:logistic',
            n_estimators=100,
            max_depth=4
        )
        model.fit(X_train, y_train)
        
        # Tahminler
        y_pred = model.predict(X_test)
        
        # Metrikleri hesapla
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred)
        }
        
        # MLflow'a metrikleri ve modeli kaydet
        mlflow.log_metrics(metrics)
        mlflow.log_params(model.get_params())
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name="customer_churn"
        )

with DAG(
    'customer_churn_training',
    default_args=default_args,
    description='Müşteri kaybı tahmin modeli eğitim pipeline\'ı',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    prepare_data_task = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_data,
    )

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )

    prepare_data_task >> train_model_task 