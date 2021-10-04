from ElasticSearch import connect_elastic , semantic_search , match_phrase_keyword_search , match_keyword_search
from flask import render_template , request
from sentence_transformers import SentenceTransformer
from timeit import default_timer as timer
# from flask_restful import abort
from App import app
@app.route('/' , methods = ['GET'] )
def index():
    return render_template("index.html")

# Connect to elasticsearch
es = connect_elastic(
    "https://vpc-video-search-engine-staging-agjuxhekih6c4kncpl5m2ffg3y.ap-southeast-1.es.amazonaws.com/", 
    "root", "4E2^4CXb")
#load the model
model = SentenceTransformer('/home/mohie_eldin@ad.ogoul.com/paraphrase-multilingual-mpnet-base-v2')
        
@app.route("/search", methods=["POST"])
def get_query() :
    print("entered the function")
    if request.method == 'POST':
        print("entered the post method")
        query = request.form.get("query")
        print(query)
        index_name = request.form.get("language")
        print(index_name)
        #search_type = request.form.get("type")
        #print(search_type)
        search_type = "semantic_search"
        if search_type == "semantic_search" :
            start = timer()
            query_vec = model.encode(query)
            end = timer()
            print("embedding_time: ",  end - start)
             
            start = timer()
            res = semantic_search(es , query_vec , index_name = index_name , top_n = 5)
            end = timer()
            print("search_time: ", end - start)
             
        elif search_type == "exact_search" :
            res = match_phrase_keyword_search(es , query , index_name = index_name , top_n = 5)
        elif  search_type == "semi_exact_search":
            res = match_keyword_search(es , query , index_name = index_name , top_n = 5)
             
      
     #print("res: " , res)
     #data = json.loads(res)
     #print("type data" , type(data))
     #print("\n data : " ,data)
     #print("\n final_res : " , final_res['data'])

    
     #print(make_response(jsonify(final_res)))
    return  render_template( "index.html" ,  data = res  )

     


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])

