from flask import Flask , render_template ,redirect
from data import Product
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData,ForeignKey
from datetime import datetime
from flask import request
import sys
import sqlite3
from datetime import datetime
from sqlalchemy.sql import text 



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Products.db'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ProductMovements.db'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Location.db'

db = SQLAlchemy(app)


class Products(db.Model):
		id = db.Column(db.Integer,primary_key=True)
		name = db.Column(db.String(200),nullable=False)
		#add new
		ProductMov =db.relationship('ProductMovements',backref='author',lazy=True)

		def __repr__(self):
				    return '<Name %r>' % self.name 

class Location(db.Model):
		id = db.Column(db.Integer,primary_key=True)
		name = db.Column(db.String(200),nullable=False)
		      
		def __repr__(self):
				    return '<Movemt: %r>' % self.name 


class ProductMovements(db.Model):

		movement_id = db.Column(db.Integer,primary_key=True)
		timestamp = db.Column(db.String,default=datetime.utcnow)
		from_location = db.Column(db.String(200),nullable=False)
		to_location = db.Column(db.String(200),nullable=False)
		product_id = db.Column(db.String,db.ForeignKey('products.id'),nullable=False)
		qty = db.Column(db.Integer,nullable=False)


		def __repr__(self):
			    return'%s %s %s %s %s %s'%(self.movement_id, self.timestamp, self.from_location,self.to_location,self.product_id,self.qty)
			    #return '<L: %r>' % self.movement_id ,'<time :%r>'% self.timestamp,'<From_Location :%r>'% self.from_location,'<to_location :%r>'% self.to_location,'<product_id :%r>'% self.product_id,'<qty :%r>'% self.qty
app.debug =True

Product = Product()
@app.route('/')
def index():
	from app import db
	from app import ProductMovements
	m=ProductMovements.query.all()
	
	#print("the total number of school is ", db.session.query(ProductMovements).count())
	
	school = db.session.query(ProductMovements.product_id,ProductMovements.from_location,db.func.sum(ProductMovements.qty)).group_by(ProductMovements.from_location).all()
	print("Sum", school)
	db.create_all()
	# y=db.engine.execute('select * from Products')
	# result=y.fetchall()
	# print(result)


	return render_template('Home.html')

@app.route('/Report')
def Report():
	

	ProductBalance = db.session.query(ProductMovements.product_id,ProductMovements.from_location,db.func.sum(ProductMovements.qty).label("Sum")).group_by(ProductMovements.from_location,ProductMovements.product_id).all()

	


	return render_template('Report.html',ProductBalance=ProductBalance)

@app.route('/Product',methods=['POST','GET'])
def products():
     

	if request.method == "POST":
		product_name = request.form['name']
		new_product = Products(name=product_name)


		try:
			db.session.add(new_product)
			db.session.commit()
			return redirect('/Product')
		except:
			   return "There is a proplem"
	else:
		products =Products.query.order_by(Products.id)
		return render_template('Product.html',products=products)
    
@app.route('/Location',methods=['POST','GET'])
def Locations():

	if request.method == "POST":
		Movemnt_name = request.form['name']
		new_Movement = Location(name=Movemnt_name)


		try:
			db.session.add(new_Movement)
			db.session.commit()
			return redirect('/Location')
		except:
			   return sys.exc_info()[0]
	else:
		Locations = Location.query.order_by(Location.id)
		return render_template('Location.html',locations=Locations)



@app.route('/item/<string:id>/')
def item(id):
	return render_template('item.html', id =id)


@app.route('/ProductMovement',methods=['POST','GET'])
def ProductMovement():


	if request.method == "POST":
		product_name = request.form['ProductName']
		Date = request.form['dateTime']
		From_Location = request.form['FromLocation']
		to_location = request.form['ToLocation']
		Quntity = request.form['Quntity']

		new_Movement = ProductMovements(timestamp=Date,from_location=From_Location,
			to_location=to_location,product_id=product_name,qty=Quntity)

		try:
			
			db.session.add(new_Movement)
			db.session.commit()
			return redirect('/ProductMovement')
		except:
			   return sys.exc_info()[0]
	else:
		Locations=Location.query.all()
		Product=Products.query.all()
		ProductMovement = ProductMovements.query.order_by(ProductMovements.movement_id)
		return render_template('ProductMovement.html', ProductMovemnt=ProductMovement,products=Product,Location=Locations)
		



#Edit Product 
@app.route('/EditProduct/<int:id>',methods=['POST','GET'])
def EditProduct(id):
		ProductToupdate=Products.query.get_or_404(id)	
		if request.method == "POST":
			ProductToupdate.name =request.form['name']
			try:
				db.session.commit()
				return redirect('/Product')
			except:
		  		return "There is a proplem"
		else:
	         return render_template('EditProduct.html', ProductToupdate=ProductToupdate)

#Edit Product 
@app.route('/EditLocation/<int:id>',methods=['POST','GET'])
def EditLocation(id):
		LocationToupdate=Location.query.get_or_404(id)	
		if request.method == "POST":
			LocationToupdate.name =request.form['name']
			try:
				db.session.commit()
				return redirect('/Location')
			except:
		  		return "There is a proplem"
		else:
	         return render_template('EditLocation.html', LocationToupdate=LocationToupdate)




@app.route('/EditProductMovment/<int:id>',methods=['POST','GET'])
def EditProductMovment(id):
		ProductMovemtToupdate=ProductMovements.query.get_or_404(id)	
		if request.method == "POST":
			ProductMovemtToupdate.timestamp =request.form['dateTime']
			ProductMovemtToupdate.from_location=request.form['FromLocation']
			ProductMovemtToupdate.to_location=request.form['ToLocation']
			ProductMovemtToupdate.product_id=request.form['ProductName']
			ProductMovemtToupdate.qty=request.form['Quntity']
			try:
				db.session.commit()
				return redirect('/ProductMovement')
			except:
		  		return "There is a proplem"
		else:
	         return render_template('EditProductMovment.html', ProductMovemtToupdate=ProductMovemtToupdate)








if __name__ == "__main__":
    app.run(debug=True)

# if __name__=='__main__':
#       app.run(debug =True)