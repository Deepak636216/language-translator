
import numpy as np

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from transformers import pipeline, Speech2TextProcessor, Speech2TextForConditionalGeneration
from fastapi.middleware.cors import CORSMiddleware
import torch
from io import BytesIO

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


s2t_model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")
s2t_processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

model_name = "SnypzZz/Llama2-13b-Language-translate"
translate_pipe = pipeline("text2text-generation", model=model_name)

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.post("/translate/")
async def translate(request: TranslationRequest):
    translated_text = translate_pipe(f"{request.text} to {request.target_language}")[0]['generated_text']
    return {"translated_text": translated_text}

@app.post("/transcribe_and_translate/")
async def transcribe_and_translate(file: UploadFile = File(...), target_language: str = 'es'):
    audio_bytes = await file.read()
    audio_file = BytesIO(audio_bytes)
    
    audio = torch.from_numpy(np.array(bytearray(audio_bytes))).float().unsqueeze(0)  
    inputs = s2t_processor(audio, sampling_rate=16000, return_tensors="pt")  
    generated_ids = s2t_model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])
    
    transcription = s2t_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    translated_text = translate_pipe(f"{transcription} to {target_language}")[0]['generated_text']

    return {"transcription": transcription, "translated_text": translated_text}

