from trezor import ui, wire


def cipher_key_value(msg, seckey: bytes) -> bytes:
    from trezor.crypto.hashlib import sha512
    from trezor.crypto import hmac
    from trezor.crypto.aes import AES_CBC_Encrypt, AES_CBC_Decrypt

    data = msg.key
    data += 'E1' if msg.ask_on_encrypt else 'E0'
    data += 'D1' if msg.ask_on_decrypt else 'D0'
    data = hmac.new(seckey, data, sha512).digest()
    key = data[:32]
    if msg.iv and len(msg.iv) == 16:
        iv = msg.iv
    else:
        iv = data[32:48]

    if msg.encrypt:
        aes = AES_CBC_Encrypt(key=key, iv=iv)
    else:
        aes = AES_CBC_Decrypt(key=key, iv=iv)

    return aes.update(msg.value)


async def layout_cipher_key_value(ctx, msg):
    from trezor.messages.CipheredKeyValue import CipheredKeyValue
    from trezor.messages.FailureType import ActionCancelled
    from trezor.ui.text import Text
    from trezor.ui.container import Container
    from ..common import seed
    from ..common.confirm import confirm

    if len(msg.value) % 16 > 0:
        raise ValueError('Value length must be a multiple of 16')

    ui.display.clear()
    title = 'Encrypt value' if msg.encrypt else 'Decrypt value'
    content = Container(Text(title, ui.ICON_RESET, msg.key, break_lines=True))

    if msg.ask_on_decrypt and not msg.encrypt or msg.ask_on_encrypt and msg.encrypt:
        result = await confirm(ctx, content)
        if result:
            node = await seed.derive_node(ctx, msg.address_n)
            value = cipher_key_value(msg, node.private_key())
            return CipheredKeyValue(value=value)
        else:
            raise wire.FailureError(ActionCancelled, 'CipherKeyValue cancelled')


