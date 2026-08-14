from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    form_data = {
        'year': '',
        'mileage': '',
        'engine': '',
        'fuel': 'petrol',
        'transmission': 'manual',
        'condition': 'good'
    }

    if request.method == 'POST':
        # Formadan kelgan ma'lumotlarni qabul qilish
        form_data['year'] = request.form.get('year')
        form_data['mileage'] = request.form.get('mileage')
        form_data['engine'] = request.form.get('engine')
        form_data['fuel'] = request.form.get('fuel')
        form_data['transmission'] = request.form.get('transmission')
        form_data['condition'] = request.form.get('condition')

        year = int(form_data['year'])
        mileage = float(form_data['mileage'])
        engine = float(form_data['engine'])

        estimated_price = 20000 - ((2026 - year) * 1000) - (mileage * 0.05)
        predicted_price = round(max(estimated_price, 1000), 2)

    return render_template('index.html', price=predicted_price, data=form_data)

if __name__ == '__main__':
    app.run(debug=True)