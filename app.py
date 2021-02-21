import psycopg2					#importing to make connection with postgresql
from flask import Flask, render_template,request,session  #To connect to the webpage 
import pandas as pd 
import pandas.io.sql as psql
from flask_table import Table, Col
import os
import sys
import time
conn = psycopg2.connect(database="********", user = "******", password = "********", host = "localhost")
cur = conn.cursor()
app = Flask(__name__)

'''params = {

  'dbname': 'group_11',

  'user': 'group_11',

  'password': '191-574-834',

  'host': '10.17.51.19',

  'port': 5432

}
conn = psycopg2.connect(**params)
cur = conn.cursor()
app = Flask(__name__)'''

class Results(Table):
    id = Col('paperid', show=False)
    artist = Col('authorid')

@app.route('/')
def f2():
   return render_template("Home.html")

@app.route('/trains')
def main():
   return render_template("train.html")

@app.route('/hotels')
def f3():
   return render_template("hotels.html")

@app.route('/Train_Number')
def f1():
   return render_template("Train_Number.html")

@app.route('/Train_Name')
def f6():
	return render_template("Train_Name.html")

@app.route('/Train_Bet_Stations')
def f7():
	return render_template("Train_Bet_Stations.html")

@app.route('/Train_TimeTable')
def f8():
	return render_template("Train_TimeTable.html")

@app.route('/searchbystation')
def new_main():
	return render_template("project.html")

@app.route('/flights')
def f4():
	return render_template("Flights.html")

@app.route('/location',methods=['GET','POST'])
def f10():
	error = None
	if request.method == 'POST':
		#try:
		latitude=request.form['latitude']
		longitude=request.form['longitude']
		rows=[[latitude,longitude]]
		print(rows)
		print(type(latitude))
		cur=conn.cursor()
		if(len(latitude)==0):
			error="First Get your current location"
			return render_template("train.html",error=error)
		else:
			query="Select * from stations as x order by (point(x.longitude,x.lattitude)<@> point('"+longitude+"','"+latitude+"')) limit 1;"
			print(query)
			cur.execute(query)
			return render_template("nearstation.html",rows=cur.fetchall())
	else:
		return render_template("train.html")

@app.route('/location_airport',methods=['GET','POST'])
def f20():
	error = None
	if request.method == 'POST':
		#try:
		latitude=request.form['latitude']
		longitude=request.form['longitude']
		rows=[[latitude,longitude]]
		print(rows)
		print(type(latitude))
		cur=conn.cursor()
		if(len(latitude)==0):
			error="First Get your current location"
			return render_template("Flights.html",error=error)
		else:
			query="Select * from airports as x order by (point(x.longitude,x.lattitude)<@> point('"+longitude+"','"+latitude+"')) limit 1;"
			print(query)
			cur.execute(query)
			return render_template("nearairport.html",rows=cur.fetchall())
	else:
		return render_template("Flights.html")

@app.route('/location_hotel',methods=['GET','POST'])
def f34():
	error = None
	if request.method == 'POST':
		#try:
		latitude=request.form['latitude']
		longitude=request.form['longitude']
		rows=[[latitude,longitude]]
		print(rows)
		print(type(latitude))
		cur=conn.cursor()
		if(len(latitude)==0):
			error="First Get your current location"
			return render_template("hotels.html",error=error)
		else:
			query="Select * from hotels as x order by (point(x.longitude,x.lattitude)<@> point('"+longitude+"','"+latitude+"')) limit 1;"
			print(query)
			cur.execute(query)
			return render_template("nearhotel.html",rows=cur.fetchall())
	else:
		return render_template("hotels.html")

@app.route('/plan_tour',methods=['GET','POST'])
def f23():
	return render_template("test.html")

