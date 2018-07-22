from flask import Flask,request,jsonify,make_response,render_template
app = Flask(__name__)

@app.route('/contacts',methods=['GET','POST','DELETE','PUT'])
def contacts():
    if request=='GET':
        return make_response(jsonify({"result": "coming soon"})),200
    elif request.method:
        return make_response(jsonify({"result": "Post Done"})),200
        # pass
@app.route('/profile/<username>')
def profile(username):
        return 'Hello there %s' % username

@app.route('/user/<int:post_id>')
def showint(post_id):
    return 'Hey There, your POST ID is %s' % post_id

@app.route('/welcome')
def welcome():
    return render_template('index.html')  # render a template

if __name__=='__main__':
    app.run(debug=True,port=3000)