import boto3
import os
from contextlib import closing
import csv
from pydub import AudioSegment

# set your credentials in your environment variables.
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
region_name = os.environ.get('AWS_REGION', 'ap-northeast-1') 

def synthesize_speech(text, output_file, voice_id='Tomoko', engine='neural'):
    polly_client = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name).client('polly')

    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine=engine
    )

    with closing(response["AudioStream"]) as stream:
        with open(output_file, "wb") as file:
            file.write(stream.read())

def load_conversation(file_path):
    conversation = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                conversation.append(tuple(row))
    return conversation

# Conversaion file.
conversation_file = 'conversation.csv' 
conversation = load_conversation(conversation_file)

# Tmp audios.
temp_dir = "temp_audio_csv"
os.makedirs(temp_dir, exist_ok=True)

# Combined conversation file.
combined_audio = AudioSegment.empty()

# Genrate and combine.
for i, (speaker, text) in enumerate(conversation):
    voice_id = 'Takumi' if speaker == "医師" else 'Tomoko'
    output_file = os.path.join(temp_dir, f"{speaker}_{i+1}.mp3")
    synthesize_speech(text, output_file, voice_id)
    print(f"Generated: {output_file}")
    
    audio_segment = AudioSegment.from_mp3(output_file)
    combined_audio += audio_segment
    
    # Put an interval.
    combined_audio += AudioSegment.silent(duration=500)

# Output combined file.
combined_output = "combined_conversation_csv.mp3"
combined_audio.export(combined_output, format="mp3")

print(f"Combined audio saved as: {combined_output}")

# Clean up.
for file in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file))
os.rmdir(temp_dir)

print("Temporary files cleaned up. Process finished.")