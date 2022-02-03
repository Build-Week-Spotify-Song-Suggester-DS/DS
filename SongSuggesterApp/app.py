from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    '''things within the home function will be run when
    the page is loaded. The page is loaded via a "GET" request'''

    print('rendering the page')

    '''When the form submits it will send a 'post' request
    to this route, so anything inside of this if statement
    will be run when the form is submitted'''

    if request.method == 'POST':
        print('submitting the form')
        user_input = request.values['search']
        print(user_input)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
