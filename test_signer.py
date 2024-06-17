import pytest, os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from signer import generate_rsa, create_keys, load_private_key_from_file, \
    load_public_key_from_file, sign_data, verify_signature


def test_save_load_keys():
    path = "/tmp"
    key_file_name = "key"
    private_key_path = path + "/" + key_file_name + "priv.pem"
    public_key_path = path + "/" + key_file_name + ".pem"
    pin = "1"
    create_keys(path=path, file_name=key_file_name, pin=pin)

    lorem_string = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in commodo diam. Mauris placerat sem "
                    "id")
    " nibh sagittis sodales. Nulla varius sollicitudin ornare. Aenean sed efficitur ex. Proin fermentum"
    " lorem sem, vitae mollis lorem auctor at. Nullam mollis diam vulputate, volutpat leo vitae,"
    " consequat nibh. Sed in enim enim. "

    public_key = load_public_key_from_file(public_key_path)
    private_key = load_private_key_from_file(url=private_key_path, pin=pin)

    encrypted_string = public_key.encrypt(lorem_string.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))

    assert lorem_string.encode() == private_key.decrypt(encrypted_string, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))

    os.remove(private_key_path)
    os.remove(public_key_path)


def test_sign_verify():
    key = generate_rsa()
    lorem_string = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in commodo diam. Mauris placerat sem "
                    "id")
    " nibh sagittis sodales. Nulla varius sollicitudin ornare. Aenean sed efficitur ex. Proin fermentum"
    " lorem sem, vitae mollis lorem auctor at. Nullam mollis diam vulputate, volutpat leo vitae,"
    " consequat nibh. Sed in enim enim. "

    signature = sign_data(lorem_string, key)
    assert verify_signature(lorem_string, key.public_key(), signature)



