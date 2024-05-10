import pymongo

client = pymongo.MongoClient("MANGO_DBB")
db = client.sample_mflix
collection = db.movies

hf_token = "HUG_AP"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-model"

# def generate_embedding(text: str) -> list[float]:  #### we don't need to generate the embdding again 
  
#   response = requests.post(
#     embedding_url,
#     header={"Authorization": f"Bearer {hf_token}"},
#     json={"input", text})

#   if response.status_code != 200:
#     raise ValueError(f"Request failed with status code {response.staus_code}: {response.text}")
  
#   return response.json()

# for doc in collection({'plot':{"$exists": True}}).limit(50):
#  doc['plot_embdding_hf'] = generate_embedding(doc['plot'])
#  collection.replace_one({'_id': doc['_id']}, doc)

query = 'imaginary characters from outer space at war'

results = collection.aggregate([
  {"$vectorsearch": {
   "queryVector": generate_embedding(query),
   "path": "plot_embedding_hf",
   "numCandiates": 100,
   "limit": 4,
   "index": "PlotSemanticSearch",
  }}

]);

for document in results:
    print(F'Movie Name: {document["title"]},\nMovie Plot:{document['Plot']}\n')
