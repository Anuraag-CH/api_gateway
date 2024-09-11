from fastapi import Request, Response
import httpx

# Define backend services and their URLs
BACKEND_SERVICES = {
    'service1': 'http://localhost:5001',
    'service2': 'http://localhost:5002',
}

async def route_request(service_name: str, path: str, request: Request) -> Response:
    # Check if the service is registered
    if service_name not in BACKEND_SERVICES:
        return None

    backend_url = f"{BACKEND_SERVICES[service_name]}/{path}"

    async with httpx.AsyncClient() as client:
        # Forward the request to the backend service
        response = await client.request(
            method=request.method,
            url=backend_url,
            headers=request.headers,
            content=await request.body(),
            allow_redirects=False
        )

    # Create a new Response object with the data from the backend service
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
