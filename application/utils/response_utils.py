import datetime
import os
import string


from flask import current_app, send_file

from application.contants import DEFAULT_ERROR_CODE
from application.errors import ERROR_CODE


def error(data=None, code=DEFAULT_ERROR_CODE, msg=None, http_code=400, error_info=None):
    """
    根据错误信息构造对应body
    """
    result = {
        'data': data,
        'code': code,
        'msg': msg or ERROR_CODE.get(code, ""),
        'status': 'error',
    }
    if current_app.config.get("ENV") != 'production':
        result['error_info'] = error_info
    return result, http_code


def success(data=None, code=200, http_code=200):
    """
    组装成功时候的body
    :param data: 返回的信息
    :param code: 业务状态码
    :param http_code: http状态码
    :return: json格式错误提示字符串
    """
    result = {'code': code, 'data': data, 'msg': 'success'}
    return result, http_code


def export(file_name: str, column_fields: list, row_data: list):
    """
    导出文件
    """
    import xlsxwriter
    file_name = file_name.replace("/", "")
    file_name = f'{file_name}{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
    file_path = os.path.join(current_app.config['TEMP_DIR'], file_name)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet("数据")
    bold = workbook.add_format({'bold': True})
    for index, column in enumerate(column_fields):
        worksheet.write(string.ascii_uppercase[index] + "1", column, bold)
    row = 1
    for item in row_data:
        for i, e in enumerate(item):
            worksheet.write(row, i, e)
        row += 1
    workbook.close()
    return send_file(file_path, attachment_filename=file_name, as_attachment=True)
