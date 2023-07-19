from flask import Flask,render_template,request,redirect
from pymongo import MongoClient
client=MongoClient('localhost',27017)

db=client['hackathon']      #we have to pass database name here    'skill' is a key of dictionary 

coll=db['recipe']    #we have to select the collection name from the list of collections of database


app=Flask(__name__)
  
@app.route('/',methods=['get'])
def homepage():
    k=coll.find()
    data=[]
    for i in k:
        data.append(i)
    l=len(data)
    z=[]
    for i in range(l):
        z.append(data[i])
    return render_template('index.html',res=z)

@app.route('/admin')
def adminpage():
    return render_template('admin.html')

@app.route('/login',methods=['post','get'])
def login():
    k=coll.find()
    data=[]
    for i in k:
        data.append(i)
    l=len(data)
    z=[]
    for i in range(l):
        z.append(data[i])
    name=request.form['name']
    password=request.form['pass']
    if name=='jagadeesh' and password=='hack':
        return render_template('content.html',res=z,n='List :')
    else:
        return render_template('admin.html',m='invalid credentials')

@app.route('/add',methods=['post'])
def addpage():
    return render_template('add.html')

@app.route('/delete',methods=['post'])
def deletepage():
    return render_template('delete.html')

@app.route('/update',methods=['post'])
def updatepage():
    return render_template('update.html')

@app.route('/content')
def content():
    k1=coll.find()
    data1=[]
    for j in k1:
        data1.append(j)
    g=len(data1)
    z1=[]
    for i in range(g):
        z1.append(data1[i])
    return render_template('content.html',res=z1,n='List :')

@app.route('/adddata',methods=['post'])
def mongodisplay():
    name=request.form['name']
    item=request.form['ingredient']
    proc=request.form['process']
    k={}
    k['name']=name
    k['ingredients']=item
    k['process']=proc
    coll.insert_one(k)
    k1=coll.find()
    data=[]
    for i in k1:
        data.append(i)
    l=len(data)
    z=[]
    for i in range(l):
        z.append(data[i])
    return render_template('content.html',res=z,n="List :")

@app.route('/updatedata',methods=['post','get'])
def mongoupdate():
    name=request.form['name']
    item=request.form['ingredient']
    proc=request.form['process']
    kl=coll.find()
    data=[]
    for i in kl:
        data.append(i)
    l=len(data)
    for i in range(l):
        z=data[i]
        if z['name']==name :
            try:
                coll.find_one_and_update(
                {"name":name},
                {"$set":
                    {"ingredients": item,"process":proc}
                }
                )
                k1=coll.find()
                data1=[]
                for j in k1:
                    data1.append(j)
                g=len(data1)
                z1=[]
                for i in range(g):
                    z1.append(data1[i])
                return render_template('content.html',res=z1,n='List :')
            except:
                return render_template('update.html',m='no record found..')
    else:
        return render_template('update.html',m='no record found..')

    
    #             z['name']=name
    #             z['ingredients']=item
    #             z['process']=proc
    #         except:
    #             return "error"
    # else:
    #     k={}
    #     k['name']=name
    #     k['ingredients']=item
    #     k['process']=proc
    #     coll.insert_one(k)
@app.route('/getdata',methods=['get','post'])
def mongoData():
    choice=request.form['get-recipe']
    # search=request.form['search']
    k=coll.find()
    data=[]
    for i in k:
        data.append(i)
    l=len(data)
    z1=[]
    for i in range(l):
        z1.append(data[i])
    for i in range(l):
        z=data[i]
        if z['name']==choice :
            return render_template('index2.html',res=z1,m=z['name'],n=z['ingredients'],p=z['process'])
    else:
        return render_template('index.html',m='search not found')

@app.route('/search',methods=['get','post'])
def mongoSearch():
    # choice=request.form['get-recipe']
    search=request.form['search']
    if search=='none':
        return redirect('/')
    k=coll.find()
    data=[]
    for i in k:
        data.append(i)
    l=len(data)
    z1=[]
    for i in range(l):
        z1.append(data[i])
    for i in range(l):
        z=data[i]
        if z['name']==search:
            return render_template('index2.html',res=z1,m=z['name'],n=z['ingredients'],p=z['process'])

@app.route('/searchadmin',methods=['get','post'])
def mongoadminSearch():
    # choice=request.form['get-recipe']
    search=request.form['search']
    print(search)
    if 'none'==search:
        return redirect('/content')
    k=coll.find()

    data=[]
    for i in k:
        data.append(i)
    l=len(data)
    z1=[]
    for i in range(l):
        z1.append(data[i])
    for i in range(l):
        z=data[i]
        if search==z['name']:
             return render_template('admin-recipe.html',res=z1,m=z['name'],n=z['ingredients'],p=z['process'])
    else:
        return redirect('/content')

    


@app.route('/deletedata',methods=['get','post'])
def deleteData():
    choice=request.form['name']
    # search=request.form['search']
    k=coll.find()
    data=[]
    for i in k:
        data.append(i)
    l=len(data)
    for i in range(l):
        z=data[i]
        if z['name']==choice :
            coll.delete_one({'name':choice})
            k1=coll.find()
            data1=[]
            for j in k1:
                data1.append(j)
            g=len(data1)
            z1=[]
            for d in range(g):
                z1.append(data1[d])
            return render_template('content.html',res=z1,n='List :')
    else:
        return render_template('delete.html',m="No such item is there in the List..Please try with exact recipe.")

if __name__ == '__main__':
    app.run(debug=True)