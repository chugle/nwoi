# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ########################################################################
# # This is a sample controller
# # - index is the default action of any application
# # - user is required for authentication and authorization
# # - download is for downloading files uploaded in the db (does streaming)
# # - api is an example of Hypermedia API support and access control
#########################################################################
from gluon.tools import Crud

crud = Crud(db)
crud.settings.download_url = URL('download')
crud.settings.update_deletable = True
crud.settings.keepvalues = True


def congfutimu(form):
    if db.timu((db.timu.oj == form.vars.oj) & (db.timu.bianhao == form.vars.bianhao)):
        form.errors = True
        response.flash = '题目已存在'


crud.settings.create_onvalidation.timu.append(congfutimu)


def index():
    if auth.user:
        print auth.user
        jisuanjifen()
    rows = db(db.auth_user.yingcang==False).select(db.auth_user.first_name,db.auth_user.last_name, db.auth_user.jifen, orderby=~db.auth_user.jifen)
    left = SQLTABLE(rows, headers={'auth_user.first_name': '姓名', 'auth_user.last_name':'学号','auth_user.jifen': '积分'})
    firstzuoye = db().select(db.zuoye.id).first().id
    title=db.zuoye[firstzuoye].title
    qtid = db.zuoye[firstzuoye].qingtong
    byid = db.zuoye[firstzuoye].baiying
    hjid = db.zuoye[firstzuoye].huangjing
    qttm = db.timu[qtid]
    bytm = db.timu[byid]
    hjtm = db.timu[hjid]
    a1 = A('青铜：' + qttm.biaoti + '通过数:' + str(qttm.tongguo), _href=URL('viewtimu', args=[qtid]))
    a2 = A('白银：' + bytm.biaoti + '通过数:' + str(qttm.tongguo), _href=URL('viewtimu', args=[byid]))
    a3 = A('黄金：' + hjtm.biaoti + '通过数:' + str(qttm.tongguo), _href=URL('viewtimu', args=[hjid]))

    return dict(left=left, title=title,a1=a1, a2=a2, a3=a3)


@auth.requires_login()
def createtimu():
    db.timu.zuozhe.default = auth.user.id
    return dict(form=crud.create(db.timu, next=URL('timus'), message='add sucessed'))


@auth.requires_login()
def edittimu():
    return dict(form=crud.update(db.timu, request.args[0]))


@auth.requires_login()
def tijiao():
    timu = request.args[0]
    if db.tijiao((db.tijiao.timu == timu) & (db.tijiao.zuozhe == auth.user.id)):
        return dict(form='已经提交该题')
    db.tijiao.timu.default = timu
    db.tijiao.zuozhe.default = auth.user.id
    form = crud.create(db.tijiao, next=URL('timus'), message='已提交')
    return dict(form=form)


@auth.requires_login()
def createjietibaogao():
    timu = request.args[0]
    if db.jietibaogao((db.jietibaogao.timu == timu) & (db.jietibaogao.zuozhe == auth.user.id)):
        return dict(form='已经提交该题解题报告')
    db.jietibaogao.timu.default = timu
    db.jietibaogao.zuozhe.default = auth.user.id
    db.jietibaogao.timu.writable=False
    form = crud.create(db.jietibaogao, next=URL('jietibaogaos', args=[timu]), message='已提交')
    return dict(form=form)


@auth.requires_login()
def tijiaos():
    grid = SQLFORM.grid(
        db.tijiao,
        fields=[db.tijiao.timu, db.tijiao.zuozhe, db.tijiao.shijian, db.tijiao.yuyan, db.tijiao.tongguo],
        orderby=~db.tijiao.id,
        create=False,
        deletable=False,
        details=False,
        editable=False,
        csv=False,
        links=[dict(header='查看', body=lambda row: A('查看', _href=URL('viewtijiao', args=[row.id])))])
    return locals()


@auth.requires_login()
def zuoyes():
    grid = SQLFORM.grid(
        db.zuoye,
        orderby=~db.zuoye.id,
        create=False,
        deletable=False,
        editable=False,
        details=False,
        csv=False,
        links_in_grid=True,
        links=[dict(header='查看', body=lambda row: A('查看', _href=URL('viewzuoye', args=[row.id])))]
    )
    return locals()


