from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.payments.v1.pay_request_builder import PgPayRequest
from phonepe.sdk.pg.env import Env
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from django.conf import settings
import uuid
import json
import base64
import requests
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

Cashfree.XClientId = settings.CF_CLIENT_ID
Cashfree.XClientSecret = settings.CF_CLIENT_SECRET
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"


def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()


def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = json.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')


def init_payment(amount, owner, data):
    id = str(owner.id)
    if owner.id < 10:
        id = f"00{owner.id}"
    elif owner.id < 99:
        id = f"0{owner.id}"

    customerDetails = CustomerDetails(customer_id=id, customer_phone=owner.phone)
    createOrderRequest = CreateOrderRequest(order_amount=amount, order_currency="INR", customer_details=customerDetails,
                                            order_meta=OrderMeta(
                                                notify_url="https://9f89-2401-4900-1ca2-d1e2-353f-436a-c4f2-3970.ngrok-free.app/autofind/payment-callback/"),
                                            order_tags=data)
    try:
        api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
        return dict(api_response.data)
    except Exception as e:
        print(e)


def fetch_order(order_id):
    try:
        api_response = Cashfree().PGFetchOrder(x_api_version=x_api_version,
                                               order_id=order_id)
        print(api_response.data)
        return dict(api_response.data)
    except Exception as e:
        print(e)

# def init_payment(amount, owner, phone):
#     merchant_id = settings.MERCHANT_ID
#     salt_key = settings.SALT_KEY
#     salt_index = str(1)
#     env = Env.UAT
#     ENDPOINT = "/pg/v1/pay"
#     transaction_id = uuid.uuid4()
#     call_back_url = "https://a64f-2401-4900-1ca2-60b1-3493-d3af-5164-b06.ngrok-free.app/autofind/payment-callback/?fullName=Himanshu"
#     # payment_client = PhonePePaymentClient(merchant_id, salt_key, 1)
#
#     MAINPAYLOAD = {
#         "merchantId": merchant_id,
#         "merchantTransactionId": str(transaction_id),
#         "merchantUserId": owner,
#         "amount": int(amount * 100),
#         "redirectUrl": call_back_url,
#         "redirectMode": "POST",
#         "callbackUrl": call_back_url,
#         "mobileNumber": int(phone),
#         "paymentInstrument": {
#             "type": "PAY_PAGE"
#         }
#     }
#
#     base64String = base64_encode(MAINPAYLOAD)
#     mainString = base64String + ENDPOINT + salt_key
#     sha256Val = calculate_sha256_string(mainString)
#     checkSum = sha256Val + '###' + salt_index
#
#     headers = {
#         'Content-Type': 'application/json',
#         'X-VERIFY': checkSum,
#         'accept': 'application/json',
#     }
#
#     return {'body': base64String,
#             'callBackURL': call_back_url,
#             'checksum': checkSum,
#             "headers": headers,
#             "apiEndPoint": ENDPOINT}

# unique_transaction_id = str(uuid.uuid4())[:-2]
# s2s_callback_url = "https://www.merchant.com/callback"
# amount = 100
# id_assigned_to_user_by_merchant = 'YOUR_USER_ID'
# pay_page_request = PgPayRequest.pay_page_pay_request_builder(merchant_transaction_id=unique_transaction_id,
#                                                              amount=amount,
#                                                              merchant_user_id=id_assigned_to_user_by_merchant,
#                                                              callback_url=s2s_callback_url)
# pay_page_response = payment_client.pay(pay_page_request)
# pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
# print(pay_page_url)
