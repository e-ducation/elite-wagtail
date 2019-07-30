from django.utils.translation import ugettext as _

def verify_parameters_exist(parameters_dict):
    """
    verify parameters is exist
    :param parameters:
    :return:
    """
    result = None
    for (key, value) in parameters_dict.items():
        if not value:
            result = {
                "success": False,
                "code": 400,
                "msg": _('Request parameter {key} missing!'.format(key=key)),
            }
            return result
    return result