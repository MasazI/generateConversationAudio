# Generate Conversation Audio
This repository is a code for genrerating conversation audio file using Amaozon Poly.

### Prerequieties
- Python 3.XX
- boto3 SDK
- ffmpeg

Before executing, AWS Credentials are needed to set in your environment variables.

### Ready transcript file
```
cp conversation-sample.csv conversation.csv
```

### Generate Audio File
```
python generateScriptCsv.py

```