@app.route('/tour',methods=['GET','POST'])
def f22():
	error=None
	if request.method=='POST':
		from_city=request.form['From_City'].upper()
		to_city=request.form['To_City'].upper()
		transport=request.form['transport'].upper()
		print(transport)
		print(len(transport))
		trip=request.form['trip'].upper()
		if(transport=="NONE" or trip=="NONE"):
			error="Please fill all the details"
			return render_template("test.html", error=error)
		else:
			from_city_new = '%'+from_city.replace(' ', '%')+'%'
			to_city_new = '%'+to_city.replace(' ', '%')+'%'
			cur=conn.cursor()
			query="select property_name,property_address,hotel_star_rating,city from hotels,(select property_id from closest_hotel_to_station as p,(select code from stations where name ilike '%"+to_city+"%' limit 1) as t where p.code=t.code) as tt where hotels.property_id=tt.property_id ;"
			cur.execute(query)
			hotel_row=cur.fetchall()
			if(transport=="TRAINS"):
				if(trip=='ONEWAY'):
					print(from_city)
					print(to_city)
					query_train="select t1.departure,t2.arrival,t3.station_name,t3.departure,t4.arrival,t1.train_number,t3.train_number,(case when t3.departure>=(t2.arrival+'00:05:00') then (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (t4.day-t3.day)* time '24:00:00'+ (t4.arrival-t3.departure) + (t3.departure-t2.arrival) else (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (t4.day-t3.day)* time '24:00:00'+ (t4.arrival-t3.departure) + (t3.departure-t2.arrival)+'24:00:00' end) as t from schedule as t1,schedule as t2,schedule as t3,schedule as t4 where upper(t4.station_name) ilike '%"+to_city+"%' and upper(t1.station_name) ilike '%"+from_city+"%' and t2.station_code=t3.station_code and t1.id<t2.id and t3.id<t4.id and t1.train_number=t2.train_number and t3.train_number=t4.train_number and t2.departure-t2.arrival>'00:01:00' and t3.departure-t2.arrival>'00:05:00' and t1.departure-t1.arrival>'00:01:00' and t3.departure-t3.arrival>'00:01:00' and t4.departure-t4.arrival>'00:01:00' order by t limit 10 ;"
					cur.execute(query_train)
					print(query_train)
					train_row=cur.fetchall()
					print(train_row)
					return render_template("holiday.html", rows_train=train_row,rows=hotel_row,cname=to_city)
				else:
					query_train="select t1.departure,t2.arrival,t3.station_name,t3.departure,t4.arrival,t1.train_number,t3.train_number,(case when t3.departure>=(t2.arrival+'00:05:00') then (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (t4.day-t3.day)* time '24:00:00'+ (t4.arrival-t3.departure) + (t3.departure-t2.arrival) else (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (t4.day-t3.day)* time '24:00:00'+ (t4.arrival-t3.departure) + (t3.departure-t2.arrival)+'24:00:00' end) as t from schedule as t1,schedule as t2,schedule as t3,schedule as t4 where upper(t4.station_name) ilike '%"+to_city+"%' and upper(t1.station_name) ilike '%"+from_city+"%' and t2.station_code=t3.station_code and t1.id<t2.id and t3.id<t4.id and t1.train_number=t2.train_number and t3.train_number=t4.train_number and t2.departure-t2.arrival>'00:01:00' and t3.departure-t2.arrival>'00:05:00' and t1.departure-t1.arrival>'00:01:00' and t3.departure-t3.arrival>'00:01:00' and t4.departure-t4.arrival>'00:01:00' order by t limit 10 ;"
					cur.execute(query_train)
					train_row=cur.fetchall()
					query_train_rev="select t1.departure,t2.arrival,t3.station_name,t3.departure,t4.arrival,t1.train_number,t3.train_number,(case when t3.departure>=(t2.arrival+'00:05:00') then (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (t4.day-t3.day)* time '24:00:00'+ (t4.arrival-t3.departure) + (t3.departure-t2.arrival) else (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (t4.day-t3.day)* time '24:00:00'+ (t4.arrival-t3.departure) + (t3.departure-t2.arrival)+'24:00:00' end) as t from schedule as t1,schedule as t2,schedule as t3,schedule as t4 where upper(t4.station_name) ilike '%"+from_city+"%' and upper(t1.station_name) ilike '%"+to_city+"%' and t2.station_code=t3.station_code and t1.id<t2.id and t3.id<t4.id and t1.train_number=t2.train_number and t3.train_number=t4.train_number and t2.departure-t2.arrival>'00:01:00' and t3.departure-t2.arrival>'00:05:00' and t1.departure-t1.arrival>'00:01:00' and t3.departure-t3.arrival>'00:01:00' and t4.departure-t4.arrival>'00:01:00' order by t limit 10 ;"
					cur.execute(query_train_rev)
					train_row_rev=cur.fetchall()
					return render_template("holiday1.html",rows_train=train_row,rows=hotel_row,cname=to_city,rows_train_rev=train_row_rev)
			elif(transport=="FLIGHTS"):
				query="SELECT count(*) from flight_details where upper(from_city) ilike '%"+from_city+"%' and upper(to_city) ilike '%"+to_city+"%';"
				cur.execute(query)
				no=cur.fetchone()[0]
				if(no!=0):
					if(trip=='ONEWAY'):
						query_flight="select from_airport,to_airport,airline,flight_number,replace(translate(days::text,'123467','SMTWFS'),'5','Th'),Concat(LPAD((sched_time/100)::text, 2, '0'),':',LPAD((sched_time%100)::text, 2, '0')) from flight_details where upper(from_city) ilike '%"+from_city+"%' and upper(to_city) ilike '%"+to_city+"%';"
						cur.execute(query_flight)
						ro=cur.fetchall()
						return render_template("holiday_f.html",flight_row=ro,rows=hotel_row,cname=to_city)
					else:
						query_flight="select from_airport,to_airport,airline,flight_number,replace(translate(days::text,'123467','SMTWFS'),'5','Th'),Concat(LPAD((sched_time/100)::text, 2, '0'),':',LPAD((sched_time%100)::text, 2, '0')) from flight_details where upper(from_city) ilike '%"+from_city+"%' and upper(to_city) ilike '%"+to_city+"%';"
						cur.execute(query_flight)
						ro=cur.fetchall()
						query_flight_rev="select from_airport,to_airport,airline,flight_number,replace(translate(days::text,'123467','SMTWFS'),'5','Th'),Concat(LPAD((sched_time/100)::text, 2, '0'),':',LPAD((sched_time%100)::text, 2, '0')) from flight_details where upper(from_city) ilike '%"+to_city+"%' and upper(to_city) ilike '%"+from_city+"%';"
						cur.execute(query_flight_rev)
						ro_rev=cur.fetchall()
						return render_template("holiday_f_rev.html",flight_row=ro,rows=hotel_row,cname=to_city,flight_row_rev=ro_rev)
				else:
					error="Sorry, No Fligths are availabe between these cities"
					return render_template("flight_error.html",rows=hotel_row,cname=to_city,error=error)
			else:
				if(trip=='ONEWAY'):
					query="select iata from airports where upper(city) ilike '%"+to_city+"%';"
					cur.execute(query)
					code=cur.fetchone()[0]
					print(code)
					query_flight="select t1.departure,t2.station_name,f3.from_airport,t2.arrival,f3.sched_time,t1.train_number,f3.flight_number,(case when Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'),':00')::time>=t2.arrival+'00:15:30'::time*a_s.distance*1.61 then (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'),':00')::time-t2.arrival) + '00:15:30'::time*a_s.distance*1.61 else (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure)  + (Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'))::time-t2.arrival)+'24:00:00' + '00:15:30'::time*a_s.distance*1.61 end) as time from schedule as t1,schedule as t2,flights as f3,closest_airport_to_station as a_s where f3.to_Airport='"+code+"' and upper(t1.station_name) ilike '%"+from_city+"%' and a_s.code=t2.station_code and a_s.iata=f3.from_airport and t1.train_number=t2.train_number and t1.id<t2.id and t2.departure-t2.arrival>'00:01:00' and t1.departure-t1.arrival>'00:01:00' and Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'),':00')::time-t2.arrival>'00:15:30'::time*a_s.distance*1.61 order  by time limit 10 ;"
					cur.execute(query_flight)
					ro=cur.fetchall()
					return render_template("holiday_flight.html",flight_row=ro,rows=hotel_row,cname=to_city)
				else:
					query="select iata from airports where upper(city) ilike '%"+to_city+"%';"
					cur.execute(query)
					code=cur.fetchone()[0]
					print(code)
					query_flight="select t1.departure,t2.station_name,f3.from_airport,t2.arrival,f3.sched_time,t1.train_number,f3.flight_number,(case when Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'),':00')::time>=t2.arrival+'00:15:30'::time*a_s.distance*1.61 then (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure) + (Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'),':00')::time-t2.arrival) + '00:15:30'::time*a_s.distance*1.61 else (t2.day-t1.day)* time '24:00:00'+ (t2.arrival-t1.departure)  + (Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'))::time-t2.arrival)+'24:00:00' + '00:15:30'::time*a_s.distance*1.61 end) as time from schedule as t1,schedule as t2,flights as f3,closest_airport_to_station as a_s where f3.to_Airport='"+code+"' and upper(t1.station_name) ilike '%"+from_city+"%' and a_s.code=t2.station_code and a_s.iata=f3.from_airport and t1.train_number=t2.train_number and t1.id<t2.id and t2.departure-t2.arrival>'00:01:00' and t1.departure-t1.arrival>'00:01:00' and Concat(LPAD((f3.sched_time/100)::text, 2, '0'),':',LPAD((f3.sched_time%100)::text, 2, '0'),':00')::time-t2.arrival>'00:15:30'::time*a_s.distance*1.61 order  by time limit 10 ;"
					cur.execute(query_flight)
					ro=cur.fetchall()
					error="Sorry, Return Information is not available"
					return render_template("holiday_flight_rev.html",flight_row=ro,rows=hotel_row,cname=to_city,error=error)

	return render_template("test.html")


