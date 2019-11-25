import crypto

class encrypt:
    def __init__(self, config):
        self.key = config["rijndael"]["publicKey"]
        # Example of a JWT header + payload
        self.header_payload = "eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ"
        # Private key MUST BE in PKCS8 format !!!
        self.f = open("cert/private_key_pkcs8.pem")
        self.pk = f.read()
        # Generate the signature
        self.signature = crypto.generate_rsa_signature(header_payload, pk, pers="my_pers_string")

    def encrypt(plainText):
        $ openssl genrsa -des3 -out private.pem 2048
        # export the RSA public key to a file
        $ openssl rsa -in private.pem -outform PEM -pubout -out public.pem
        # export the RSA private key to a file
        $ openssl rsa -in private.pem -out private_unencrypted.pem -outform PEM

        return crypto.rsa_encrypt(plainText, self.pk)
