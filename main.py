from flask import Flask, jsonify
from flask_restful import reqparse
import pandas as pd

app = Flask(__name__)

@app.route('/getproduct', methods=['GET'])
def getproduct_records():
    data = pd.read_csv('product_hierarchy.csv',nrows=10)
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

@app.route('/getproduct_hierarchywise', methods=['POST'])
def getproduct_store_records():
    parser = reqparse.RequestParser()
    parser.add_argument('hierarchy1_id', required=True)
    args = parser.parse_args()
    data = pd.read_csv('product_hierarchy.csv',nrows=20)        
    data = data [(data ["hierarchy1_id"] == args['hierarchy1_id'])]
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})


@app.route('/getsaledata', methods=['GET'])
def getsaledata_records():
    data = pd.read_csv('sales.csv',nrows=10)
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

@app.route('/getsale_productdata', methods=['POST'])
def getsaledata_product_records():
    parser = reqparse.RequestParser()
    parser.add_argument('product_id', required=True)
    args = parser.parse_args()
    data = pd.read_csv('sales.csv',nrows=20)        
    data = data [(data ["product_id"] == args['product_id'])]
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

@app.route('/getcitydata', methods=['GET'])
def getcitydata_records():
    data = pd.read_csv('store_cities.csv',nrows=10)
    data = data.to_dict('records')
    return jsonify({'data' :data,'code':200})

@app.route('/getcity_storetypedata', methods=['POST'])
def getcitydata_storetype_records():
    parser = reqparse.RequestParser()
    parser.add_argument('city_id', required=True)
    parser.add_argument('start_date', required=True)
    parser.add_argument('end_date', required=True)
    args = parser.parse_args()

    data = pd.read_csv('store_cities.csv')        
    data = data [(data ["city_id"] == args['city_id'])]
    data = data.to_dict('records')
    store_ids=[]

    for x in data:
        store_ids.append(x['store_id'])
    print(store_ids)

    salesData = pd.read_csv('sales.csv',nrows=1200)
    
    # date filter
    date_filter=salesData['date'].between(args['start_date'],args['end_date'])
    salesData=salesData[date_filter]
    
    #store filter
    store_filter=salesData.store_id.isin(store_ids)
    salesData=salesData[store_filter]
    
    salesData = salesData.to_dict('records')

    print('salesDataAFTER',date_filter)

    return jsonify({
            'code': 200,
            'store_ids': store_ids,
            'xsalesData': salesData
          })

if __name__ == '__main__':
    app.run()