@app.route('/allresults')
def allresults():
	cur = conn.cursor()
	cur.execute(
		"""
        SELECT trainnumber,trainname,traintype,from_station_name,to_station_name FROM trains
        Limit 50
    """)
	return render_template("base.html", rows=cur.fetchall())

@app.route('/airport_code',methods=['GET','POST'])
def f21():
	if request.method=='POST':
		city_name=request.form['city'].upper()
		cur=conn.cursor()
		query1="SELECT count(*) from airports where upper(city) ilike '%"+city_name+"%';"
		cur.execute(query1)
		a=cur.fetchone()[0]
		if(a==0):
			rows=[['Null','Sorry, your city dont have any airport']]
		else:	
			query="SELECT iata,name,city,type,home_link,wikipedia_link from airports where upper(city) ilike '%"+city_name+"%';"
			cur.execute(query)
			rows=cur.fetchall()	
		return render_template("flight2.html",rows=rows)
	else:
		return render_template("flights.html")

@app.route('/train' ,methods=['GET','POST'])
def train():
	if request.method == 'POST':
		trainnumber=request.form['Train_Number']
		cur=conn.cursor()
		query="SELECT train_number,train_name,train_type,from_station_name,from_station_code,to_station_name,to_station_code,arrival,departure,distance,duration_h, chair_car,first_ac,first_class,second_ac,sleeper,third_ac, train_zone, duration_m, return_train FROM trains where train_number='"+trainnumber+"';"
		
		cur.execute(query)
		ro=cur.fetchall()
		print(ro)
		return render_template("train2.html",rows=ro)
	else:
		return render_template("searchbytrainnumber.html")	

