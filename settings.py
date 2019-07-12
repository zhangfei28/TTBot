
URL_HOST = 'https://www.toutiao.com'
URL_USER_HOME = URL_HOST + '/c/user/{id}/'
URL_USER_RELATION = URL_HOST +'/c/user/relation/{id}/'
URL_ARTICLE_ITEM = 'https://www.toutiao.com/a{item_id}/'
URL_LOGIN_HOME = 'https://sso.toutiao.com/'
URL_SEARCH_TEST = 'https://www.toutiao.com/search/?keyword='
URL_TTH = 'https://mp.toutiao.com/profile_v3/index'
URL_TTH_COMMENTS = 'https://mp.toutiao.com/profile_v3/weitoutiao/comment'
URL_PGC_IMG_PREFIX = 'https://p3.pstatp.com/list/'
URL_WENDA = 'https://www.wukong.com/user/?type=1'

#API
#GET
API_NEWS_FEED = 'https://www.toutiao.com/api/pc/feed/'
API_USER_ARTICLE = 'https://www.toutiao.com/c/user/article/'
API_USER_WEITT = 'https://www.toutiao.com/api/pc/feed/'
API_USER_FOLLOWING = 'https://www.toutiao.com/c/user/following/'
API_USER_FANS = 'https://www.toutiao.com/c/user/followed/'
API_COMMENT_LIST = 'https://www.toutiao.com/api/comment/list/'
#LOGINED
API_USER_FAVOURITE = 'https://www.toutiao.com/c/user/favourite/'
API_UNFOLLOW = 'https://www.toutiao.com/c/user/unfollow/'
API_FOLLOW = 'https://www.toutiao.com/c/user/follow/'
API_FANS_TREND = 'http://mp.toutiao.com/statistic/audience/count/trend/'
API_NOTY_COUNT  = 'http://mp.toutiao.com/comment/notification_count/'
API_INVITE_COUNT = 'http://mp.toutiao.com/wenda/invite/count/'
API_UNREAD_IMPORTANT_NOTY = 'http://mp.toutiao.com/notification/get_unread_important_notification'
API_UNREAD_MSG = 'http://mp.toutiao.com/delivers/mp/messages/unread/'
API_UNREAD_MSG_INFO = 'https://mp.toutiao.com/api/msg/v1/unread/?from=pgc_notify'
API_UNREAD_FANS_COUNT = 'https://mp.toutiao.com/notification/get_unread_fans_count/'
API_ACCOUNT_EDIT_INFO = 'http://mp.toutiao.com/edit_media_account/?output=json'
API_MEDIA_INFO = 'http://mp.toutiao.com/get_media_info/'
API_BLOCKING_USER_LIST = 'http://mp.toutiao.com/im/get_blocking_users/'
API_LOGIN_OP_LOG = 'http://mp.toutiao.com/passport/safe/login_op_log/'
API_SENSITIVE_OP_LOG = 'https://mp.toutiao.com/passport/safe/sensitive_op_log/'
API_CONTENT_OVERVIEW = 'http://mp.toutiao.com/statistic/content_overview/'
API_CONTENT_DISPLAY_DAILY_STATUS = 'http://mp.toutiao.com/statistic/content_daily_stat/'#?start_date=2019-06-25&end_date=2019-06-25&pagenum=1'
API_CONTENT_ARTICLE_STATUS = 'http://mp.toutiao.com/statistic/content_article_stat/'
API_SEARCH = 'https://www.toutiao.com/api/search/content/'
API_COMMENTS = 'https://mp.toutiao.com/comment/'#?cursor=0&feature=wtt'
API_USER_COMMENTS = 'https://mp.toutiao.com/thread/get_thread_list'
API_WEITT_LIST = 'https://mp.toutiao.com/comment'
API_VEDIO_LIST = 'https://mp.toutiao.com/api/feed/profile/v1/'#?count=20&category=ugc_video_mine&offset=0'
API_SUBSCRIBERS = 'https://mp.toutiao.com/statistic/subscriber_list/0'#?cursor=0&hasmore=true&pagesize=28'
API_INTERACT_USERS = 'https://mp.toutiao.com/statistic/audience/interaction/'#?page=1&size=15'
API_ACCOUNT_STATUS = 'https://mp.toutiao.com/statistic/profile_stat/'
API_ARTICLE_COMMENTS = 'https://mp.toutiao.com/comment/article_detail_comment/'
API_DELETE_VIDEO = 'https://mp.toutiao.com/ugc/publish/video/v1/delete/'
API_INVITE_USER_LIST = 'https://www.wukong.com/wenda/web/invite/userlist/'#?qid=6708204462206353675&rn=1561954531069
API_WENDA_DRAFT = 'https://www.wukong.com/wenda/web/draft/list/brow/'#?cursor=1561955403011'
API_WENDA_QUESTIONS = 'https://www.wukong.com/wenda/web/myquestion/brow/'#?count=15&t=1561955515454&offset=0&other_uid=95480041731'
API_WENDA_ANALYSIS = 'https://mp.toutiao.com/statistic/media_total_stats/'
API_SMALL_VIDEO_ANALYSIS = 'https://mp.toutiao.com/ugc/video/v1/user/data_analysis/'
API_FANS_PROPERTY = 'http://mp.toutiao.com/statistic/audience_property/'
API_ARTICLE_LIST = 'https://mp.toutiao.com/pgc/mp/core/article/list'
API_STORE_RESOURCES = 'https://mp.toutiao.com/article/get_storage_resource/'
API_ARTICLE_TITLE_CHECK = 'https://mp.toutiao.com/check_title/'
API_ARTICLE_EXTERN_LINK_CHECK = 'https://mp.toutiao.com/article/check_extern_link/'

