import xadmin

from .models import EmailVerifyRecord,Banner


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fileds = ['code','email','send_type','send_time']
    list_filter = ['code','email','send_type','send_time']   # 过滤功能

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fileds = ['title', 'image', 'url', 'index','add_time']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)