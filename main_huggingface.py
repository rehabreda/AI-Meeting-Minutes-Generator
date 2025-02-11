import gradio as gr
import pyaudio
import wave
import threading
import time
from datetime import datetime
from pathlib import Path
import numpy as np
import logging
from openai import OpenAI
import os
from audio_module import speech_to_text
from llm_module import generate_meeting_minutes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MeetingRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.output_dir = Path("recordings")
        self.output_dir.mkdir(exist_ok=True)
        self.current_audio_file = None
        
        
        # Audio settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        
    def start_recording(self):
        """Start audio recording"""
        if not self.is_recording:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.is_recording = True
            self.frames = []
            
            # Start recording thread
            self.record_thread = threading.Thread(target=self._record)
            self.record_thread.start()
            
            return "Recording in progress...", gr.update(variant="stop", value="Stop Recording")
            
        return "Already recording!", gr.update()
    
    def _record(self):
        """Record audio data"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            except Exception as e:
                logger.error(f"Error during recording: {str(e)}")
                self.stop_recording()
                break
    
    def stop_recording(self):
        """Stop recording and save the file"""
        if self.is_recording:
            self.is_recording = False
            
            if hasattr(self, 'stream'):
                self.stream.stop_stream()
                self.stream.close()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.output_dir / f"meeting_{timestamp}.wav"
            
            with wave.open(str(filename), 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            
            self.current_audio_file = filename
            logger.info(f"Recording saved to {filename}")
            
            return (
                f"Recording saved as {filename.name}",
                gr.update(variant="primary", value="Start Recording"),
                str(filename)
            )
            
        return "No recording in progress!", gr.update(), None
    
    def generate_minutes(self, audio_file):
        """Generate meeting minutes from audio file"""
        try:
            if audio_file is None:
                return "Please record or upload an audio file first."
            
            # First, transcribe the audio
            
            transcript =speech_to_text(audio_file)
           
            
            # Then, generate minutes using GPT-4
            minutes=generate_meeting_minutes(transcription=transcript)
           
            
            # Save minutes to file
            minutes_file = Path(audio_file).with_suffix('.txt')
            minutes_file.write_text(minutes)
            
            return minutes     
        except Exception as e:
            logger.error(f"Error generating minutes: {str(e)}")
            return f"Error generating minutes: {str(e)}"

def create_interface():
    recorder = MeetingRecorder()
    
    with gr.Blocks(title="Meeting Recorder & Minutes Generator") as interface:
        gr.Markdown("# Meeting Recorder & Minutes Generator")
        
        with gr.Row():
            status = gr.Textbox(
                label="Status",
                value="Ready to record",
                interactive=False
            )
            
        with gr.Row():
            record_button = gr.Button(
                "Start Recording",
                variant="primary"
            )
            
        with gr.Row():
            audio_output = gr.Audio(
                label="Recorded Audio",
                type="filepath"
            )
            
        with gr.Row():
            generate_button = gr.Button(
                "Generate Meeting Minutes",
                variant="secondary"
            )
            
        with gr.Row():
            minutes_output = gr.Markdown(
                label="Meeting Minutes"
                # placeholder="Minutes will appear here...",
                # lines=10
            )
            
        def toggle_recording():
            if record_button.value == "Start Recording":
                status_text, button_update = recorder.start_recording()
                return status_text, button_update, None
            else:
                status_text, button_update, audio_file = recorder.stop_recording()
                return status_text, button_update, audio_file
        
        record_button.click(
            fn=toggle_recording,
            outputs=[status, record_button, audio_output]
        )
        
        generate_button.click(
            fn=recorder.generate_minutes,
            inputs=[audio_output],
            outputs=[minutes_output]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True)