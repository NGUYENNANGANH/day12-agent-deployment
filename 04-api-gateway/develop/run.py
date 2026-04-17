import os
import uvicorn
os.environ['AGENT_API_KEY'] = 'my-secret-key'
uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=False)