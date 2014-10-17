# -*- coding: utf-8 -*-

# ########################################################################
# # This scaffolding model makes your app work on Google App Engine too
# # File is released under public domain and you can use without limitations
# ########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()
# db+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
auth.settings.extra_fields['auth_user'] = [
    Field('yingcang', 'boolean', default=False, label='隐藏', writable=False),
    Field('jifen', 'integer', label='积分', default=0, writable=False)
]
auth.define_tables(username=False, signature=False)

db.auth_user.first_name.label = '姓名'
db.auth_user.last_name.label = '学号'
db.auth_user.first_name.requires = IS_NOT_EMPTY()
db.auth_user.last_name.requires = [IS_NOT_EMPTY(), IS_MATCH('^\d\d\d\d\d\d$', error_message='请输入6位长学号')]

##changed
db.auth_user._format = '%(first_name)s(%(last_name)s):%(jifen)s'
## create all tables needed by auth if not custom tables
#----------------------------------------------------------------------------------------------
## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
#auth.settings.actions_disabled = ['profile','register']


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
import datetime

db.define_table('timu',
                Field('biaoti', requires=IS_NOT_EMPTY(), label='标题'),
                Field('zuozhe', db.auth_user, writable=False, label='作者'),
                Field('shijian', 'datetime', label='时间', default=datetime.datetime.now(), writable=False),
                Field("wangzhi", requires=IS_NOT_EMPTY(), label='完整网址'),
                Field('oj', requires=IS_IN_SET(['codevs', 'ningwai', 'szoj', 'jzxx', 'vijos', 'rqnoj']), label='oj'),
                Field('bianhao', requires=[IS_NOT_EMPTY(), IS_MATCH('^\d\d\d\d$', error_message='请输入正确题号')],
                      label='编号'),
                Field('neirong', 'text', requires=IS_NOT_EMPTY(), label='内容'),
                Field('jietu', 'upload', label='网页截图', autodelete=True, requires=IS_NOT_EMPTY()),
                Field('jifen', 'integer', default=0, label='积分', writable=False),
                Field('tongguo', 'integer', default=0, label='通过人数', writable=False),
                format='%(oj)s%(bianhao)s-%(biaoti)s')


db.define_table('tijiao',
                Field('timu', db.timu, label='题目', writable=False),
                Field('zuozhe', db.auth_user, writable=False, widget=SQLFORM.widgets.string.widget, label='作者'),
                Field('shijian', 'datetime', label='时间', default=datetime.datetime.now(), writable=False),
                Field('yuyan', requires=IS_IN_SET(['pascal', 'c++']), label='语言'),
                Field('jietu', 'upload', label='截图', autodelete=True, requires=IS_NOT_EMPTY()),
                Field('wenjian', "upload", label='文件', autodelete=True, requires=IS_NOT_EMPTY()),
                Field('daima', 'text', requires=IS_NOT_EMPTY(), label='代码'),
                Field('tongguo', 'boolean', writable=False, default=False, label='通过审核'),
                format='%(timu)s-%(zuozhe)s')

db.define_table('jietibaogao',
                Field('timu', db.timu, label='题目'),
                Field('zuozhe', db.auth_user, writable=False, widget=SQLFORM.widgets.string.widget, label='作者'),
                Field('shijian', 'datetime', label='时间', default=datetime.datetime.now(), writable=False),
                Field('neirong', 'text', requires=IS_NOT_EMPTY(), label='内容摘要'),
                Field('wenjian', "upload", label='附件', autodelete=True),
                Field('jifen', 'integer', default=0, label='积分', writable=False),
                format='%(timu)s-%(zuozhe)s')

db.define_table('jiajianfen',
                Field('zuozhe', db.auth_user, label='用户'),
                Field('fenzhi', 'integer', label='分值'),
                Field('shijian', 'date', label='时间', default=datetime.date.today(), writable=False),
                Field('beizhu', label='备注'))

db.define_table('zuoye',
                Field('title', label='标题'),
                Field('qingtong', db.timu, label='青铜'),
                Field('baiying', db.timu, label='白银'),
                Field('huangjing', db.timu, label='黄金'))

db.define_table('pinglun',
                Field('timu', db.timu, label='题目', writable=False),
                Field('zuozhe', db.auth_user, writable=False, widget=SQLFORM.widgets.string.widget, label='作者'),
                Field('shijian', 'datetime', label='时间', default=datetime.datetime.now(), writable=False),
                Field('jietu', 'upload', label='图片（可选）', autodelete=True, requires=IS_NULL_OR(IS_IMAGE())),
                Field('neirong', 'text', requires=IS_NOT_EMPTY(), label='内容'),
                format='%(timu)s-%(zuozhe)s')
















