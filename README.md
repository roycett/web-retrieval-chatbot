# SarwarGPT
The name is just my own name and I don't know why I added GPT even though it's not even GPT but let's just get into some details that you need to get this up and running.

## Dependencies
```bash
pip install fastapi langchain langchain-community langchain-groq pydantic
```
## API Keys
You need to obtain API keys for Groq and Brave Search. A simple search will land you them.

## Edit app.py
Edit the following lines of code in app.py and place your API keys appropiately:

```bash
searcher = BraveSearch.from_api_key(api_key='', search_kwargs={"count": 3})
model = ChatGroq(model_name='llama3-70b-8192', api_key='')
```

## Open cmd and deploy
Open cmd in the directory containing app.py and index.html and type:

```bash
fastapi dev app.py
```

It will deploy the app on localhost:8000.


