from elasticsearch import Elasticsearch
import json

def connect_elastic(HOST, user, password):
    es = Elasticsearch(hosts=HOST, http_auth=(user, password), timeout=30)
    if es.ping():
        print("Connected to elasticsearch...")
    else:
        print("Elasticsearch connection error...")
    return es

        
def semantic_search( es , query_vector ,index_name,  top_n = 5 ) :
    # Retrieve top_n semantically similar records for the given query vector
   
   
    search_body = {
  "size": top_n,
  "query": {
    "knn": {
      "sentence_vector": {
        "vector": query_vector,
        "k": top_n 
      }
    }
  }
}
                          
    
    # Semantic vector search with cosine similarity
    result = es.search(index=index_name, body=search_body)
    total_match = len(result["hits"]["hits"])
    data = []
    if total_match > 0:
        #print("Query: ",queries[counter])
        #i = 1
        for hit in result["hits"]["hits"]:
            #print("--\nscore: {} \n {}) sentence: {} \n--".format(hit["_score"], i , hit["_source"]['sentence']))
            data.append({'score' : hit["_score"]})
            #i = i+1
    else :
        print("No Results")
    return data



def match_phrase_keyword_search(es , query,  index_name , top_n=10  ):
    # Retrieve top_n records using TF-IDF scoring for the given query vector
    k_body = {
        "size" : top_n,
        "query": {
            "match_phrase": {
                "sentence": query
            }
        }
    }

    # Keyword search
    result = es.search(index=index_name, body=k_body)
    total_match = len(result["hits"]["hits"])
    data = []
    if total_match > 0:
        for hit in result["hits"]["hits"]:
                #print("--\nscore: {} \n sentence: {} \n--".format(hit["_score"], hit["_source"]['sentence']))
                data.append({'video_id': hit["_source"]['video_id'] , 'start_time':hit["_source"]['start_time']})
    else :
        return False
    #return json.dumps({"data": data})
    return data





def match_keyword_search(es , query,  index_name , top_n=10  ):
    # Retrieve top_n records using TF-IDF scoring for the given query vector
    k_body = {
        "size" : top_n,
        "query": {
            "match": {
                "sentence": query
            }
        }
    }

    # Keyword search
    result = es.search(index=index_name, body=k_body)
    total_match = len(result["hits"]["hits"])
    data = []
    if total_match > 0:
        for hit in result["hits"]["hits"]:
                #print("--\nscore: {} \n sentence: {} \n--".format(hit["_score"], hit["_source"]['sentence']))
                data.append({'video_id': hit["_source"]['video_id'] , 'start_time':hit["_source"]['start_time']})
    else :
       return False
    #return json.dumps({"data": data})
    return data

