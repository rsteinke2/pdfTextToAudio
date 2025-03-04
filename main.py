import os
import PyPDF2
from google.cloud import texttospeech

def extract_text_from_pdf(pdf_path):

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def text_to_speech(text, output_file):

    try:
        # Initialize the Text-to-Speech client
        client = texttospeech.TextToSpeechClient()

        # Configure the request
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",  # Adjust language code as needed
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config
        )

        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to '{output_file}'")

    except Exception as e:
        print(f"Error generating audio: {e}")

if __name__ == "__main__":

    pdf_path = "AI.pdf"
    output_audio_file = "output.mp3"

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = MY_JSON_CREDENTIALS

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    if pdf_text:
        print("Text extracted successfully. Converting to speech...")
        text_to_speech(pdf_text, output_audio_file)
    else:
        print("Failed to extract text from the PDF.")