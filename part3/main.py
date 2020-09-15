import MySQLdb
from flask import Flask, render_template, request, redirect, jsonify
from flask_bootstrap import Bootstrap
from AppDB import AppDB
import pandas as pd
import numpy as np

# Create Database Instance 
appDB = AppDB()

# Create flask instance w/ bootstrap 
app = Flask(__name__)
Bootstrap(app)

# Home page 
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Select database table to view 
@app.route('/dataview') 
def dataView():
    return render_template('view_table.html')

# Pivot builder
@app.route('/pivotbuilder')
def pivotBuilder():
    return render_template('pivot.html', iserror=False)

# JQuery fetch attributes for table
@app.route('/fetchattributes')
def fetchAttributes():
    # Get & validate supplied arg
    table = request.args.get('table', None, type=str)
    if (table is None):
        return jsonify(error=True)
   
    # Fetch attributes
    query = "SELECT * FROM " + table + " LIMIT 1"
    cursor = appDB.dbFetchCursor(query)
    table_attributes=[]
    for x in cursor.description:
        table_attributes.append(x[0])
    
    # Return as JSON
    return jsonify(error=False, attributes=table_attributes)

# Helper func to get numeric representation 
def parseFilterVal( strVal ):
    try:
        return int(strVal)
    except ValueError:
        try:
            return float(strVal)
        except ValueError:
            return strVal

# Get CSS class for table data
def getDataClass( minVal, maxVal, dataVal ):
    # Percentage between min/max
    valPercent = (dataVal - minVal) / (maxVal - minVal)

    # Choose one of 12 distinct colors 
    if ( valPercent < 0.08333 ):
        return "table-min"
    elif ( valPercent < 0.16666 ):
        return "table-10"
    elif ( valPercent < 0.24999 ):
        return "table-20"
    elif ( valPercent < 0.33332 ):
        return "table-30"
    elif ( valPercent < 0.41665 ):
        return "table-40"
    elif ( valPercent < 0.49998 ):
        return "table-50"
    elif ( valPercent < 0.58331 ):
        return "table-60"
    elif ( valPercent < 0.66664 ):
        return "table-70"
    elif ( valPercent < 0.74997 ):
        return "table-80"
    elif ( valPercent < 0.8333 ):
        return "table-90"
    elif ( valPercent < 0.91663 ):
        return "table-100"
    else:
        return "table-max"

