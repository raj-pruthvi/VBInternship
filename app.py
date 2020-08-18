from flask import Flask,render_template,url_for,request, redirect
from bson.objectid import ObjectId
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from main import mongoConnect
collection = mongoConnect()
# retr = collection.find()

app = Flask(__name__)

def retrdata():
    	return collection.find()

@app.route('/')
def home():
    # retr = collection.find()
	retr = retrdata()
	return render_template('home.html', retr = retr)

@app.route('/',methods=['POST'])
def predict():
	df= pd.read_csv("spam.csv", encoding="latin-1")
	df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)

	df['label'] = df['class'].map({'ham': 0, 'spam': 1})
	X = df['message']
	y = df['label']
	
	cv = CountVectorizer()
	X = cv.fit_transform(X) 
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
	print("X_train")
	print(X_train)
	print("X_test")
	print(X_test)
	print("y_train")
	print(y_train)
	print("y_test")
	print(y_test)
	from sklearn.naive_bayes import MultinomialNB

	clf = MultinomialNB()
	clf.fit(X_train,y_train)
	print("Test score: ", clf.score(X_test,y_test))
	print("Train score: ", clf.score(X_train, y_train))
	if request.method == 'POST':
		message = request.form['message']
		data = [message]
		vect = cv.transform(data).toarray()
		my_prediction = clf.predict(vect)
		data_push = {
			"result" : "spam" if my_prediction[0] == 1 else "ham",
			"content": data[0]
		}
		global collection
		collection.insert_one(data_push)
		print(data_push)

	retr = collection.find()
	return render_template('home.html',prediction = my_prediction, retr = retr)

@app.route('/delete',methods=['POST'])
def unspam():
	retr = retrdata()
	print("in unspam")
	if(request.method == 'POST'):
		for i in request.form:
			print("request form content: ", i, " ", request.form[i])
		collection.delete_one({'_id': ObjectId( request.form['id'] )})
	return redirect(url_for('home'))
		# return render_template('home.html', retr = retr)
	# return render_template('home.html', retr = retr)

@app.route('/unmatch',methods=['POST'])
def unmatch():
	retr = retrdata()
	if(request.method == 'POST'):
		getRes = collection.find_one({'_id': ObjectId(request.form['id'])})
		if(getRes):
			setQueryVal = "spam" if getRes['result'] == "ham" else "ham" 
			collection.update({'_id': ObjectId( request.form['id'] ) }, {'$set': {"result": setQueryVal}} )
			print("updated now: ", getRes)

	return redirect(url_for('home'))



	# return render_template('home.html', retr = retr)



if __name__ == '__main__':
	app.run(debug=True)
