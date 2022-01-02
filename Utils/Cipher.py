from Crypto.Cipher import AES
import pbkdf2
import os
from tqdm.tk import trange
# // class __PBKDF2Cipher(object):
# //    def __init__(self, salt):
# //        self.salt = salt
    
#  //   def derive_pbkdf2(self, password):
#  //       generator = pbkdf2.PBKDF2(password, self.salt, 8)
#   //      return generator.read(32)


class AESCipher(object):
    r"""
    The class of aes cipher, mode is CBC.

    :param key: the key of en(de)crypt session.
    :param iv: the iv of en(de)crypt session.
    :param passphrase: the password of en(de)crypt session.
    :type key: bytes, default None.
    :type iv: bytes, default b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'.
    :type passphrase: string, default None.
    """
    def __init__(self, key:bytes = None, iv=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', passphrase=None, salt='\x00'):
        self.iv = iv
        def derive_pbkdf2(self, password):
            generator = pbkdf2.PBKDF2(password, self.salt, 8)
            return generator.read(32)
        if not (key is None and passphrase is None):
            if key is None:
                self.salt = salt
                self.key = derive_pbkdf2(self, password=passphrase)
                self.passphrase = passphrase
                #
                #  //self.crypto = AES.new(self.key, AES.MODE_CBC, self.iv) # * create the object of AES Cipher.
                return
            if key.__len__() <= 32 and iv.__len__() <= 16:
                key = key.ljust(32, b'\x00') # fix NUL
                iv = iv.ljust(16, b'\x00')
                self.key = key
                # // self.crypto = AES.new(self.key, AES.MODE_CBC, self.iv) # * create the object of AES Cipher.
            else:
                raise ValueError("Please check key and iv, if key's length is higher than 32 bytes or iv's length is higher than 16 bytes, please change it.")
        else:
            raise ValueError()
    
    def __fix_16(self, content: bytes):
        len = content.__len__()
        len_fix = 16 - (len % 16)
        # print(len_fix)
        return content + (b'\xf9' * len_fix)

    def encrypt(self, content: bytes):
        """
        encrypt content
        :param content: the content of encrypt session
        :type content: bytes
        """
        self.crypto = AES.new(self.key, AES.MODE_CBC, self.iv) # * create the object of AES Cipher.
        return self.crypto.encrypt(self.__fix_16(content))
    
    def decrypt(self, enc_content):
        """
        decrypt content
        :param enc_content the content of decrypt session(It's encrypted).
        """
        self.crypto = AES.new(self.key, AES.MODE_CBC, self.iv)  # * create the object of AES Cipher.
        return (self.crypto.decrypt(enc_content)).rstrip(b'\xf9')
    
    def encrypt_file(self, file_path, enc_file_path):
        fp = open(file_path, mode='rb')
        fp_enc = open(enc_file_path, mode='wb')
        header = pbkdf2.PBKDF2(self.passphrase, '\xfe', 8).read(32)
        #content = fp.read()
#        enc_bytes = self.encrypt(content=content)
        fp_enc.write(header)
        tmp = os.stat(file_path).st_size % 268435456
        for i in trange(os.stat(file_path).st_size // 268435456):
            content = self.encrypt(fp.read(268435456))
            fp_enc.write(content)
        content = self.encrypt(fp.read())
        fp_enc.write(content)
        fp_enc.close()

    def decrypt_file(self, file_path, dec_file_path):
        fp = open(file_path, mode='rb')
        fp_dec = open(dec_file_path, mode='wb')
        hash = fp.read(32)
        #content = fp.read()
        if hash != (pbkdf2.PBKDF2(self.passphrase, '\xfe', 8).read(32)):
            raise ValueError('Passphrase wrong')
        for i in trange(((os.stat(file_path).st_size) - 32) // 268435456):
            content = self.decrypt(fp.read(268435456))
            fp_dec.write(content)
        #dec_content = self.decrypt(content)
        #fp_dec.write(dec_content)
        content = self.decrypt(fp.read())
        fp_dec.write(content)
        fp_dec.close()
