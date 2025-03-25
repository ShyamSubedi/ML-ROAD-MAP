# Fraud Detection API

## Overview
This API predicts whether a financial transaction is fraudulent based on the transaction amount. The model is deployed on Render and logs transactions to a SQLite database.

## Features
- Accepts transaction **amount** as input.
- Returns **fraud prediction** (0 = Not Fraud, 1 = Fraud).
- Logs all transactions to a **SQLite database**.

## API Endpoint
- **Base URL:** `https://finanance-fraud-detection-ml.onrender.com`
- **Prediction Endpoint:** `POST /predict/`

## How to Use

### 1. Using Python (Requests Library)
```python
import requests
API_URL = "https://finanance-fraud-detection-ml.onrender.com/predict/"
test_data = {"amount": 5000}
response = requests.post(API_URL, json=test_data)
print(response.json())  # {'fraud_prediction': 0 or 1}
```

### 2. Using Postman
1. Open **Postman**.
2. Select **POST** request.
3. Enter the API URL:  
   ```
   https://finanance-fraud-detection-ml.onrender.com/predict/
   ```
4. Go to **Body**, select **raw**, and set format to **JSON**.
5. Paste the following JSON request:
   ```json
   {"amount": 5000}
   ```
6. Click **Send**.
7. The response should be:
   ```json
   {"fraud_prediction": 0}
   ```
   (or `1` if the transaction is fraudulent)

### 3. Using cURL (Command Line)
```sh
curl -X POST "https://finanance-fraud-detection-ml.onrender.com/predict/" \
     -H "Content-Type: application/json" \
     -d '{"amount": 5000}'
```
Expected Response:
```json
{"fraud_prediction": 0}
```

## Logging Transactions
- Every request is **automatically logged** in a SQLite database.
- Logs can be accessed externally using SQLite.

## Deployment
- Hosted on **Render** (`https://finanance-fraud-detection-ml.onrender.com`).
- Automatically updates when changes are pushed to **GitHub**.

## Contributing
Feel free to open an issue or submit a pull request if you have suggestions!

## License
This project is **MIT licensed**.

