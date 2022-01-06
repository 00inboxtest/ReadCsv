from flask import Flask, jsonify
from flask_restful import reqparse
import pandas as pd
import holidays
import datetime

app = Flask(__name__)

# @app.route('/getproduct', methods=['GET'])
# def getproduct_records():
#     data = pd.read_csv('product_hierarchy.csv')
#     data = data.to_dict('records')
#     return jsonify({'data' :data,'code':200})



# Rquired parms for Post method
# {
#     "hierarchy1_id":"H00",
#     "start_date":"2017-01-03",
#     "end_date":"2017-01-03"
# }


# http://127.0.0.1:5000/getsale_productdata
@app.route('/getproduct_hierarchywise', methods=['POST'])
def getproduct_store_records():
    parser = reqparse.RequestParser()
    parser.add_argument('hierarchy1_id', required=True)
    parser.add_argument('start_date', required=True)
    parser.add_argument('end_date', required=True)
    args = parser.parse_args()

    #read product data
    data = pd.read_csv('product_hierarchy.csv')        
    data = data [(data ["hierarchy1_id"] == args['hierarchy1_id'])]
    data = data.to_dict('records')
    product_ids=[]

    for x in data:
        product_ids.append(x['product_id'])
    # print(product_ids)

    #read sales data
    salesData = pd.read_csv('sales.csv')
    
    # date filter
    date_filter=salesData['date'].between(args['start_date'],args['end_date'])
    salesData=salesData[date_filter]
    
    #product filter
    product_filter=salesData.product_id.isin(product_ids)
    salesData=salesData[product_filter]

    #sum of revenu and sales
    total_revenue=salesData['revenue'].sum()
    total_sales=salesData['sales'].sum()

    #output
    salesData = salesData.to_dict('records')

    return jsonify({
            'total_revenue':total_revenue,
            'total_sales':total_sales,
          })


# Rquired parms for Post method
# {
#     "product_id":"P0001",
#     "start_date":"2017-01-02",
#     "end_date":"2017-01-03"
# }

# http://127.0.0.1:5000/getsale_productdata
@app.route('/getsale_productdata', methods=['POST'])
def getsaledata_product_records():
    parser = reqparse.RequestParser()
    parser.add_argument('product_id', required=True)
    parser.add_argument('start_date', required=True)
    parser.add_argument('end_date', required=True)
    args = parser.parse_args()

    #read product data
    data = pd.read_csv('product_hierarchy.csv')        
    data = data [(data ["product_id"] == args['product_id'])]
    data = data.to_dict('records')

    total_dimensions=0
    for x in data:
        total_dimensions=x['product_length']*x['product_width']*x['product_depth']

    #read sales data
    salesData = pd.read_csv('sales.csv')
    
    # date filter
    date_filter=salesData['date'].between(args['start_date'],args['end_date'])
    salesData=salesData[date_filter]
    
    #product filter
    product_filter=(salesData["product_id"] == args['product_id'])
    salesData=salesData[product_filter]

    # sum of total sales
    total_sales=salesData['sales'].sum()

    # calculate total volume
    total_volume=total_dimensions*total_sales
    
    #output
    salesData = salesData.to_dict('records')

    return jsonify({
            'total_volume':total_volume,
            'total_sales':total_sales,
            'total_dimensions':total_dimensions,
          })



# Rquired parms for Post method
# {
#     "city_id":"C013",
#     "start_date":"2017-01-03",
#     "end_date":"2017-01-03"
# }

# http://127.0.0.1:5000/getcity_storetypedata
@app.route('/getcity_storetypedata', methods=['POST'])
def getcitydata_storetype_records():
    parser = reqparse.RequestParser()
    parser.add_argument('city_id', required=True)
    parser.add_argument('start_date', required=True)
    parser.add_argument('end_date', required=True)
    args = parser.parse_args()

    #read cities data
    data = pd.read_csv('store_cities.csv')        
    data = data [(data ["city_id"] == args['city_id'])]
    data = data.to_dict('records')
    store_ids=[]

    for x in data:
        store_ids.append(x['store_id'])

    #read sales data
    salesData = pd.read_csv('sales.csv')
    
    # date filter
    date_filter=salesData['date'].between(args['start_date'],args['end_date'])
    salesData=salesData[date_filter]
    
    #store filter
    store_filter=salesData.store_id.isin(store_ids)
    salesData=salesData[store_filter]

    #sum of revenu and sales
    total_revenue=salesData['revenue'].sum()
    total_sales=salesData['sales'].sum()

    #output
    salesData = salesData.to_dict('records')

    return jsonify({
            'code': 200,
            'total_revenue':total_revenue,
            'total_sales':total_sales,
          })

# http://127.0.0.1:5000/get_holidaysales
@app.route('/get_holidaysales', methods=['GET'])
def getholidays_records():
    holiday_dates=[]
    for date in holidays.Sweden(years=2018).items():
        holiday_dates.append(str(date[0]))

     #read sales data
    salesData = pd.read_csv('sales.csv')
    
    #store filter
    store_filter=salesData.date.isin(holiday_dates)
    salesData=salesData[store_filter]

    #sum of revenu and sales
    total_revenue=salesData['revenue'].sum()
    total_sales=salesData['sales'].sum()

    return jsonify({
        'total_revenue':total_revenue,
        'total_sales':total_sales,
    })

if __name__ == '__main__':
    app.run()
