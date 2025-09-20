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

def get_jwks():
  jwks_keys = []
  for kid, key_info in keys.items():
    if key_info["expiry"] > datetime.utcnow():
      public_key = key_info["public"]
      numbers = public_key.public_numbers()
      e = base64.urlsafe_b64encode(numbers.e.to_bytes(3, 'big')).decode('utf-8').rstrip("=")
      n = base64.urlsafe_b64encode(numbers.n.to_bytes(256, 'big')).decode('utf-8').rstrip("=")
      jwks_keys.append({
            "kty": "RSA",
            "use": "sig",
            "kid": kid,
            "n": n,
            "e": e,
            "alg": "RS256"
        })
    return jwks_keys
    
@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks_endpoint():
  return jsonify({"keys": get_jwks()})

@app.route("/auth", methods=["POST"])
def auth():
  expired_param = request.args.get("expired", "false").lower()
    if expired_param == "true":
       kid = generate_rsa_key(expiry_minutes=-60)
    else:
        kid = generate_rsa_key(expiry_minutes=60)

key_info = keys[kid]
    payload = {
        "sub": "1234",
        "name": "test_user",
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int(key_info["expiry"].timestamp())
    }
    token = jwt.encode(payload, key_info["private"], algorithm="RS256", headers={"kid": kid})
    return jsonify({"token": token})

  if __name__ == "__main__":
    generate_rsa_key(expiry_minutes=60)
    generate_rsa_key(expiry_minutes=-60)
    app.run(port=8080, debug=True)
