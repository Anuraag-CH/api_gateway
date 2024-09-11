from fastapi import FastAPI, Request, HTTPException, Depends
from functions.dynamic_routing import route_request
from functions.authentication import verify_token
from functions.whitelist import is_whitelisted

app = FastAPI()

# Define the API gateway endpoint with authentication
@app.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(
    service_name: str,
    path: str,
    request: Request,
):
    token = request.headers.get("Authorization")
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not is_whitelisted(service_name, request.method):
        raise HTTPException(status_code=403, detail="Method not allowed for this service")
    
    return await route_request(service_name, path, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