@app.route('/contact_us' ,methods=['GET','POST'])
def f5():
	return render_template("contact_us.html")

@app.route('/trainname' ,methods=['GET','POST'])
def train_name():
	if request.method == 'POST':
		tname=request.form['Train_Name'].upper()
		tnamenew = '%'+tname.replace(' ', '%')+'%'
		cur=conn.cursor()
		query1="SELECT train_number, train_name,departure,arrival,train_type FROM trains where upper(train_name) ilike'"+tnamenew+"';"
		cur.execute(query1)
		r1=cur.fetchall()
		query2 = "SELECT distinct train_type FROM trains where train_name ilike'"+tnamenew+"';"
		cur.execute(query2)
		r2=cur.fetchall()
		return render_template("train1.html",rows=r1, rtype = r2, trname = tnamenew, f=1)
	else:
		return render_template("train.html")

@app.route('/trainname/filter1' ,methods=['GET','POST'])
def train_name_filter1():
	if request.method=='POST':
		ttype=request.form.getlist('trains')
		tnew = [[x] for x in ttype]
		tname=request.form['Train_Name']
		train_string = "('"+"','".join(ttype)+"')"
		cur=conn.cursor()
		print(tnew)
		print(tname)
		print(train_string)
		query="SELECT train_number, train_name,departure,arrival,train_type FROM trains where upper(train_name) ilike'"+tname+"' and train_type in "+train_string+";"
		cur.execute(query)
		row = cur.fetchall()
		return render_template("train1.html",rows=row,rtype = tnew, tstring = train_string, trname = tname,f=1)
	else:
		return render_template("train.html")

@app.route('/trainname/filter2' ,methods=['GET','POST'])
def train_name_filter2():
	if request.method=='POST':
		ttype=request.form.getlist('strain')
		ttypes = request.form.getlist('trains')
		tnews = [[x] for x in ttypes]
		train_strings = "('"+"','".join(ttypes)+"')"
		tname=request.form['Train_Name']
		#type_st=request.form['train_type']
		
		#print(train_strings)
		
		cur=conn.cursor()
		tnew = " = 't' or ".join(ttype) +" = 't'"
		#print(tnew)
		query="SELECT train_number, train_name,departure,arrival,train_type FROM trains where upper(train_name) ilike'"+tname+"' and ("+tnew+") and train_type in "+train_strings+";"
		cur.execute(query)
		#print(query)
		row = cur.fetchall()
		#print(row)
		query2 = "SELECT distinct train_type FROM trains,(SELECT train_number FROM trains where upper(train_name) ilike'"+tname+"' and ("+tnew+") ) as t1 where t1.train_number = trains.train_number and train_type in "+train_strings+";"
		cur.execute(query2)
		#print(query)
		r2=cur.fetchall()
		#print(r2)
		return render_template("train1.html", rows=row,trname = tname,rtype=r2,tstring = train_strings, f=1 )
	else:
		return render_template("train.html")



@app.route('/searchbetstations' ,methods=['GET','POST'])
def tbs():
	if request.method == 'POST':
		Fstation=request.form['From_Station'].upper()
		Tstation=request.form['To_Station'].upper()
		cur=conn.cursor()
		query2="SELECT trains.train_number, train_name, V3.DEPARTURE,v3.ARRIVAL,train_type FROM trains, (select V1.train_number,V1.DEPARTURE,v2.ARRIVAL from (select train_number,id, DEPARTURE from schedule where upper(station_name) ilike '%"+Fstation+"%') AS V1, (select train_number,id, ARRIVAL  from schedule where upper(station_name) ilike '%"+Tstation+"%') AS V2 WHERE V1.TRAIN_NUMBER = V2.TRAIN_NUMBER AND V1.ID < V2.ID) as V3 where trains.train_number = V3.train_number ;"
		cur.execute(query2)
		return render_template("train1.html",rows=cur.fetchall(),f=0)
	else:
		return render_template("train.html")

@app.route('/trainroutes' , methods=['GET','POST'])
def tr():
	if request.method == 'POST':
		trainnumber=request.form['Train_Number']
		cur=conn.cursor()
		query="SELECT id,arrival,departure,station_code,station_name,train_name,address from schedule,stations where train_number='"+trainnumber+"' and stations.code = schedule.station_code order by id;"
		cur.execute(query,conn)
		return render_template("train3.html",rows=cur.fetchall(), tno = trainnumber)
	else:
		return render_template("train.html")
    
#Hotels

