import json
import base64
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the cart abandonment threshold in minutes
CART_ABANDONMENT_THRESHOLD_MINUTES = 30

def lambda_handler(event, context):
    """
    Lambda function to process cart events and determine if carts are abandoned.

    Args:
        event (dict): The Lambda event object containing Kinesis records.
        context (LambdaContext): The Lambda execution context.

    Returns:
        dict: The result containing processed records.
    """

    logger.info(
        f"Events Transform Handler Invoked with Records {event['records'][:3]}")

    output = []
    for record in event['records']:
        try:
            payload = decode_record(record['data'])

        except Exception as e:
            logger.error({
                'error': 'failed-decoding-record',
                'exception': str(e),
                'record': record
            })
            raise e

        logger.info({
            'message': 'Processed event record',
            'event': payload
        })

        # Calculate the time elapsed since the event_time
        event_time = datetime.fromtimestamp(payload['event_time'] / 1000)
        current_time = datetime.now()
        time_elapsed_minutes = (current_time - event_time).total_seconds() / 60

        # Check if the cart is abandoned based on the threshold
        if time_elapsed_minutes >= CART_ABANDONMENT_THRESHOLD_MINUTES:
            payload['cart_abandoned'] = True

            cart_items = payload.pop('cart_items')
            total = sum([ci['product_quantity']*ci['product_price']
                    for ci in cart_items])
            payload['cart_total'] = total
        else:
            payload['cart_abandoned'] = False

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(payload).encode('utf-8'))
        }

        output.append(output_record)

    logger.info(f'Processed Records {output[:2]}')

    return {'records': output}


def decode_record(record: bytes) -> dict:
    """
    Decode a base64-encoded record and parse it as a JSON object.

    Args:
        record (bytes): The base64-encoded record.

    Returns:
        dict: The decoded JSON object.
    """
    string_data = base64.b64decode(record).decode('utf-8')
    return json.loads(string_data)
