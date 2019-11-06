from flask import Flask,render_template,url_for,request, redirect
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
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
	
	# Extract Feature With CountVectorizer
	cv = CountVectorizer()
	X = cv.fit_transform(X) # Fit the Data
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
	#Naive Bayes Classifier
	from sklearn.naive_bayes import MultinomialNB

	clf = MultinomialNB()
	clf.fit(X_train,y_train)
	clf.score(X_test,y_test)
	#Alternative Usage of Saved Model
	# joblib.dump(clf, 'NB_spam_model.pkl')
	# NB_spam_model = open('NB_spam_model.pkl','rb')
	# clf = joblib.load(NB_spam_model)

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
		# if(data_push)
		# data_push['result'] = "spam" if my_prediction[0] == 1 else "ham"
		# data_push['content'] = data[0]
		# print(data[0], " ", my_prediction[0])
		print(data_push)
	# for i in retr:
    		# print(i)
	retr = collection.find()
	return render_template('home.html',prediction = my_prediction, retr = retr)

@app.route('/delete',methods=['POST'])
def unspam():
	retr = retrdata()
	print("in unspam")
	if(request.method == 'POST'):
		print("asdas")
		# getid = request.form['name']
		myquery = { "content": request.form['name'] }
		collection.delete_one(myquery)
		print("now deleting: ", myquery)
		return redirect(url_for('home'))



		# return render_template('home.html', retr = retr)
	return render_template('home.html', retr = retr)

@app.route('/unmatch',methods=['POST'])
def unmatch():
	retr = retrdata()
	if(request.method == 'POST'):
		# getid = request.form['name']
		myquery = { "content": request.form['name']}
		found = collection.find(myquery)
		getone = found[0]
		# print(getone)
		if(getone):
			collection.delete_one(getone)
			getone['result'] = "spam" if getone['result'] == "ham" else "ham"
			collection.insert_one(getone)
		print("updated now: ", getone)
		# if(getone):
			# collection.delete_one(myquery)
			# collection.insert_one(found)
		
		return redirect(url_for('home'))



		# return render_template('home.html', retr = retr)
	return render_template('home.html', retr = retr)



if __name__ == '__main__':
	app.run(debug=True)
