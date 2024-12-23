from flask import Flask, request, jsonify
import boto3
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

sns_client = boto3.client('sns', region_name=os.getenv('REGION'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

@app.route('/')
def index():
    return 'API Email Sender'

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    url = data['url']
    email_address = data['email_address']

    response = sns_client.publish(
        TopicArn=os.getenv('ARN_SNS'),
        Message=url,
        Subject='Content from S3 Bucket',
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email_address
            }
        }
    )

    return jsonify({'message': 'Email sent', 'response': response}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)