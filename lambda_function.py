import json
import logging

# Local imports
from grammar import GRAMMAR

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler function - Simple echo service
    
    Args:
        event: The event dict that contains the data sent to the Lambda function
        context: The context object provides information about the runtime environment
        
    Returns:
        dict: Response object with statusCode and body
    """
    
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Echo back the event data
        response_body = {
            "message": "Echo successful",
            "received_data": event,
            "function_name": context.function_name if context else "local-test",
            "request_id": context.aws_request_id if context else "local-request"
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
        # Log the error
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