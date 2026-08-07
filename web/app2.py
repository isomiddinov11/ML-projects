from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Model va scalerlarni yuklab olish
car_model = joblib.load('mashina_modeli_pkl')
scaler = joblib.load('scaler2.pkl')

ustunlar_tartibi = [
    'year', 'mileage', 'engine_size', 
    'fuel_type_Diesel', 'fuel_type_Petrol',
    'transmission_Manual'
]

def mashina_narxini_bashorat_qil(year, mileage, engine_size, fuel_type, transmission):
    yangi_mashina = pd.DataFrame([{
        'year': year,
        'mileage': mileage,
        'engine_size': engine_size,
        'fuel_type_Diesel': 1 if fuel_type == 'Diesel' else 0,
        'fuel_type_Petrol': 1 if fuel_type == 'Petrol' else 0,
        'transmission_Manual': 1 if transmission == 'Manual' else 0,
    }])

    # Sonli ustunlarni scaling qilish
    yangi_mashina[['year', 'mileage', 'engine_size']] = scaler.transform(
        yangi_mashina[['year', 'mileage', 'engine_size']]
    )

    # Ustunlar ketma-ketligini moslash
    yangi_mashina = yangi_mashina[ustunlar_tartibi]

    # Bashorat
    natija = car_model.predict(yangi_mashina)
    return natija[0]


@app.route('/')
def home():
    # Bosh sahifa ochilganda shaklni ko'rsatadi
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Formadan yuborilgan ma'lumotlarni olish
        year = float(request.form['year'])
        mileage = float(request.form['mileage'])
        engine_size = float(request.form['engine_size'])
        fuel_type = request.form['fuel_type']
        transmission = request.form['transmission']

        # Model orqali bashorat qilish
        natija = mashina_narxini_bashorat_qil(year, mileage, engine_size, fuel_type, transmission)
        narx = round(float(natija), 2)

        # Natijani sahifaga qaytarish
        return render_template('index.html', predicted_price=narx)


if __name__ == "__main__":
    app.run(debug=True)
    