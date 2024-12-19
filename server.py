#!/usr/bin/python3
# coding: utf-8
import time
import utils as u
from data import data as data_init
from flask import Flask, render_template, request, url_for, redirect, flash, make_response, jsonify
from markupsafe import escape
import json

d = data_init()
app = Flask(__name__)

time_get = time.time()
pc_time_get = time.time()
status = d.dget('status')
pc_status = d.dget('pc_status')
app_name = d.dget('app_name')
pc_app_name = d.dget('pc_app_name')

def check_timeout():
    global time_get, pc_time_get, status, pc_status
    now_time = time.time()
    if now_time - time_get > 60 and status != 1:
        status = 1
        d.dset('status', status)
        d.dset('app_name', [])
        u.info(f'status changed to: {status} due to timeout')
    if now_time - pc_time_get > 60 and pc_status != 1:
        pc_status = 1
        d.dset('pc_status', pc_status)
        d.dset('pc_app_name', [])
        u.info(f'PC status changed to: {pc_status} due to timeout')




def reterr(code, message):
    ret = {
        'success': False,
        'code': code,
        'message': message
    }
    u.error(f'{code} - {message}')
    return u.format_dict(ret)


def showip(req, msg):
    ip1 = req.remote_addr
    try:
        ip2 = req.headers['X-Forwarded-For']
        u.infon(f'- Request: {ip1} / {ip2} : {msg}')
    except:
        ip2 = None
        u.infon(f'- Request: {ip1} : {msg}')


@app.route('/')
def index():
    d.load()
    showip(request, '/')
    other = d.data['other']
    try:
        status = d.data['status_list'][d.data['status']]
    except:
        status = {
            'id': -1,
            'name': '未知',
            'desc': '未知的标识符，可能是配置问题。',
            'color': 'error'
        }
    return render_template(
        'index.html',
        user=other['user'],
        learn_more=other['learn_more'],
        repo=other['repo'],
        status_name=status['name'],
        status_desc=status['desc'],
        status_color=status['color'],
        more_text=other['more_text']
    )


@app.route('/style.css')
def style_css():
    response = make_response(render_template(
        'style.css',
        bg=d.data['other']['background'],
        alpha=d.data['other']['alpha']
    ))
    response.mimetype = 'text/css'
    return response


@app.route('/query')
def query():
    d.load()
    showip(request, '/query')
    st = d.data['status']
    # stlst = d.data['status_list']
    try:
        stinfo = d.data['status_list'][st]
    except:
        stinfo = {
            'status': st,
            'name': '未知'
        }
    ret = {
        'success': True,
        'status': st,
        'info': stinfo
    }
    return u.format_dict(ret)


@app.route('/get/status_list')
def get_status_list():
    showip(request, '/get/status_list')
    stlst = d.dget('status_list')
    return u.format_dict(stlst)


@app.route('/status', methods=['GET'])
def status():
    showip(request, '/status')

    # 获取参数
    global time_get
    secret = request.args.get("secret")
    status = escape(request.args.get("status"))
    app_name = request.args.getlist("app_name")

    check_timeout()

    # 验证secret（如果存在）
    if secret:
        secret_real = d.dget('secret')
        if secret != secret_real:
            return jsonify({
                'success': False,
                'code': 'not authorized',
                'message': 'invalid secret'
            }), 403

        # 更新状态
        if status is not None:
            d.dset('status', status)

        if app_name:
            d.dset('app_name', app_name)

        u.info(f'Set status:{status}, app_name: {app_name}, secret: "{secret}"')
        u.info('set success')

        time_get = time.time()

    # 获取当前的状态和应用名称列表
    current_status = d.dget('status')
    current_app_name = d.dget('app_name') or []

    time_get = time.time()

    ret = {
        'success': True,
        'info': {
            'status': current_status,
            'app_name': current_app_name,
        }
    }

    return jsonify(ret)

@app.route('/pc_status', methods=['GET'])
def pc_status():
    showip(request, '/pc_status')

    # 获取参数
    global pc_time_get
    secret = request.args.get("secret")
    pc_status = escape(request.args.get("pc_status"))
    pc_app_name = request.args.getlist("pc_app_name")

    check_timeout()

    # 验证secret（如果存在）
    if secret:
        secret_real = d.dget('secret')
        if secret != secret_real:
            return jsonify({
                'success': False,
                'code': 'not authorized',
                'message': 'invalid secret'
            }), 403

        # 更新状态
        if pc_status is not None:
            d.dset('pc_status', pc_status)

        if pc_app_name :
            d.dset('pc_app_name', pc_app_name)

        u.info(f'Set pc_status:{pc_status}, pc_app_name: {pc_app_name}, secret: "{secret}"')
        u.info('set success')

        pc_time_get = time.time()

    # 获取当前的状态和应用名称列表
    current_pc_status = d.dget('pc_status')
    current_pc_app_name = d.dget('pc_app_name') or []

    ret = {
        'success': True,
        'info': {
            'pc_status': current_pc_status,
            'pcapp_name': current_pc_app_name,
        }
    }

    return jsonify(ret)



@app.route('/set/<secret>/<int:status>')
def set_path(secret, status):
    showip(request, f'/set/{secret}/{status}')
    secret = escape(secret)
    u.info(f'status: {status}, secret: "{secret}"')
    secret_real = d.dget('secret')
    if secret == secret_real:
        d.dset('status', status)
        u.info('set success')
        ret = {
            'success': True,
            'code': 'OK',
            'set_to': status
        }
        return u.format_dict(ret)
    else:
        return reterr(
            code='not authorized',
            message='invaild secret'
        )


if __name__ == '__main__':
    d.load()
    app.run(
        host=d.data['host'],
        port=d.data['port'],
        debug=d.data['debug']
    )
