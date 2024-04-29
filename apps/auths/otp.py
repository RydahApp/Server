import pyotp

# Generates 4 digit OTP with 30mins validity
def generateKey():
    secret = pyotp.random_base32()        
    totp = pyotp.TOTP(secret, digits=4, interval=1800)
    OTP = totp.now()
    return {"totp":secret,"OTP":OTP}

# Verifies 4 digit OTP
def verify_otp(activation_key,otp):
    totp = pyotp.TOTP(activation_key, digits=4, interval=1800)
    verify = totp.verify(otp)
    return verify