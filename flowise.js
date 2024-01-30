async function query(data) {
  const response = await fetch(
    "http://localhost:3000/api/v1/vector/upsert/6a00454e-18df-4dc1-88f4-20b57c2f2ba4",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    }
  );
  const result = await response.json();
  return result;
}

query({
  "overrideConfig": {
    "openAIApiKey": "example",
    "stripNewLines": true,
    "batchSize": 1,
    "timeout": 1,
  }
}).then((response) => {
  console.log(response);
});
