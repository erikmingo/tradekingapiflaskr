from flask import Flask, jsonify, render_template
import account
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def home():
#    values = account.stockvalue(account.getstocksym(account.urlquery()))
#    json = jsonify(values)

    return render_template('home.html')
    #return render_template('home.html', json=json)


#@app.route("/stocks/")
#def hello():
#    values = account.stockvalue(account.getstocksym(account.urlquery()))
#    json = jsonify(values)
#    return json

if __name__ == "__main__":
    app.run(debug = True)
