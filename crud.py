from flask import Flask, request, jsonify
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

sns_client = boto3.client('sns', region_name=os.getenv('REGION'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

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

    return jsonify({'message': 'Email sent', 'response': response})

if __name__ == '__main__':
    app.run(debug=True)