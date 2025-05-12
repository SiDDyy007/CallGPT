from fastapi.responses import Response

def twiml_response(message: str) -> Response:
    response = f"""
    <Response>
        <Say>{message}</Say>
    </Response>
    """
    return Response(content=response.strip(), media_type="application/xml")
