import threading
import time

from flask import current_app, request, render_template
from wechatpy.events import SubscribeScanEvent, ScanEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature

from application.extensions import siwa, cache, openai_api
from . import wechat_bp

from ...dto import ResponseSuccessDto
from ...dto.wechat import SignatureDto
from ...errors import WechatError
from wechatpy import parse_message

from ...services.openai_service import set_answer


@wechat_bp.get('/wechat')
@siwa.doc(query=SignatureDto, resp=ResponseSuccessDto, group="wechat")
def signature_validate(query: SignatureDto):
    """
    微信服务器校验
    """
    try:
        token = current_app.config.get("WECHAT_TOKEN")
        check_signature(token, query.signature, query.timestamp, query.nonce)
        return query.echostr
    except InvalidSignatureException:
        raise WechatError(msg="invalid signature")


@wechat_bp.post("/wechat")
def handler_wx_msg():
    """
    处理微信事件
    """
    msg = parse_message(request.data)
    openid = request.args.get("openid")
    current_app.logger.info("openid:%s", openid)
    if isinstance(msg, (SubscribeScanEvent, ScanEvent)):
        # 关注或扫二维码
        result = TextReply(content="欢迎使用志军的私人AI助理，请直接输入问题，技术支持：lzjun567", message=msg).render()
    elif isinstance(msg, TextMessage):
        question = msg.content
        if question != "继续":
            current_app.logger.info(f"问题：{question}")
            s = threading.Thread(target=set_answer, args=(openid, question))
            s.start()
            time.sleep(2)
            answer = cache.pop(openid)
            if not answer:
                answer = "我正在思考中，请稍后回复【继续】获取回答"
        else:
            answer = cache.pop(openid)
            if not answer:
                answer = "请稍后，还没准备好参考答案"
        result = TextReply(content=answer, message=msg).render()
    else:
        result = TextReply(content="欢迎使用志军的私人AI助理", message=msg).render()
    return result


@wechat_bp.route("/company", methods=["GET", "POST"])
def handler_company():
    """
    根据公司信息生成一句话简介
    """
    answer = ""
    if request.method == 'POST':
        intro = request.form.get("intro")
        question = f"'''{intro}'''\n" \
                   f"基于上面几段话生成一句话简介，格式：xxx商， 必须以 xxx提供商/服务商/销售商/品牌商/运营商/开发商/生产商/研发商/制造商/供应商/平台商 结尾，" \
                   f"不得超过20个字符，不要标点符号"
        answer = openai_api.answer(question).strip()
    return render_template("company.html", answer=answer)
