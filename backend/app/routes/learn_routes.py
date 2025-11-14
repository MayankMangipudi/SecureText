from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.routes.crypto_routes import get_current_user
from app.schemas.learn_schema import AesVisualizeRequest, RsaVisualizeRequest
import base64

router = APIRouter(prefix="/learn")

@router.post("/aes/visualize")
def visualize_aes(request: AesVisualizeRequest, current_user: User = Depends(get_current_user)):
    """
    Returns step-by-step AES encryption process
    """
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        
        # Convert to bytes
        plaintext_bytes = request.plaintext.encode('utf-8')
        
        # The key comes as base64 string from the frontend
        try:
            # First, try to decode as base64
            key_bytes = base64.b64decode(request.key)
        except Exception as e:
            # If that fails, maybe it's already in hex or wrong format
            try:
                # Try hex format
                key_bytes = bytes.fromhex(request.key)
            except:
                raise HTTPException(400, f"Invalid key format. Please generate a new key using the Generate button.")
        
        # Validate key length (must be 16, 24, or 32 bytes for AES)
        if len(key_bytes) not in [16, 24, 32]:
            raise HTTPException(400, f"Invalid key length: {len(key_bytes)} bytes. Must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes.")
        
        steps = []
        
        # Step 1: Show original plaintext
        steps.append({
            "step": 1,
            "title": "Original Plaintext",
            "description": "Convert text to bytes",
            "data": {
                "text": request.plaintext,
                "bytes": plaintext_bytes.hex(),
                "length": len(plaintext_bytes)
            }
        })
        
        # Step 2: Padding
        padded = pad(plaintext_bytes, AES.block_size)
        steps.append({
            "step": 2,
            "title": "Apply PKCS7 Padding",
            "description": f"Pad to {AES.block_size} bytes (128 bits)",
            "data": {
                "before": plaintext_bytes.hex(),
                "after": padded.hex(),
                "padding_added": len(padded) - len(plaintext_bytes)
            }
        })
        
        # Step 3: Key scheduling (simplified)
        key_size_bits = len(key_bytes) * 8
        rounds_map = {16: 10, 24: 12, 32: 14}
        rounds = rounds_map.get(len(key_bytes), 14)
        
        steps.append({
            "step": 3,
            "title": f"AES-{key_size_bits} Key",
            "description": "The secret key used for encryption",
            "data": {
                "key": key_bytes.hex(),
                "key_size": key_size_bits,
                "rounds": rounds
            }
        })
        
        # Step 4: Actual encryption
        cipher = AES.new(key_bytes, AES.MODE_CBC)
        ciphertext = cipher.encrypt(padded)
        
        steps.append({
            "step": 4,
            "title": "AES Encryption Rounds",
            "description": f"{rounds} rounds of SubBytes, ShiftRows, MixColumns, AddRoundKey",
            "data": {
                "rounds": rounds,
                "operations": ["SubBytes", "ShiftRows", "MixColumns", "AddRoundKey"],
                "iv": base64.b64encode(cipher.iv).decode('utf-8')
            }
        })
        
        # Step 5: Final ciphertext
        result = base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
        steps.append({
            "step": 5,
            "title": "Final Ciphertext",
            "description": "IV + Encrypted Data (Base64 encoded)",
            "data": {
                "ciphertext": result,
                "length": len(ciphertext),
                "format": "Base64"
            }
        })
        
        return {"steps": steps, "final_ciphertext": result}
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Visualization error: {str(e)}")


@router.post("/rsa/visualize")
def visualize_rsa(request: RsaVisualizeRequest, current_user: User = Depends(get_current_user)):
    """
    Returns step-by-step RSA key generation and encryption
    """
    try:
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_OAEP
        import base64
        
        steps = []
        
        # Step 1: Generate two prime numbers
        key = RSA.generate(2048)
        p = key.p
        q = key.q
        
        steps.append({
            "step": 1,
            "title": "Generate Two Large Prime Numbers",
            "description": "p and q are randomly chosen primes",
            "data": {
                "p": str(p)[:50] + "...",
                "q": str(q)[:50] + "...",
                "note": "These are 1024-bit primes (very large!)"
            }
        })
        
        # Step 2: Calculate n
        n = p * q
        steps.append({
            "step": 2,
            "title": "Calculate n = p × q",
            "description": "n is the modulus for both public and private keys",
            "data": {
                "n": str(n)[:50] + "...",
                "bit_length": n.bit_length()
            }
        })
        
        # Step 3: Calculate φ(n)
        phi_n = (p - 1) * (q - 1)
        steps.append({
            "step": 3,
            "title": "Calculate φ(n) = (p-1)(q-1)",
            "description": "Euler's totient function",
            "data": {
                "phi_n": str(phi_n)[:50] + "...",
                "purpose": "Used to find private key"
            }
        })
        
        # Step 4: Public exponent
        e = key.e
        steps.append({
            "step": 4,
            "title": "Choose Public Exponent e",
            "description": "Commonly 65537 (0x10001)",
            "data": {
                "e": e,
                "condition": "1 < e < φ(n) and gcd(e, φ(n)) = 1"
            }
        })
        
        # Step 5: Private exponent
        d = key.d
        steps.append({
            "step": 5,
            "title": "Calculate Private Exponent d",
            "description": "d is the modular inverse: d × e ≡ 1 (mod φ(n))",
            "data": {
                "d": str(d)[:50] + "...",
                "relationship": "d × e mod φ(n) = 1"
            }
        })
        
        # Step 6: Show keys
        public_key = key.publickey().export_key().decode('utf-8')
        private_key = key.export_key().decode('utf-8')
        
        steps.append({
            "step": 6,
            "title": "Public & Private Keys Generated",
            "description": "Public key (n, e) can be shared. Private key (n, d) must be kept secret",
            "data": {
                "public_key": public_key.split('\n')[1][:60] + "...",
                "private_key": "KEEP SECRET",
                "public_components": {"n": "modulus", "e": str(e)},
                "private_components": {"n": "modulus", "d": "secret exponent"}
            }
        })
        
        # Step 7: Encrypt
        cipher = PKCS1_OAEP.new(key.publickey())
        ciphertext = cipher.encrypt(request.plaintext.encode('utf-8'))
        ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        
        steps.append({
            "step": 7,
            "title": "Encryption: c = m^e mod n",
            "description": "Message is encrypted using public key",
            "data": {
                "plaintext": request.plaintext,
                "ciphertext": ciphertext_b64[:60] + "...",
                "formula": "ciphertext = plaintext^e mod n"
            }
        })
        
        # Step 8: Decrypt (demonstration)
        steps.append({
            "step": 8,
            "title": "Decryption: m = c^d mod n",
            "description": "Only private key holder can decrypt",
            "data": {
                "formula": "plaintext = ciphertext^d mod n",
                "note": "Private key (d) reverses the encryption"
            }
        })
        
        return {
            "steps": steps,
            "keys": {
                "public": public_key,
                "private": private_key
            },
            "encrypted": ciphertext_b64
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Visualization error: {str(e)}")