@app.route('/allhotels' ,methods=['GET','POST'])
def allhotel():
	if request.method == 'POST':
		cityname=request.form['City_Name'].upper()
		hname=request.form['Hotel_Name'].upper()
		hnamenew = '%'+hname.replace(' ', '%')+'%'
		cur=conn.cursor()
		start=time.time()
		query="SELECT distinct property_name,property_address,hotel_star_rating,city FROM hotels where upper(city) ilike '%"+cityname+"%'and upper(property_name) ILIKE '"+hnamenew+"';"
		print(query)
		print(time.time()-start)
		cur.execute(query)
		row =cur.fetchall()
		return render_template("hotel1.html",rows=row, hnames = hnamenew, cname =cityname)
		
	else:
		return render_template("hotels.html")

@app.route('/allhotels/tour',methods=['GET','POST'])
def allhotel_tour():
	if request.method == 'POST':
		cityname=request.form['City_Name'].upper()
		hname=request.form['Hotel_Name'].upper()
		hnamenew = '%'+hname.replace(' ', '%')+'%'
		cur=conn.cursor()
		query="SELECT property_name,property_address,hotel_star_rating,city FROM hotels where upper(city) ilike '%"+cityname+"%'and upper(property_name) ILIKE '"+hnamenew+"'limit 10;"
		
		cur.execute(query)
		row =cur.fetchall()
		return render_template("holiday.html",rows=row, cname =cityname)
		
	else:
		return render_template("hotels.html")

@app.route('/allhotels/filter/tour',methods=['GET','POST'])
def allhotel_filter_tour():
	if request.method=='POST':
		ratings=request.form.getlist('Rating')
		cityname=request.form['City_Name'].upper()
		rows_train=request.form['rows_train']
		print(rows_train)
		cur=conn.cursor()
		#print(ratings[0])
		query="SELECT property_name,property_address,hotel_star_rating,city FROM hotels where upper(city) ilike '%"+cityname+"%'and hotel_star_rating >= "+ratings[0]+" limit 10;"
		#print(query)
		cur.execute(query)
		return render_template("holiday.html",rows=cur.fetchall(), cname =cityname ,rows_train=rows_train)
	else:
		return render_template("hotels.html")

@app.route('/hdetails/tour' ,methods=['GET','POST'])
def hdetail_tour():
	if request.method == 'POST':
		cityname=request.form['City_Name'].upper()
		hname=request.form['Hotel_Name'].upper()
		cur=conn.cursor()
		query="SELECT distinct property_name, property_address, hotel_star_rating, hotels.facilities, room_types, hotel_overview, highlight_value, round(location_,2),round(hospitality,2),round(traveller_ratings.facilities,2),round(cleanliness,2),round(valueformoney,2),round(food,2) FROM hotels left join traveller_ratings on traveller_ratings.property_id=hotels.property_id where upper(city) ilike  '%"+cityname+"%'and upper(property_name) = '"+hname+"';"
		cur.execute(query)
		ro=cur.fetchall()
		print(ro)
		return render_template("holiday.html",rows=ro)
		
	else:
		return render_template("hotels.html")

@app.route('/allhotels/filter' ,methods=['GET','POST'])
def allhotel_filter():
	if request.method=='POST':
		ratings=request.form.getlist('Rating')
		cityname=request.form['City_Name'].upper()
		hname=request.form['Hotel_Name'].upper()
		cur=conn.cursor()
		#print(ratings[0])
		start=time.time()
		query="SELECT property_name,property_address,hotel_star_rating,city FROM hotels where upper(city) ilike '%"+cityname+"%'and upper(property_name) ILIKE '"+hname+"' and hotel_star_rating >= "+ratings[0]+";"
		print(query)
		cur.execute(query)
		print(time.time()-start)
		return render_template("hotel1.html",rows=cur.fetchall(),hnames = hname, cname =cityname )
	else:
		return render_template("hotels.html")

@app.route('/hdetails' ,methods=['GET','POST'])
def hdetail():
	if request.method == 'POST':
		cityname=request.form['City_Name'].upper()
		hname=request.form['Hotel_Name'].upper()
		cur=conn.cursor()
		start=time.time()
		query="SELECT distinct property_name, property_address, hotel_star_rating, hotels.facilities, room_types, hotel_overview, highlight_value, round(location_,2),round(hospitality,2),round(traveller_ratings.facilities,2),round(cleanliness,2),round(valueformoney,2),round(food,2) FROM hotels left join traveller_ratings on traveller_ratings.property_id=hotels.property_id where upper(city)='"+cityname+"'and upper(property_name) = '"+hname+"' limit 1;"
		cur.execute(query)
		print(time.time()-start)
		print(query)
		ro=cur.fetchall()
		return render_template("hotel2.html",rows=ro)
		
	else:
		return render_template("hotels.html")   


@app.route('/uhdetails' ,methods=['GET','POST'])
def hdetail_u():
	if request.method == 'POST':
		email=request.form['mail']
		user_n=request.form['nam']
		cityname=request.form['City_Name'].upper()
		hname=request.form['Hotel_Name'].upper()
		cur=conn.cursor()
		start=time.time()
		query="SELECT distinct property_name, property_address, hotel_star_rating, hotels.facilities, room_types, hotel_overview, highlight_value, round(location_,2),round(hospitality,2),round(traveller_ratings.facilities,2),round(cleanliness,2),round(valueformoney,2),round(food,2) FROM hotels left join traveller_ratings on traveller_ratings.property_id=hotels.property_id where upper(city)='"+cityname+"'and upper(property_name) = '"+hname+"';"
		cur.execute(query)
		print(time.time()-start)
		print(query)
		ro=cur.fetchall()
		return render_template("u_hotel.html",rows=ro,user=email,uname=user_n)
		
	else:
		return render_template("hotels.html")
    
