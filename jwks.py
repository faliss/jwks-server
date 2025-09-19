from flask import Flask, jsonify, request
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64

app = Flask(__name__)

key = {}

def generate_rsa_key(expiry_minutes=60):
  private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
  )
  public_key = private_key.public_key()
  
  kid= str(int(datetime.utcnow().timestamp()))
  expiry= datetime.utcnow() + timedelta(minutes=expiry_minutes)
  
  key[kid] = {"private": private_key, "public": public_key, "expiry": expiry}
  return kid