@auth.requires_login()
def viewtimu():
    timuid = request.args[0]
    if db.tijiao((db.tijiao.timu == timuid) & (auth.user.id == db.tijiao.zuozhe)):
        tjid = db.tijiao(db.tijiao.timu == timuid).id
        tijiaourl = A('已提交', _href=URL('viewtijiao', args=[tjid]))
    else:
        tijiaourl = A('提交', _href=URL('tijiao', args=[timuid]))
    jietibaogaourl=A('解题报告',_href=URL('jietibaogaos',args=[timuid]))
    pingluns=db(db.pinglun.timu==timuid).select()
    formpl=[]
    for pl in pingluns:
        formpl.append(crud.read(db.pinglun,pl.id))
    db.pinglun.timu.default=timuid
    db.pinglun.zuozhe.default=auth.user.id
    addpinglun=crud.create(db.pinglun,next=request.url)
    return dict(form=crud.read(db.timu, timuid),
                tijiaourl=tijiaourl,jietibaogaourl=jietibaogaourl,
                pingluns=formpl,addpinglun=addpinglun)


@auth.requires_login()
def viewtijiao():
    tjid = request.args[0]
    if db.tijiao[tjid].zuozhe == auth.user.id:
        return dict(form=crud.read(db.tijiao, tjid))
    return '只能查看本人提交'


@auth.requires_login()
def viewjietibaogao():
    jtbgid = request.args[0]
    return dict(form=crud.read(db.jietibaogao, jtbgid))


@auth.requires_login()
def viewzuoye():
    zuoyeid = request.args[0]
    title=db.zuoye[zuoyeid].title
    qtid = db.zuoye[zuoyeid].qingtong
    byid = db.zuoye[zuoyeid].baiying
    hjid = db.zuoye[zuoyeid].huangjing
    qttm = db.timu[qtid]
    bytm = db.timu[byid]
    hjtm = db.timu[hjid]
    a1 = A('青铜：' + qttm.biaoti + '------通过数:' + str(qttm.tongguo), _href=URL('viewtimu', args=[qtid]))
    a2 = A('白银：' + bytm.biaoti + '------通过数:' + str(qttm.tongguo), _href=URL('viewtimu', args=[byid]))
    a3 = A('黄金：' + hjtm.biaoti + '------通过数:' + str(qttm.tongguo), _href=URL('viewtimu', args=[hjid]))

    return dict(title=title,a1=a1, a2=a2, a3=a3)


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def managetijiaos():
    db.tijiao.tongguo.writable = True
    grid = SQLFORM.grid(
        db.tijiao,
        editable=True,
        details=True,
        selectable=None,
        create=True
    )
    return dict(form=grid)


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def managezuoyes():
    grid = SQLFORM.grid(db.zuoye, orderby=~db.zuoye.id)
    return dict(form=grid)


@auth.requires_login()
def timus():
    add = A('新建', _href=URL('createtimu'))
    grid = SQLFORM.grid(
        db.timu,
        fields=[db.timu.biaoti, db.timu.zuozhe, db.timu.shijian, db.timu.oj, db.timu.bianhao, db.timu.jifen,
                db.timu.tongguo],
        orderby=~db.timu.id,
        create=False,
        deletable=False,
        editable=False,
        csv=False,
        links_in_grid=True,
        details=False,
        links=[dict(header='提交', body=lambda row: A('提交', _href=URL('tijiao', args=[row.id]))),
               dict(header='查看', body=lambda row: A('查看', _href=URL('viewtimu', args=[row.id]))),
               dict(header='解题报告', body=lambda row: A('报告', _href=URL('jietibaogaos', args=[row.id])))])
    return locals()