# Create pivot handler 
@app.route('/createpivot', methods=['POST', 'GET'])
def createPivot(): 
    if (request.method == 'POST'):
        # Fetch POST data
        post_table          = request.form['selectTable']
        post_col_attribute  = request.form['col_attribute']
        post_row_attribute  = request.form['row_attribute']  
        post_aggr_attribute = request.form['aggr_attribute']
        post_aggr_type      = request.form['aggr_type']
        post_filter_attr    = request.form['filter_attribute'] 
        post_filter_func    = request.form['filter_type']
        post_filter_val     = request.form['filterval']

        # Check for filter checkbox (not in form unless checked)
        post_filter_enabled = False 
        try:
            post_filter_enabled = request.form['filteron']
        except:
            pass

        # Validate details
        if (post_table is None):            
            return render_template('pivot.html', iserror=True, error='Invalid data table supplied. Please try again.')
        
        if (post_col_attribute=='0' or post_row_attribute=='0' or post_aggr_attribute=='0'):
            return render_template('pivot.html', iserror=True, error='Invalid attributes supplied. Please try again.')

        if (post_col_attribute==post_row_attribute or post_col_attribute==post_aggr_attribute or post_row_attribute==post_aggr_attribute):
            return render_template('pivot.html', iserror=True, error='Invalid attributes supplied - Attributes must be unique.')

        # Get aggregate function
        npAggrFunc = None 
        if (post_aggr_type == 'sum'):
            npAggrFunc = np.sum
        elif (post_aggr_type == 'avg'):
            npAggrFunc = np.mean
        elif (post_aggr_type == 'count'):
            npAggrFunc = pd.Series.count
        elif (post_aggr_type == 'unique_count'):
            npAggrFunc = pd.Series.nunique
        elif (post_aggr_type == 'min'):
            npAggrFunc = min
        elif (post_aggr_type == 'max'):
            npAggrFunc = max
        else:
            return render_template('pivot.html', iserror=True, error='Invalid aggregate function supplied. Please try again.')

        # Get data for pivot table in DataFrame format 
        data = appDB.dbPandasFetch( 'SELECT * FROM ' + post_table + " LIMIT 2000")

        # Apply filter if selected
        if (post_filter_enabled):
            print "Filtering by attribute " + post_filter_attr + " " + post_filter_func + " " + post_filter_val
            post_filter_val = parseFilterVal(post_filter_val)

            if (post_filter_func == 'equal'):
                data = data[ data[post_filter_attr] == post_filter_val ]
            elif (post_filter_func == 'notEqual'):
                data = data[ data[post_filter_attr] != post_filter_val ]
            elif (post_filter_func == 'less'):
                data = data[ data[post_filter_attr] < post_filter_val ]
            elif (post_filter_func == 'more'):
                data = data[ data[post_filter_attr] > post_filter_val ]
            elif (post_filter_func == 'lessEqual'):
                data = data[ data[post_filter_attr] <= post_filter_val ]
            elif (post_filter_func == 'moreEqual'):
                data = data[ data[post_filter_attr] >= post_filter_val ]


        # Create pivot table 
        pivotData = pd.pivot_table(data, index=post_row_attribute, columns=post_col_attribute, values=post_aggr_attribute, 
            aggfunc=npAggrFunc)

        # Get min/max values
        pivotMin = min(pivotData.min(axis=1))
        pivotMax = max(pivotData.max(axis=1))


        ####### Convert to html

        # Table start + Column headers
        pivotHTML = "<table border='0' class='dataframe table'><thead><tr style='text-align: right;'><th>"+post_col_attribute+"</th>"
        for colHeader in pivotData.columns.values:
            pivotHTML += "<th>"+colHeader+"</th>"

        # Row attribute header 
        pivotHTML += "</tr><tr><th>"+post_row_attribute+"</th>"
        for colHeader in pivotData.columns.values:
            pivotHTML += "<th></th>"
        pivotHTML += "</tr></thead><tbody>"

        # Data set + row headers 
        for row in pivotData.itertuples():
            pivotHTML += "<tr>"
            index = 0
            for data in row:
                if index == 0:
                    pivotHTML += "<th>"+data+"</th>"
                else:
                    if pd.isnull( data ):
                        pivotHTML += "<td>.</td>"
                    else:
                        pivotHTML += "<td class='" + getDataClass(float(pivotMin), float(pivotMax), float(data))+ "' >"+str(data)+"</td>"

                index += 1
            pivotHTML += "</tr>"

        pivotHTML += "</tbody></table>"

        #htmlTable = pivotData.to_html(classes='table', border=0, na_rep='.')

        # Render pivot table
        return render_template('pivotresult.html', table=post_table, col_attribute=post_col_attribute, row_attribute=post_row_attribute, 
            aggr_func=post_aggr_type, aggr_attribute=post_aggr_attribute, pivot_table_html=pivotHTML, fill_value=0, table_min=pivotMin, 
            table_max=pivotMax, filter=) 
    else:
        # Not a POST, redirect to pivot builder
        return pivotBuilder()


# Observations page 
@app.route('/observations')
def observations():
    return render_template('observations.html')

# 'About the data' link
@app.route('/aboutdata')
def aboutData():
    return render_template('aboutdata.html')

# 'About us' link
@app.route('/aboutus')
def aboutUs():
    return render_template('aboutus.html')

# Posted database viewer
@app.route('/view_table',methods = ['POST', 'GET'])
def view_table():
    if request.method == 'POST':
        # Fetch post data
        table_name      = request.form['table_name']
        results_count   = request.form['results_count']
        page_no         = request.form['page_no']

        # Create Query & fetch data from db
        query = "SELECT * FROM "+ table_name+" LIMIT "+str(results_count)+" OFFSET "+str( int(page_no)*int(results_count) )
        cursor = appDB.dbFetchCursor(query)
        table_head=[]
        for x in cursor.description:
            table_head.append(x[0])
        table_content = cursor.fetchall()

        return render_template("result.html",table_head=table_head, table_content=table_content, page_title=table_name, page=page_no, 
            page_next=int(page_no)+1, page_prev=str(int(page_no)-1 if (int(page_no) > 0) else 0), results_count=results_count )
    else:
        # Not a POST, redirect to view select
        return dataView()


if __name__ == '__main__':
   app.run(debug = True)