#POST
API_REPORT = 'https://verify.snssdk.com/report'
#LOGINED
API_IMAGE_UPLOAD = 'https://www.toutiao.com/c/ugc/image/upload/'
API_PUBLISH = 'https://www.toutiao.com/c/ugc/content/publish/'
API_ASK_QUESTION = 'https://www.toutiao.com/wenda/web/commit/postquestion/'
API_DELETE_QUESTION = 'https://www.wukong.com/wenda/web/commit/deletequestion/'
API_DELETE = 'https://www.toutiao.com/c/ugc/content/delete/'
API_POST_COMMENT = 'https://www.toutiao.com/api/comment/post_comment/'
API_POST_REPLY = 'https://www.toutiao.com/api/comment/post_reply/'
API_STORE_MEDIA = 'https://www.toutiao.com/group/repin/'
API_UNSTORE_MEDIA = 'https://www.toutiao.com/group/unrepin/'
API_UNBLOCK_USER = 'http://mp.toutiao.com/im/user_block/'
API_REPOST = 'https://www.toutiao.com/c/ugc/content/repost/'
API_DIGG_COMMENT = 'https://mp.toutiao.com/comment/digg/'
API_ARTICLE_POST = 'https://mp.toutiao.com/core/article/edit_article_post/?source=mp&type=article'
API_CANCEL_DIGG_COMMENT = 'https://mp.toutiao.com/comment/cancel_digg/'
API_ARTICLE_IMAGE_UPLOAD = 'https://mp.toutiao.com/micro/image/upload'
API_IMG_QRCODE_CHECK = 'https://mp.toutiao.com/article/check_qrcode/'
API_ARTICLE_IMG_CHECK = 'https://mp.toutiao.com/micro/image/check'
API_ARTICLE_DELETE = 'https://mp.toutiao.com/delete_article/'
API_QUESTION_FOLLOW = 'https://www.wukong.com/wenda/web/commit/followquestion/'
API_INVITE_USER_ANSWER ='https://www.wukong.com/wenda/web/commit/postinvite/'#?to_uid=101969759790&qid=6708204462206353675'
API_POST_ANSWER = 'https://www.wukong.com/wenda/web/commit/postanswer/?source=question_click_write_answer'#answer_detail_write_answer
API_DELETE_ANSWER = 'https://www.wukong.com/wenda/web/commit/deleteanswer/'
API_DIGG_ANSWER = 'https://www.wukong.com/wenda/web/commit/digg/'
API_BURY_ANSWER = 'https://www.wukong.com/wenda/web/commit/bury/'
API_BAN_ANSWER_COMMENT = 'https://www.wukong.com/wenda/web/commit/opanswercomment/'
API_DELETE_WENDA_DT = 'https://www.wukong.com/wenda/web/commit/deletedongtai/'#qid: 6708204462206353675
API_DELETE_WENDA_DRAFT = 'https://www.wukong.com/wenda/web/commit/deletedraft/'#qid: 6708204462206353675
API_RESOURCE_IMG_UPLOAD = 'https://mp.toutiao.com/tools/upload_picture/?type=ueditor&pgc_watermark=1&action=uploadimage&encode=utf-8'
API_CHANGE_RESOURCE_REF = 'https://mp.toutiao.com/article/change_media_resource_ref/'
API_CHANGE_RESOURCE_FLAGS = 'https://mp.toutiao.com/article/change_media_resource_flags/'
API_SET_ARTICLE_TOP = 'https://mp.toutiao.com/set_top_artcile/'
API_CANCEL_ARTCLE_TOP = 'https://mp.toutiao.com/cancel_top_article/'
API_HIDE_ARTICLE = 'https://mp.toutiao.com/hide_article/'
API_UNHIDE_ARTICLE = 'https://mp.toutiao.com/unhide_article/'
# API_DIGG_ARTICLE = 'https://mp.toutiao.com/content/digg/'