@auth.requires_login()
def jietibaogaos():
    timuid = request.args(0)
    add = A('新建', _href=URL('createjietibaogao', args=[timuid]))
    if timuid:
        rows = db(db.jietibaogao.timu == timuid).select(db.jietibaogao.id,
                                                        db.jietibaogao.zuozhe,
                                                        db.jietibaogao.shijian,
                                                        db.jietibaogao.jifen,
                                                        orderby=~db.jietibaogao.jifen
        )

    else:
        rows = db().select(db.jietibaogao.id,
                           db.jietibaogao.timu,
                           db.jietibaogao.zuozhe,
                           db.jietibaogao.shijian,
                           db.jietibaogao.jifen,
                           orderby=~db.jietibaogao.jifen)
    form = SQLTABLE(rows,
                    headers={'jietibaogao.id': 'id',
                             'jietibaogao.timu': '题目',
                             'jietibaogao.zuozhe': '作者',
                             'jietibaogao.shijian': '时间',
                             'jietibaogao.jifen': '积分',
                    },
                    extracolumns=[{'label': A('查看', _href='#'),
                                   'class': '',  #class name of the header
                                   'width': '',  #width in pixels or %
                                   'content': lambda row, rc: A('查看', _href=URL('viewjietibaogao', args=[row.id])),
                                   'selected': False}])
    return dict(add=add,form=form)


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def managejietibaogaos():
    db.jietibaogao.jifen.writable = True
    grid = SQLFORM.grid(db.jietibaogao, orderby=~db.jietibaogao.id)
    return dict(form=grid)


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def managetimus():
    db.timu.jifen.writable = True
    grid = SQLFORM.grid(
        db.timu,
        editable=True,
        details=True,
        selectable=None,
        create=True
    )
    return dict(form=grid)


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def tongguotimu():
    row = db(db.timu.jifen == 0).select().first()
    if row:
        db.timu.jifen.writable = True
        form = SQLFORM(db.timu, row.id, upload=URL('download'))
        if form.process().accepted:
            response.flash = 'finished'
            redirect(request.url)
    else:
        return dict(form='全部已完成')
    return dict(form=form)


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def tongguotijiao():
    image = ''
    row = db(db.tijiao.tongguo == False).select().first()
    if row:
        timuid=row.timu
        image = db.timu[timuid].jietu
        db.tijiao.tongguo.writable = True
        form = SQLFORM(db.tijiao, row.id, upload=URL('download'))
        if form.process().accepted:
            response.flash = 'finished'
            jisuantongguo(timuid)
            redirect(request.url)
    else:
        return dict(form='全部已完成', image=image)
    return dict(form=form, image=IMG(_src=URL('download',args=[image])))


@auth.requires(auth.has_membership(role='teacher'), requires_login=True)
def tongguojietibaogao():
    image = ''
    row = db(db.jietibaogao.jifen == 0).select().first()
    if row:
        image = db.timu[row.timu].jietu
        db.jietibaogao.jifen.writable = True
        form = SQLFORM(db.jietibaogao, row.id, upload=URL('download'))
        if form.process().accepted:
            response.flash = 'finished'
            redirect(request.url)
    else:
        return dict(form='全部已完成', image=image)
    return dict(form=form, image=IMG(_src=URL('download',args=[image])))

@auth.requires(auth.has_membership(role='teacher'), requires_login=True)

def jiajianfen():
    form=SQLFORM.grid(db.jiajianfen,orderby=~db.jiajianfen.id)
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection

    rules = {
        '<tablename>': {'GET': {}, 'POST': {}, 'PUT': {}, 'DELETE': {}},
    }
    return Collection(db).process(request, response, rules)


def jisuanjifen():
    userid=auth.user.id
    sumjjf=db.jiajianfen.fenzhi.sum()
    sumjtbg=db.jietibaogao.jifen.sum()
    sumtj=db.timu.jifen.sum()
    userjiajianfen=db(db.jiajianfen.zuozhe==userid).select(sumjjf).first()[sumjjf]
    usertijiaos=db((db.tijiao.timu==db.timu.id) & (db.tijiao.zuozhe==userid)).select(sumtj,left=db.tijiao).first()[sumtj]
    userjietibaogaos=db(db.jietibaogao.zuozhe==userid).select(sumjtbg).first()[sumjtbg]
    if not userjiajianfen:userjiajianfen=0
    if not userjietibaogaos:userjietibaogaos=0
    if not usertijiaos:usertijiaos=0
    jifen=userjiajianfen+usertijiaos+userjietibaogaos
    db.auth_user[userid]=dict(jifen=jifen)
    return jifen

def jisuantongguo(timuid):
    n=db((db.tijiao.tongguo==True) & (db.tijiao.timu==timuid)).count()
    db.timu[timuid] = dict(tongguo=n)
    return n


@auth.requires_login()
def myjiajianfen():
    jiajianfen=db(db.jiajianfen.zuozhe==auth.user.id).select(orderby=~db.jiajianfen.id)
    return dict(form=SQLTABLE(jiajianfen,
                              headers={'jiajianfen.id':'id',
                                       'jiajianfen.zuozhe':'用户',
                                       'jiajianfen.fenzhi':'分值',
                                       'jiajianfen.shijian':'时间',
                                       'jiajianfen.beizhu':'原因'}))