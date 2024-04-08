import json
from yookassa import Configuration,Payment
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

Configuration.account_id = os.getenv('SHOP_ID')
Configuration.secret_key = os.getenv('SHOP_API_TOKEN')

def test_pay():
	number_pay = 1111
	summa = 500
	return number_pay, summa

def payment(value,description):
	payment = Payment.create({
    		"amount": {"value": value,
        				"currency": "RUB"},
    		"payment_method_data": {
        				"type": "bank_card" },
    		"confirmation": {
        				"type": "redirect",
        				"return_url": "урл редиректа"},
    		"capture": True,
    		"description": description})
	return json.loads(payment.json())

async def check_payment(payment_id):
	payment = json.loads((Payment.find_one(payment_id)).json())
	while payment['status'] == 'pending':
		payment = json.loads((Payment.find_one(payment_id)).json())
		await asyncio.sleep(3)

	if payment['status']=='succeeded':
		print("SUCCSESS RETURN")
		print(payment)
		return True
	else:
		print("BAD RETURN")
		print(payment)
		return False