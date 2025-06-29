from flask import Flask, url_for, redirect, render_template
from flask_bootstrap import Bootstrap5 # bootstrap for forms and stuff?
import os, stripe # Import stripe for payment stuff
from dotenv import load_dotenv # Place to store my api key n stuff

load_dotenv()
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") # Save api key as attribute

app = Flask(__name__) # App is in the name of our script (main)
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/store-page')
def store_page():
    balls = ['bal-1.png', 'bal-2.png',
             'bal-3.png', 'bal-4.png',
             'bal-5.jpg', 'bal-6.png'] # List of ball images
    prices = [32.50, 40.00, 20.00,
              5.00, 15.99, 25.00] # List of prices we will get randomly. Prices change every refresh lol
    return render_template('store.html', balls=balls, prices=prices)

@app.route('/checkout/<ball>/<float:price>')
def checkout_ball(ball, price):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(price * 100), # Multiply price by 100 since stripe counts by cents, make int
                    "product_data": {"name": ball}
                },
                "quantity": 1,
            }
        ],
        success_url=url_for('success', _external=True),
        cancel_url=url_for('cancel', _external=True),
    )
    return redirect(session.url, code=303)
    # Return this session checkout object we just made as the URL, for user to buy

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')




if __name__ == '__main__': # Only run app if we are in this file
    app.run(debug=True)