'''@app.route('/hotelRegistration' , methods=['GET','POST'])
def hotel_reg():
		return render_template("hotelreg.html")'''
    
@app.route('/hotelratings' , methods=['GET','POST'])
def hotel_rate():
	if request.method == 'POST':
		cityname=request.form['City_Name']
		hname=request.form['Hotel_Name']
		return render_template("HotelRating.html",rows=[hname,cityname])	
	else:
		return render_template("hotels.html")

@app.route('/hotelrating2' , methods=['GET','POST'])
def hotel_rate2():
	if request.method == 'POST':
		clean=request.form['cleanliness']
		ffood=request.form['Food']
		vmoney=request.form['vfmoney']
		room=request.form['rfacilities']
		address=request.form['location']
		host=request.form['hospitality']
		cityname=request.form['City_Name']
		hname=request.form['Hotel_Name']
		cur=conn.cursor()
		start=time.time()
		query1="SELECT count, location_,hospitality,traveller_ratings.facilities,cleanliness,valueformoney,food,hotels.property_id FROM hotels left join traveller_ratings on traveller_ratings.property_id=hotels.property_id where city ='"+cityname+"'and property_name = '"+hname+"';"

		cur.execute(query1)
		print(time.time()-start)
		print(query1)
		r1=cur.fetchall()
		#print(type(r1[0][1]))
		if (r1[0][1]) is None :
			list_new = [1, float(address), float(host), float(room), float(clean), float(vmoney), float(ffood), r1[0][7]]
			start=time.time()
			query3 = "insert into traveller_ratings (count, location_, hospitality, facilities, cleanliness, valueformoney, food, property_id) values ( "+str(list_new[0])+" , "+str(list_new[1])+", "+str(list_new[2])+", "+str(list_new[3])+", "+str(list_new[4])+", "+str(list_new[4])+", "+str(list_new[6])+", '"+list_new[7]+"');"
			cur.execute(query3)
			print(time.time()-start)
			print(query3)
		else:
			list_new = [r1[0][0]+1, (r1[0][1]*r1[0][0] + int(address))/(r1[0][0]+1), (r1[0][2]*r1[0][0] + int(host))/(r1[0][0]+1), (r1[0][3]*r1[0][0] + int(room))/(r1[0][0]+1), (r1[0][4]*r1[0][0] + int(clean))/(r1[0][0]+1), (r1[0][5]*r1[0][0] + int(vmoney))/(r1[0][0]+1), (r1[0][6]*r1[0][0] + int(ffood))/(r1[0][0]+1), r1[0][7]]
			start=time.time()
			query2="update traveller_ratings set count = "+str(list_new[0])+", location_ = "+str(list_new[1])+", hospitality = "+str(list_new[2])+", facilities = "+str(list_new[3])+", cleanliness = "+str(list_new[4])+", valueformoney = "+str(list_new[5])+", food = "+str(list_new[6])+" where property_id = '"+list_new[7]+"';"
			#print(query2)
			cur.execute(query2)
			print(time.time()-start)
			print(query2)
		conn.commit()
		return render_template("hotelrateSuccess.html")
		
	else:
		return render_template("hotels.html")

#flight

@app.route('/flightnumber' , methods=['GET','POST'])
def flight_number():
	if request.method=='POST':
		flightnumber=request.form['Flight_Number']
		cur=conn.cursor()
		query="SELECT flight_number,airline,from_airport,to_airport,sched_time,days from flights where flight_number='"+flightnumber+"';"
		cur.execute(query,conn)
		return render_template("searchflights.html",rows=cur.fetchall())
	else:
		return render_template("flights.html")

@app.route('/flight/filter' , methods=['GET','POST'])
def flight_number_filter():
	error = None
	if request.method=='POST':
		airline=request.form.getlist('Airline')
		flightnumber=request.form['Flight_Number']
		air_string = "('"+"','".join(airline)+"')"
		cur=conn.cursor()
		query="SELECT flight_number,airline,from_airport,to_airport,sched_time,time_zone from flights where flight_number='"+flightnumber+"' and airline in "+air_string+";"
		cur.execute(query,conn)
		row = cur.fetchall()
		if len(row)==0 :
			error = 'No flights for given airline types'
		else:
			return render_template("searchflights.html",rows=row)
	return render_template("searchflights.html", error=error)


@app.route('/airpline' , methods=['GET','POST'])
def airpline():
	if request.method=='POST':
		airline=request.form['airpline']
		cur=conn.cursor()
		start=time.time()
		query="SELECT flight_number,airline,from_airport,to_airport,sched_time,days from flights where upper(airline)='"+airline+"';"
		cur.execute(query,conn)
		print(time.time()-start)
		print(query)
		return render_template("searchflights.html",rows=cur.fetchall())
	else:
		return render_template("Flights.html")

