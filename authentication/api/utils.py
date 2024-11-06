import random
import string
    
def gen_otp():
    opt = ''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits)
                                            for _ in range(8)])
                            
    return opt