PATTERN_USERINFO = 'userInfo = (\{(?:.|\n)*?\});'
PATTERN_RELATION = "'statistics',(\{(?:.|\n)*?\})"
PATTERN_CRSFTOKEN = "'csrfmiddlewaretoken' value='(.+)'"

#调用今日头条生成tassesionIDcookie的JavaScript文件的路径以及解密方法
ts_js_path = './javascript/tasessionID.js'
ts_js_func = 'get_id'
#调用今日头条签名解密JavaScript文件的路径以及解密方法
signature_js_path = './javascript/signature.js'
signature_js_func = 'get_sign'
#调用今日头条as/cp解密JavaScript文件的路径以及解密方法
ascp_js_path = './javascript/ascp.js'
ascp_js_func = 'ascp'

# 滑块登陆 相关
USERNAME_ID = 'user-name'
PASSWORD_ID = 'password'
LOGIN_BTN_ID = 'bytedance-login-submit'
LOGIN_ICON_CLASS = 'login-type-icon'
VALIDATE_IMG_BIG_ID = 'validate-big'
VALIDATE_IMG_BLOCK_CLS = 'validate-block'
SLIDER_BTN_CLASS = 'drag-button'
UGC_CLASS = 'ugc-content'

# 用户爬取新闻文章微头条等的值设置
VIDEO = '0'
ARTICLE = '1'
WEITT = '2'
# 对应数据库
MODE_MAP = {
    '0':'video',
    '1':'article',
    '2':'weitt'
}
APIS = {
    'fans':API_USER_FANS,
    'followings':API_USER_FOLLOWING
}


# 作品 状态码
ARTICLE_STATUS = {
    'checking':6,
    'draft':1,
    'unpassed':0,
    'passed':3,
    'hide':11,
}
# 微头条请求参数
W_PARAMS = {
    'category': 'pc_profile_ugc',
    'utm_source': 'toutiao',
    'visit_user_id':'',
    'max_behot_time': '0'
}
# 用户 关注 粉丝 请求参数
F_PARAMS = {
    'user_id': '',
    'cursor': '0',   # 初始值0
    'count': '400',  # 极限值是410左右，默认值是20
    '_signature': '',
}

HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

HEADERS_USER_ARTICLE = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

HEADERS_F = {
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'accept-encoding': 'gzip, deflate, br',
    'content-type': 'application/x-www-form-urlencoded',
    'referer': URL_HOST,
    'origin':URL_HOST,
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