@app.route('/searchbetairports' , methods=['GET','POST'])
def airports():
	e1=None
	if request.method=='POST':
		from_city=request.form['from_airport'].upper()
		to_city=request.form['to_airport'].upper()
		cur=conn.cursor()
		query="select flight_number,airline,from_airport,to_airport,Concat(LPAD((sched_time/100)::text, 2, '0'),':',LPAD((sched_time%100)::text, 2, '0')),replace(translate(days::text,'123467','SMTWFS'),'5','Th') from flight_details where upper(from_city) ilike '%"+from_city+"%' and upper(to_city) ilike '%"+to_city+"%' ;"
		cur.execute(query)
		row=cur.fetchall()
		if(len(row)==0):
			e1="Flights are not available between given city names"
			return render_template("Flights.html",e1=e1)
		else:
			return render_template("searchflights.html",rows=row)
	else:
		return render_template("Flights.html")

#user login signup
@app.route('/signup' , methods=['GET','POST'])
def signup1():
	if request.method=='POST':
		return render_template("signup_new.html")
	else:
		return render_template("hotels.html")

@app.route('/sign' , methods=['GET','POST'])
def signup2():
	error1 = None
	error = None
	if request.method=='POST':
		cur=conn.cursor()
		nam=request.form['nam']
		email=request.form['email']
		password=request.form['psw']
		repeat=request.form['psw-repeat']
		start=time.time()
		query="SELECT count(*) from users where email_id='"+email+"';"
		cur.execute(query,conn)
		print(time.time()-start)
		print(query)
		a=cur.fetchone()
		noe=a[0]
		if(noe!=0):
			error1 = 'User already exist'
		else:	
			if(password==repeat):
				cur=conn.cursor()
				start=time.time()
				query="INSERT INTO users VALUES ('"+email+"',crypt('"+password+"', gen_salt('bf')), '"+nam+"');"
				cur.execute(query,conn)
				print(time.time()-start)
				print(query)
				conn.commit()
				return render_template("login_new.html")
			else:
				error = 'Password does not match'
	return render_template("signup_new.html", e1 = error,e2 =  error1)

@app.route('/login' , methods=['GET','POST'])
def login1():
	if request.method=='POST':
		return render_template("login_new.html")
	else:
		return render_template("hotels.html")

@app.route('/afterlogin',methods=['GET','POST'])
def login2():
	error = None
	error2 = None
	if request.method=='POST':
		usern=request.form['email']
		password=request.form['psw']
		cur=conn.cursor()
		start=time.time()	
		query="SELECT password, username from users where email_id='"+usern+"';"
		cur.execute(query)
		print(time.time()-start)
		print(query)
		row=cur.fetchall()
		if(len(row)==0):
			error2  = 'No such user exist'
		else:
			password_d=row[0][0]
			start=time.time()
			query2="select crypt('"+password+"', '"+password_d+"');"
			
			cur.execute(query2)
			print(time.time()-start)
			print(query2)
			row2=cur.fetchall()
			print(row2)
			print(password_d)
			if(row2[0][0]==password_d):
				
				return render_template("login_new2.html", user = usern, uname =row[0][1] )
			else:
				error = 'Incorrect password'
	return render_template("login_new.html" , e1 = error, e2 = error2,)

@app.route('/user_hotels' , methods=['GET','POST'])
def ureghotel():
	if request.method=='POST':
		email=request.form['mail']
		user_n=request.form['nam']
		cur=conn.cursor()
		start=time.time()
		query="SELECT property_name,property_address,hotel_star_rating,city, hotels.property_id FROM hotels, hotel_permissions where email_id = '"+email+"' and hotel_permissions.property_id = hotels.property_id;"
		cur.execute(query,conn)
		print(time.time()-start)
		print(query)
		row = cur.fetchall()
		#print(row[0][4])
		return render_template("user_hotel1.html", rows = row, user = email, uname = user_n)
	else:
		return render_template("login_new2.html")

@app.route('/user_hotel_reg' ,methods=['GET','POST'])
def hotelreg():
	error = None
	if request.method == 'POST':
		proId=request.form['Hotel_Id']
		email=request.form['mail']
		user_n=request.form['nam']
		cur=conn.cursor()
		start=time.time()
		query="SELECT property_id FROM hotels where upper(property_id)='"+proId.upper()+"';"
		cur.execute(query)
		print(time.time()-start)
		print(query)
		listId=cur.fetchall()
		if len(listId)==1 :
			error = 'HotelId already exist'
		else:
			return render_template("hotelreg.html",rows=[proId], user = email,uname = user_n)
		
	return render_template("login_new2.html", error=error, user = email,uname = user_n)	

