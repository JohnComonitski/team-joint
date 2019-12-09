from crypto import AES
import crypto


class encrypt:
    def __init__(self, config, logger):
        f = open("/sd/public.pem")
        self.pubKey = f.read()
        self.Logger = logger
        f.close()

    def RSAEncrypt(self, plainText):
        return crypto.rsa_encrypt(plainText, self.pubKey)

    def RSADecrypt(self, privKey):
        key = privKey.read()
        privKey.close()
        f = open('/sd/EMoveData.txt', 'r')
        contents = f.readlines()
        f.close()
        f = open('/sd/decryptedMoveData.txt', 'w')
        for l in contents:
            try:
                f.write(crypto.rsa_decrypt(l[:-1].encode('utf-8'), key) + "\n")
                print(crypto.rsa_decrypt(l[:-1].encode('utf-8'), key))
            except RuntimeError:
                self.Logger.log("Error: line failed to decrypt")
            except ValueError:
                self.Logger.log("Error: private key error")

        f.close()
        return
