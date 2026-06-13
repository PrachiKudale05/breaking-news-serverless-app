import json
import boto3
import uuid

# AWS services
dynamodb = boto3.resource('dynamodb')
polly = boto3.client('polly')
s3 = boto3.client('s3')

# DynamoDB table
table = dynamodb.Table('BreakingNews')

# S3 bucket
BUCKET_NAME = "news-audio-bucket-prachi"

def lambda_handler(event, context):

    # News in 3 languages
    english_news = [
        "India launches new AI innovation mission.",
        "Heavy rainfall alert issued in Maharashtra.",
        "Indian cricket team wins thrilling match."
    ]

    hindi_news = [
        "भारत ने नई एआई इनोवेशन मिशन की शुरुआत की।",
        "महाराष्ट्र में भारी बारिश की चेतावनी जारी।",
        "भारतीय क्रिकेट टीम ने रोमांचक मैच जीता।"
    ]

    marathi_news = [
        "भारताने नवीन एआय इनोव्हेशन मिशन सुरू केले.",
        "महाराष्ट्रात मुसळधार पावसाचा इशारा जारी.",
        "भारतीय क्रिकेट संघाने रोमांचक सामना जिंकला."
    ]

    # Store news in DynamoDB
    for news in english_news:
        table.put_item(
            Item={
                'news_id': str(uuid.uuid4()),
                'headline': news,
                'language': 'English'
            }
        )

    for news in hindi_news:
        table.put_item(
            Item={
                'news_id': str(uuid.uuid4()),
                'headline': news,
                'language': 'Hindi'
            }
        )

    for news in marathi_news:
        table.put_item(
            Item={
                'news_id': str(uuid.uuid4()),
                'headline': news,
                'language': 'Marathi'
            }
        )

    # Combine text
    english_text = " ".join(english_news)
    hindi_text = " ".join(hindi_news)
    marathi_text = " ".join(marathi_news)

    # Generate English audio
    english_audio = polly.synthesize_speech(
        Text=english_text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    # Generate Hindi audio
    hindi_audio = polly.synthesize_speech(
        Text=hindi_text,
        OutputFormat='mp3',
        VoiceId='Aditi',
        LanguageCode='hi-IN'
    )

    # Generate Marathi audio
    marathi_audio = polly.synthesize_speech(
        Text=marathi_text,
        OutputFormat='mp3',
        VoiceId='Aditi',
        LanguageCode='hi-IN'
    )

    # Upload English audio
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='english/today_news.mp3',
        Body=english_audio['AudioStream'].read(),
        ContentType='audio/mpeg'
    )

    # Upload Hindi audio
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='hindi/today_news.mp3',
        Body=hindi_audio['AudioStream'].read(),
        ContentType='audio/mpeg'
    )

    # Upload Marathi audio
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='marathi/today_news.mp3',
        Body=marathi_audio['AudioStream'].read(),
        ContentType='audio/mpeg'
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'News audio generated successfully',
            'english_audio':
            f'https://{BUCKET_NAME}.s3.amazonaws.com/english/today_news.mp3',

            'hindi_audio':
            f'https://{BUCKET_NAME}.s3.amazonaws.com/hindi/today_news.mp3',

            'marathi_audio':
            f'https://{BUCKET_NAME}.s3.amazonaws.com/marathi/today_news.mp3'
        })
    }