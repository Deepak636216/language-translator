// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [targetLanguage, setTargetLanguage] = useState('');
  const [transcription, setTranscription] = useState('');
  const [translatedText, setTranslatedText] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleTranslate = async () => {
    if (!file) {
      alert('Please upload an audio file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_language', targetLanguage);

    try {
      const response = await axios.post('http://localhost:8000/transcribe_and_translate/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setTranscription(response.data.transcription);
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error('There was an error processing the file!', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Speech-to-Text and Translator</h1>
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
        />
        <input
          type="text"
          value={targetLanguage}
          onChange={(e) => setTargetLanguage(e.target.value)}
          placeholder="Enter target language"
        />
        <button onClick={handleTranslate}>Transcribe and Translate</button>
        <div>
          <h2>Transcription:</h2>
          <p>{transcription}</p>
        </div>
        <div>
          <h2>Translated Text:</h2>
          <p>{translatedText}</p>
        </div>
      </header>
    </div>
  );
}

export default App;
