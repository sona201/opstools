import json

from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS, coreapi, coreschema,
    pygments_css, yaml
)

from common.status_code import MESSAGE_MAP
import logging

logger = logging.getLogger("devops")


class CodeMsgResponse(Response):
    def __init__(self, data=None, status=200, data_status=20000,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        data_content = {
            'status': data_status,
            'message': MESSAGE_MAP.get(data_status),
            'data': data,
        }
        super(Response, self).__init__(
            # data=data_content,
            status=status,
            headers=headers,
            content_type=content_type,
            template=None
        )


def code_msg_response(data_status=20000, message=None, data=None, **kwargs):
    return Response(
        {
            "code": data_status,
            "message": message if message else MESSAGE_MAP[data_status],
            "data": data,
            **kwargs
        }
    )


def response_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        msg = "失败" if response.status_code >= 400 else "成功"
        notification_response = {
            "code": response.status_code,
            "message": msg,
            "data": response.data,
        }
        # code_msg_response(40010)
        response.data = notification_response
    return response


class FormatRenderer(JSONRenderer):
    """
    自定义返回处理
    restful 返回增加 code message data 字段
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b''

        # if isinstance(data, dict) and data.get('message') and data.get('code'):
        #     message = data.pop('message', 'success')
        #     code = data.pop('code', 20000)

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


class CustomRenderer(JSONRenderer):
    """
    自定义返回处理
    restful 返回增加 code message data 字段
    """

    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            status_code = renderer_context['response'].status_code
            if status_code < 300:
                message = 'success'
                code = 20000
                if isinstance(data, dict) and data.get('message') and data.get('code'):
                    message = data.pop('message', 'success')
                    code = data.pop('code', 20000)
                if data:
                    if len(data) == 1 and data.get('data'):
                        data = data
                ret = {
                    'message': message,
                    'code': code,
                    'data': data
                }
                # 返回JSON数据
                return super().render(ret, accepted_media_type, renderer_context)
            elif status_code >= 400:
                try:
                    logger.error(
                        'bad request method/path => ' +
                        renderer_context['request'].stream.method + ' ' +
                        renderer_context['request'].stream.path)
                    logger.error('bad request query_params => ' + str(renderer_context['request'].query_params))
                    logger.error('bad request data => ' +
                                 json.dumps(renderer_context['request'].data, ensure_ascii=False))
                    logger.error('bad request user.username => ' + renderer_context['request'].user.username)
                except AttributeError as error:
                    logger.info('bad request print error => ' + str(error))
                ret = {
                    'message': data.get('detail'),
                    'code': status_code,
                    'data': data,
                }
                return super().render(ret, accepted_media_type, renderer_context)
            else:
                return super().render(data, accepted_media_type, renderer_context)
        except Exception as err:
            logger.error('返回状态异常 data: {} err: {}'.format(data, err))
            return super().render(data, accepted_media_type, renderer_context)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data = {
            'code': response.status_code,
            'detail': response.reason_phrase
        }
        if hasattr(exc, 'detail'):
            response.data['detail'] = exc.detail

    return response
