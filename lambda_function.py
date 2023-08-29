import psycopg2
import json
from psycopg2.extras import RealDictCursor
import os

#POST

os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'

host = 'testdb.ciecm0r8o60g.us-east-2.rds.amazonaws.com'
username = 'postgres1'
password = 'AUGHftp021243'
database = 'postgres'

conn = psycopg2.connect(host=host, user=username, password=password, database=database)

def lambda_handler(event, context):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    
    body = json.loads(event['body'])
    id = body['id']
    email = body['email']

    
    cur.execute("UPDATE invitations SET email = %s WHERE id = %s", (email, id))
    conn.commit()  

    
    cur.execute("SELECT * FROM invitations")
    results = cur.fetchall()
    print(results)

    names_as_dict = []  
    for row in results:
        names_as_dict.append({
            'id': row['id'],
            'email': row['email'],
            'subject': row['subject'],
            'body': row['body']
        })
    print(names_as_dict)

    return { 
        "statusCode": 200,
        "body": json.dumps(names_as_dict),
        "headers": {
            "Content-Type": "application/json"
        }
    }

# Test (id must match an existing id in the database)
event = {
    'body': json.dumps({
        'id': 4,
        'email': 'new.email@example.com'
    })
}
context = {}

lambda_handler(event, context)