@app.route('/user_reghotel1' ,methods=['GET','POST'])
def hotel_reg2():
	error = None;
	error2 = None;
	if request.method == 'POST':
		pid = request.form['PropertyId']
		hotelname=request.form['Property_Name']
		cityname=request.form['City_Name']
		statename=request.form['State_Name']
		starrate=request.form['hotel_rate']
		
		purl=request.form['url']
		rtype=request.form['room']
		oview=request.form['Overview']
		location=request.form['Address']
		rfacilities=request.form['Facilities']
		email=request.form['mail']
		user_n=request.form['nam']
		cur=conn.cursor()
		query1 = "select pageurl from hotels where pageurl = '"+purl+"';"
		cur.execute(query1)
		r1 = cur.fetchall()
		if(len(r1)==1):
			error = "Hotel url already exist"
			return render_template("hotelreg.html",rows=[pid],user = email, uname = user_n, e1 = error, e2 = error2)
		elif(int(starrate)>5 or int(starrate)<0):
			error2 = "Star rating must be an integer between 0 and 5" 
			return render_template("hotelreg.html",rows=[pid],user = email, uname = user_n, e1 = error, e2 = error2)
		else:
			
			start=time.time()
			query="insert into hotels (property_name,property_id, city, state, hotel_star_rating, pageurl, room_types, hotel_overview, property_address, facilities) values ('"+hotelname+"','"+pid+"', '"+cityname+"', '"+statename+"', "+starrate+", '"+purl+"', '"+rtype+"', '"+oview+"', '"+location+"', '"+rfacilities+"');"
			cur.execute(query)
			print(time.time()-start)
			print(query)
			start=time.time()
			query2 = "insert into hotel_permissions (email_id,property_id) values ('"+email+"', '"+pid+"');"
			cur.execute(query2)
			print(time.time()-start)
			print(query2)
			conn.commit()
			return render_template("hotelregSuccess.html", user = email, uname = user_n)
	else:	
		return render_template("hotelreg.html")

@app.route('/edithotel' , methods=['GET','POST'])
def user_edit():
	if request.method == 'POST':
		cityname=request.form['City_Name']
		hname=request.form['Hotel_Name']
		email=request.form['mail']
		user_n=request.form['nam']
		row=[hname,cityname,email,user_n]
		query = "select property_id,property_name, city, state, hotel_star_rating, pageurl, room_types, hotel_overview, property_address, facilities from hotels where property_name = '"+hname+"' and city = '"+cityname+"';"
		cur.execute(query)
		listId=cur.fetchall()		
		print(row)
		print(listId)
		return render_template("hoteledit.html",user = email, uname = user_n,rows=listId)	
	else:
		return render_template("hotels.html")

@app.route('/hdetails_changes' ,methods=['GET','POST'])
def hotel_update():
	if request.method == 'POST':
		pid = request.form['PropertyId']
		hotelname=request.form['Property_Name']
		cityname=request.form['City_Name']
		statename=request.form['State_Name']
		starrate=request.form['hotel_rate']
		purl=request.form['url']
		rtype=request.form['room']
		oview=request.form['Overview']
		location=request.form['Address']
		rfacilities=request.form['Facilities']
		email=request.form['mail']
		user_n=request.form['nam']
		cur=conn.cursor()
		start=time.time()
		query = "update hotels set property_name = '"+hotelname+"', city = '"+cityname+"', state = '"+statename+"', hotel_star_rating = "+str(starrate)+", pageurl = '"+purl+"', room_types= '"+rtype+"', hotel_overview= '"+oview+"', property_address= '"+location+"', facilities= '"+rfacilities+"' where property_id = '"+pid+"';"
		cur.execute(query)
		print(time.time()-start)
		print(query)
		conn.commit()
		return render_template("hotelChangesSuccess.html", user = email, uname = user_n)
		
	else:
		return render_template("hotels.html")

@app.route('/deletehotel' , methods=['GET','POST'])
def user_delete():
	if request.method == 'POST':
		cityname=request.form['City_Name']
		hname=request.form['Hotel_Name']
		email=request.form['mail']
		user_n=request.form['nam']
		proid = request.form['pid']
		row=[hname,cityname,email,user_n,proid]	
		start=time.time()
		query2 = "delete from hotels where property_id = '"+proid+"';"	
		cur.execute(query2)
		print(time.time()-start)
		print(query2)
		query="SELECT property_name,property_address,hotel_star_rating,city,hotels.property_id FROM hotels, hotel_permissions where email_id = '"+email+"' and hotel_permissions.property_id = hotels.property_id;"
		cur.execute(query)
		return render_template("user_hotel_delete.html", rows = cur.fetchall(), user = email, uname = user_n)
	else:
		return render_template("hotels.html")	

@app.route('/logout', methods=['GET','POST'])
def logout():
	if request.method == 'POST':
		return render_template("hotels.html")

@app.route('/nlogout', methods=['GET','POST'])
def nlogout():
	if request.method == 'POST':
		email=request.form['mail']
		user_n=request.form['nam']
		return render_template("login_new2.html", user = email, uname = user_n)

@app.route('/dashboard' ,methods=['GET','POST'])
def dash():
	if request.method == 'POST':
		email=request.form['xmail']
		user_n=request.form['nam']
		return render_template("login_new2.html", user = email, uname = user_n)
	else:
		return render_template("hotels.html")

if __name__ == '__main__':
   app.debug=True
   app.run()


