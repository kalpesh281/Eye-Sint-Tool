import requests
from modules.export import export
requests.packages.urllib3.disable_warnings()

def headers(target, output, data):
    result = {}
    print(f'\nHeaders :\n')
    try:
        rqst = requests.get(target, verify=False, timeout=10)
        for key, val in rqst.headers.items():
            print(f'{key} : {val}')
            if output != 'None':
                result.update({key: val})
    except Exception as e:
        print(f'\nException : {e}\n')
        if output != 'None':
            result.update({'Exception': str(e)})     
    result.update({'exported': False})

    if output != 'None':
        fname = f'{output["directory"]}/headers.{output["format"]}'
        print(f'Generated File Path: {fname}')  # Add this line for debugging
        output['file'] = fname
        data['module-headers'] = result
        export(output, data)



# def headers(target, output, data):
#     result = {}
#     print(f'\nHeaders :\n')
#     try:
#         rqst = requests.get(target, verify=False, timeout=10)
#         for key, val in rqst.headers.items():
#             print(f'{key} : {val}')
#             if output != 'None':
#                 result.update({key: val})
#     except Exception as e:
#         print(f'\nException : {e}\n')
#         if output != 'None':
#             result.update({'Exception': str(e)})     
#     result.update({'exported': False})

#     if output != 'None':
#         fname = f'{output["directory"]}/headers.{output["format"]}'
#         print(f'Generated File Path: {fname}')  # Add this line for debugging
#         output['file'] = fname
#         data['module-headers'] = result
#         export(output, data)
#         # fname = f'{output["directory"]}/headers.{output["format"]}'
#         # output['file'] = fname
#         # data['module-headers'] = result
#         # export(output, data)
