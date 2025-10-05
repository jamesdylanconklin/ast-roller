import json
import logging

# Local imports
from grammar import parser, transformer


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler function - Dice rolling service
    
    Args:
        event: API Gateway event with body containing:
               - event['body']['roll_string']: Dice expression (e.g., "6 2d6+6")  
               - event['body']['options']: Roll configuration options, not supported yet
        context: Lambda runtime context
        
    Returns:
        dict: HTTP response with dice roll results
    """
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event)}")

        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']

        roll_string = body.get('roll_string', '') or '1d20'
        parsed_tree = parser.parse(roll_string)
        transformed = transformer.transform(parsed_tree)
        roll_result = transformed.evaluate()
        
        # Echo back the event data
        response_body = {
            "roll_result": roll_result.raw_result
        }
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_body)
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        
        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


# For local testing
if __name__ == "__main__":
    # Sample test event
    test_event = {
        "name": "test",
        "message": "Hello from local test!"
    }
    
    # Mock context object for local testing
    class MockContext:
        function_name = "echo-lambda-local"
        aws_request_id = "test-request-123"
    
    result = lambda_handler(test_event, MockContext())
    print(json.dumps(result, indent=2))