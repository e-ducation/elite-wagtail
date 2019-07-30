from django.utils.translation import ugettext as _


def verify_parameters_exist(parameters_dict):
    """
    verify parameters is exist
    :param parameters:
    :return:
    """
    result = None
    parameters_dict_require = ['content']
    for i in parameters_dict_require:
        if not parameters_dict[i]:
            result = {
                "success": False,
                "code": 400,
                "msg": _('Request parameter {key} missing!'.format(key=i)),
            }
            return result
    return result
