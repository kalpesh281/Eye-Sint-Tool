import ssl
from modules.export import export
import OpenSSL
import datetime
import pytz


def convert_asn1_time(asn1_time):
    timestamp = asn1_time.decode("utf-8")
    dt = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%SZ")
    dt_utc = pytz.utc.localize(dt)
    return dt_utc.strftime("%d %B %Y %H:%M:%S %Z")



def ssl_analyzer(target, output, data):
    if target.startswith("http://"):
        target = target[len("http://"):]
    elif target.startswith("https://"):
        target = target[len("https://"):]

    # print(target)
    result = {}
    print('\nSSL Certificate Analysis:\n')
    try:
        cert = ssl.get_server_certificate((target, 443))
        x509 = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)

        print(f'Expired: {x509.has_expired()}')
        print(f'Signature Algorithm: {x509.get_signature_algorithm()}')
        result['Expired'] = x509.has_expired()
        result['Signature Algorithm'] = x509.get_signature_algorithm()

        for item in x509.get_subject().get_components():
            print(f'Subject {item[0]}: {item[1]}')
            result[f'Subject {item[0]}'] = item[1]

        print(f'Subject Hash: {x509.get_subject().hash()}')
        result['Subject Hash'] = x509.get_subject().hash()

        for item in x509.get_issuer().get_components():
            print(f'Issuer {item[0]}: {item[1]}')
            result[f'Issuer {item[0]}'] = item[1]

        print(f'Issuer Hash: {x509.get_issuer().hash()}')
        result['Issuer Hash'] = x509.get_issuer().hash()

        for i in range(x509.get_extension_count()):
            ext_name = x509.get_extension(i).get_short_name()
            ext_value = x509.get_extension(i).__str__()
            print(f'Extension {ext_name}: {ext_value}')
            result[f'Extension {ext_name}'] = ext_value

        print(f'\nPublic Key Bits: {x509.get_pubkey().bits()}')
        result['Public Key Bits'] = x509.get_pubkey().bits()

        print(f'Public Key Type: {x509.get_pubkey().type()}')
        result['Public Key Type'] = x509.get_pubkey().type()

        print(f'Public Key only public: {x509.get_pubkey()._only_public}')
        result['Public Key only public'] = x509.get_pubkey()._only_public

        print(f'Public Key initialized: {x509.get_pubkey()._initialized}')
        result['Public Key initialized'] = x509.get_pubkey()._initialized

        serial_number = x509.get_serial_number()
        serial_hex = hex(serial_number).rstrip('L').lstrip('0x')
        print(f'Serial Number: {serial_number}')
        result['Serial Number'] = serial_number

        print(f'Serial Number Length: {serial_number.bit_length()}')
        result['Serial Number Length'] = serial_number.bit_length()

        print(f'\nMD5: {x509.digest("md5")}')
        result['MD5'] = x509.digest('md5')

        print(f'SHA1: {x509.digest("sha1")}')
        result['SHA1'] = x509.digest('sha1')

        print(f'SHA256: {x509.digest("sha256")}')
        result['SHA256'] = x509.digest('sha256')

        print(f'SHA512: {x509.digest("sha512")}')
        result['SHA512'] = x509.digest('sha512')

        valid_from = convert_asn1_time(x509.get_notBefore())
        valid_until = convert_asn1_time(x509.get_notAfter())

        valid_from_date = datetime.datetime.strptime(valid_from, "%d %B %Y %H:%M:%S %Z")
        valid_until_date = datetime.datetime.strptime(valid_until, "%d %B %Y %H:%M:%S %Z")

        days_difference = (valid_until_date - valid_from_date).days

        print(f'\nValid from: {valid_from}')
        result['Valid from'] = valid_from

        print(f'Valid until: {valid_until}')
        result['Valid until'] = valid_until

        result['Days Difference'] = days_difference
        print(f'Days Difference: {days_difference} days')
                
        result['exported'] = False
        return result

    except Exception as e:
        print(f'\nException: {e}')
        result['Exception'] = str(e)
        # return result

    if output != 'None':
        fname = f'{output["directory"]}/ssl_analysis.{output["format"]}'
        output['file'] = fname
        data['module-ssl_analysis'] = result
        export(output, data)
