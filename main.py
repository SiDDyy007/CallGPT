from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from agents.store_agent import process_voice_entry
from utils.twilio_utils import twiml_response

app = FastAPI()

@app.post("/twilio/voice")
async def handle_call(request: Request):
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    caller = form.get("From")
    if not recording_url:
        return PlainTextResponse("No recording found", status_code=400)

    await process_voice_entry(recording_url, caller)
    return twiml_response("Thanks for your journal entry. It's saved!")


@app.post("/twilio/retrieve")
async def handle_query(request: Request):
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    caller = form.get("From")
    if not recording_url:
        return PlainTextResponse("No query recording found", status_code=400)

    from agents.retrieve_agent import process_query
    result_text = await process_query(recording_url, caller)
    return twiml_response(result_text)
