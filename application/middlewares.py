# -*- coding: utf-8 -*-


class WSGICopyBodyMiddleware(object):
    """
    没有找到可靠的方法找到原始的请求体， 参考了stackoverflow上面一个回答
    https://stackoverflow.com/questions/10999990/get-raw-post-body-in-python-flask-regardless-of-content-type-header
    代码基本相同， 只是兼容了python3
    """
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        from io import BytesIO
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['body_copy'] = body
        environ['wsgi.input'] = BytesIO(body)

        # Call the wrapped application
        app_iter = self.application(environ,
                                    self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback

