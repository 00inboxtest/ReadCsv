from flask import Flask, jsonify
from flask_restful import reqparse
import pandas as pd

app = Flask(__name__)

@app.route('/getproduct', methods=['GET'])
def getproduct_records():
    data = pd.read_csv('product_hierarchy.csv')
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

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
    sum_revenue=salesData['revenue'].sum()
    sum_sales=salesData['sales'].sum()

    #output
    salesData = salesData.to_dict('records')

    return jsonify({
            'total_revenue':sum_revenue,
            'total_sales':sum_sales,
          })


@app.route('/getsaledata', methods=['GET'])
def getsaledata_records():
    
    #read sales data
    data = pd.read_csv('sales.csv')
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

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

    dimensions=0
    for x in data:
        dimensions=x['product_length']*x['product_width']*x['product_depth']

    #read sales data
    salesData = pd.read_csv('sales.csv')
    
    # date filter
    date_filter=salesData['date'].between(args['start_date'],args['end_date'])
    salesData=salesData[date_filter]
    
    #product filter
    product_filter=(salesData["product_id"] == args['product_id'])
    salesData=salesData[product_filter]

    # sum of total sales
    sum_sales=salesData['sales'].sum()

    # calculate total volume
    total_volume=dimensions*sum_sales
    
    #output
    salesData = salesData.to_dict('records')

    return jsonify({
            'total_volume':total_volume,
            'total_sales':sum_sales,
            'total_dimensions':dimensions,
          })


@app.route('/getcitydata', methods=['GET'])
def getcitydata_records():
    #read cities data
    data = pd.read_csv('store_cities.csv')
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

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
    sum_revenue=salesData['revenue'].sum()
    sum_sales=salesData['sales'].sum()
    
    # a_series = (salesData['sales'] != 0)
    # new_df = salesData['sales'].loc[a_series]

    #output
    salesData = salesData.to_dict('records')

    return jsonify({
            'code': 200,
            'total_revenue':sum_revenue,
            'total_sales':sum_sales,
          })

if __name__ == '__main__':
    app.run()
