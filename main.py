import readchar
import signal
from wake import *
from ioutil import *

### Prints formatted current open, encrypted and decrypted texts.
###
def print_iteration():
    decrypted_msg_type = 'good' if open_text == decrypted_text else 'bad'
    print_help()
    pretty_print(f'Encrypted text: "{encrypted_text}"\n', type='good')
    pretty_print(f'Decrypted text: "{decrypted_text}"\n', type=decrypted_msg_type)
    print(f'Open text: "{open_text}"', end=f'\rOpen text: "{open_text}', flush=True)


### Example of the WAKE algorithm usage.
# Reads user input by character and prints encrypted and decrypted texts
# Used files:
# file "key":    contains 16-byte key
###
if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_on_sigint)

    key_file = 'key'
    key = read(key_file)

    if key is None:
        sys.exit(2)

    open_text = ""
    encrypted_text = ""
    decrypted_text = ""

    try:
        wake_enc = Wake(key)
        wake_dec = Wake(key)
    except AssertionError as e:
        pretty_print(e.args[0], type='bad')
        exit(2)

    print_iteration()
    while True:
        c = readchar.readchar()
        c_enc = wake_enc.encrypt(c)
        open_text += c
        encrypted_text += c_enc
        decrypted_text += wake_dec.decrypt(c_enc)
        clear_console()
        print_iteration()
