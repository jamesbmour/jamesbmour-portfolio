import requests

API_URL = "http://localhost:3000/api/v1/vector/upsert/6a00454e-18df-4dc1-88f4-20b57c2f2ba4"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

output = query({
    "overrideConfig": {
        "openAIApiKey": "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",
        "stripNewLines": True,
        "batchSize": 1,
        "timeout": 1,
    }
})
