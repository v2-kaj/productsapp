from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as psycopg2

app = Flask(__name__)

# PostgreSQL database connection
conn = psycopg2.connect(
    dbname="webapp",
    user="admin",
    password="kajani",
    host="localhost",
    port="5432"
)
print("Connected to PostgreSQL database.")

@app.route('/')
def get_products():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")
        rows = cursor.fetchall()
        products = []
        for row in rows:
            product = {
                'id': row[0],
                'name': row[1],
                'price': float(row[2]),
                'description': row[3]
            }
            products.append(product)
        return render_template('products.html', products=products)
    except psycopg2.Error as e:
        return f"Error: {e}"

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product (name, price, description) VALUES (%s, %s, %s)", (name, price, description))
            conn.commit()
            return redirect(url_for('get_products'))
        except psycopg2.Error as e:
            return f"Error: {e}"
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
