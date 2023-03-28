import threading
import time

from flask import current_app, request, render_template

from application.extensions import siwa, cache, openai_api
from . import web_bp


@web_bp.route("/company", methods=["GET", "POST"])
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


@web_bp.get("/")
def chat():
    return render_template("chatgpt.html")
