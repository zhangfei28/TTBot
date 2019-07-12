#coding:utf-8

import os
import re
import time
import requests
import validators

from config import *
from settings import *
from copy import deepcopy
from util.jstool import signature_func
from util.tools import time_to_date
from util.account import articles_cleaner
from urllib3 import encode_multipart_formdata
from deco.crawl import crawl_helper
from deco.toutiao import check,login_required,action
from component.sliderlogin import SliderHelper
from component.user import TTUser
from component.dbhelper import Database
from component.log import getLogger
from util.account import params_for_favourite,\
    favourite_cleaner,videos_cleaner

logger = getLogger(__name__)

class TTAcount:

    def __init__(self):
        self.helper = SliderHelper()
        self.db = Database(MONGODB)
        self.session = requests.session()
        self.login_headers = None
        self._account_info = None
        self._media_info = None
        self._name = None
        self._id = None
        self._mid = None

    @check
    def login(self, username=USERNAME, password=PASSWORD):
        self.login_headers = self.helper.login(username=username,password=password)

    @property
    def user_info(self):
        if not self._account_info:
            self.get_account_info()
        return self._account_info

    @property
    def media_info(self):
        if not self._media_info:
            self.get_account_media_info()
        return self._media_info

    @property
    def name(self):
        self._name = self.user_info.get('name') if not self._name else self._name
        return self._name

    @property
    def user_id(self):
        self._id = str(self.user_info.get('creator_id')) if not self._id else self._id
        return self._id

    @property
    def media_id(self):
        self._mid = str(self.user_info.get('id')) if not self._mid else self._mid
        return self._mid

    @property
    @action('get',api=API_ACCOUNT_STATUS)
    @login_required
    def account_status(self):
        return {
            'params':None,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'获取当前登陆账户 {self.name}(ID:{self.user_id}) 状态信息 成功!',
                'fail': f'获取当前登陆账户 {self.name}(ID:{self.user_id}) 状态信息 失败.',
            }
        }

    @action('get', api=API_FOLLOW)
    @login_required
    def follow_user(self, uid):
        user = TTUser(uid)
        HEADERS_F.update({
            'referer': URL_USER_HOME.format(id=uid),
        })
        self.login_headers.update(HEADERS_F)
        return {
            'params': {
                'user_id': uid,
                '_signature': signature_func('', user.mediaId)
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'关注用户 {user.name}(ID:{user.id}) 成功!',
                'fail': f'关注用户 {user.name}(ID:{user.id}) 失败.',
            }
        }

    @action('get', api=API_UNFOLLOW)
    @login_required
    def unfollow_user(self, uid):
        user = TTUser(uid)
        HEADERS_F.update({
            'referer': URL_USER_HOME.format(id=uid),
        })
        self.login_headers.update(HEADERS_F)
        return {
            'params': {
                'user_id': uid,
                '_signature': signature_func('', user.mediaId)
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'取消关注用户 {user.name}(ID:{user.id}) 成功!',
                'fail': f'取消关注用户 {user.name}(ID:{user.id}) 失败.',
            }
        }

    @action('post', api=API_STORE_MEDIA)
    @login_required
    def store_media(self, item_id):
        csrftoken = re.findall("csrftoken=(.*)", self.login_headers['cookie'])[0]
        self.login_headers.update({
            'x-csrftoken': csrftoken,
        })
        self.login_headers.update(HEADERS_F)
        self.login_headers.update({
            'referer': URL_ARTICLE_ITEM.format(item_id=item_id)
        })
        return {
            'params': {
                'group_id': item_id,
                'item_id': item_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'收藏头条文章ID:{item_id} 成功!',
                'fail': f'收藏头条文章ID:{item_id} 失败.',
            }
        }

    @action('post', api=API_UNSTORE_MEDIA)
    @login_required
    def unstore_media(self, item_id):
        csrftoken = re.findall("csrftoken=(.*)", self.login_headers['cookie'])[0]
        self.login_headers.update({
            'x-csrftoken': csrftoken,
        })
        self.login_headers.update(HEADERS_F)
        self.login_headers.update({
            'referer': URL_ARTICLE_ITEM.format(item_id=item_id)
        })
        return {
            'params': {
                'group_id': item_id,
                'item_id': item_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'取消收藏头条文章ID:{item_id} 成功!',
                'fail': f'取消收藏头条文章ID:{item_id} 失败.',
            }
        }

    @action('post', api=API_UNBLOCK_USER)
    @login_required
    def block_user(self, uid):
        return {
            'params': {
                'action': 'block',
                'to_uid': uid,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'拉黑 用户(ID:{uid}) 成功!',
                'fail': f'拉黑 用户(ID:{uid}) 失败.',
            },
        }

    @action('post', api=API_UNBLOCK_USER)
    @login_required
    def unblock_user(self, uid):
        return {
            'params': {
                'action': 'cancelblock',
                'to_uid': uid,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'黑名单中移出用户(ID:{uid}) 成功!',
                'fail': f'黑名单中移出用户(ID:{uid}) 失败.',
            },
        }

    @action('post', api=API_DIGG_COMMENT)
    @login_required
    def like_comment(self, comment_id):
        return {
            'params': {
                'cursor': f'{int(time.time())}',
                'user_id': self.user_id,
                'comment_id': comment_id,
                'type': '1'
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'点赞评论(ID:{comment_id}) 成功!',
                'fail': f'点赞评论(ID:{comment_id}) 失败.',
            },
        }

    @action('post', api=API_CANCEL_DIGG_COMMENT)
    @login_required
    def unlike_comment(self, comment_id):
        return {
            'params': {
                'cursor': f'{int(time.time())}',
                'user_id': self.user_id,
                'comment_id': comment_id,
                'type': '1'
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'取消点赞评论(ID:{comment_id}) 成功!',
                'fail': f'取消点赞评论(ID:{comment_id}) 失败.',
            },
        }

    @action('post', api=API_SET_ARTICLE_TOP)
    @login_required
    def set_top_article(self, item_id, create_time, article_type=0, group_source=2):
        return {
            'params': {
                'item_id': item_id,
                'pgc_id': item_id,
                'id': item_id,
                'article_type': article_type,
                'group_id': item_id,
                'source_type': 0,
                'has_article_pgc': 1,
                'book_id': '',
                'create_time': create_time,
                'group_source': group_source
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'置顶图文作品(ID:{item_id}) 成功!',
                'fail': f'置顶图文作品(ID:{item_id}) 失败.',
            },
        }

    @action('post', api=API_CANCEL_ARTCLE_TOP)
    @login_required
    def cancel_top_article(self, item_id, create_time, article_type=0, group_source=2):
        return {
            'params': {
                'item_id': item_id,
                'pgc_id': item_id,
                'id': item_id,
                'article_type': article_type,
                'group_id': item_id,
                'source_type': 0,
                'has_article_pgc': 1,
                'book_id': '',
                'create_time': create_time,
                'group_source': group_source
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'取消置顶图文作品(ID:{item_id}) 成功!',
                'fail': f'取消置顶图文作品(ID:{item_id}) 失败.',
            },
        }

    @action('post', api=API_HIDE_ARTICLE)
    @login_required
    def hide_article(self, item_id, create_time='', article_type=0, group_source=2):
        return {
            'params': {
                'item_id': item_id,
                'pgc_id': item_id,
                'id': item_id,
                'article_type': article_type,
                'group_id': item_id,
                'source_type': 0,
                'has_article_pgc': 1,
                'book_id': '',
                'create_time': create_time,
                'group_source': group_source
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'从主页撤回图文作品(ID:{item_id}) 成功!',
                'fail': f'从主页撤回图文作品(ID:{item_id}) 失败.',
            },
        }

    @action('post', api=API_UNHIDE_ARTICLE)
    @login_required
    def unhide_article(self, item_id, create_time='', article_type=0, group_source=2):
        return {
            'params': {
                'item_id': item_id,
                'pgc_id': item_id,
                'id': item_id,
                'article_type': article_type,
                'group_id': item_id,
                'source_type': 0,
                'has_article_pgc': 1,
                'book_id': '',
                'create_time': create_time,
                'group_source': group_source
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'恢复到主页 图文作品(ID:{item_id}) 成功!',
                'fail': f'恢复到主页 图文作品(ID:{item_id}) 失败.',
            },
        }

    def star_resource_img(self, web_uri):
        return self.change_media_resource_ref(web_uri, opt='save',
                                              saved=True, api=API_CHANGE_RESOURCE_FLAGS)

    def unstar_resource_img(self, web_uri):
        return self.change_media_resource_ref(web_uri, opt='unsave',
                                              saved=0, api=API_CHANGE_RESOURCE_FLAGS)

    @action('post', api=API_PUBLISH)
    @login_required
    def post_weitt(self, content, image=None):
        image_uris = []
        web_uri = ''
        if isinstance(image, list):
            for i in image:
                json_res = self.upload_image(i)
                uri = json_res.get('data')['web_uri']
                image_uris.append(uri)
                web_uri = ','.join(image_uris)
        elif image:
            res = self.upload_image(image)
            web_uri = res.get('data')['web_uri']
        csrftoken = re.findall("csrftoken=(.*)", self.login_headers['cookie'])[0]
        self.login_headers.update({
            'x-csrftoken': csrftoken,
        })
        self.login_headers.update(HEADERS_F)
        return {
            'params': {
                'content': content,
                'image_uris': web_uri,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'发布微头条内容成功!',
                'fail': f'发布微头条内容失败.',
            }
        }

    @action('post', api=API_ARTICLE_POST)
    @login_required
    def post_article(self, title, content, extern_link=None,
                     timer_time=None, run_ad=True,
                     writting_race_mode=0, cover_img=None):
        """
        :param title: 图文作品 标题
        :param content: 图文作品 内容
        :param extern_link: 扩展链接
        :param timer_time: 定时发布的时间
        :param run_ad: 是否投放头条广告
        :param writting_race_mode: 参加 新写作大赛 的模式： 0:不参加 1:参加主竞赛单元评选 2:参加青年竞赛单元评选
        :param cover_img: 封面图，可以是图片网络地址 或是 本地图片路径
        """
        _time = time_to_date(time.time() + 3600) if not timer_time else timer_time
        cover = {}
        if validators.url(cover_img):
            res = self.upload_resource_img_by_url(cover_img)
        elif os.path.isfile(cover_img):
            res = self.upload_resource_img_by_open(cover_img)
        else:
            res = {}
        if res:
            width = res.get('width')
            height = res.get('height')
            cover = {
                "id": 1,
                "url": URL_PGC_IMG_PREFIX + res.get('web_uri'),
                "uri": res.get('web_uri'),
                "origin_uri": res.get('original'),
                "ic_uri": "",
                "thumb_width": f'{width}',
                "thumb_height": f'{height}'
            }
        _cover = '[{"id":2,"url":"' + cover['url'] + '","uri":"' + cover['uri'] + \
                 '","origin_uri":"' + cover['origin_uri'] + \
                 '","ic_uri":"","thumb_width":' + cover['thumb_width'] + \
                 ',"thumb_height":' + cover['thumb_height'] + '}]' if cover else '[]'
        params = {
            'article_type': 0,
            'title': title,
            'content': content,
            'activity_tag': 0,
            'title_id': f'{int(time.time()*1000)}_{self.media_id}',
            'claim_origin': 0,
            'article_ad_type': [2, 3][run_ad],
            'add_third_title': 0,
            'recommend_auto_analyse': 0,
            'tag': '',
            'article_label': '',
            'is_fans_article': 0,
            'quote_hot_spot': 0,
            'govern_forward': 0,
            'push_status': 0,
            'push_android_title': '',
            'push_android_summary': '',
            'push_ios_summary': '',
            'timer_status': [0, 1][bool(timer_time)],
            'timer_time': _time,
            'praise': 0,
            'community_sync': 0,
            'column_chosen': 0,
            'pgc_id': 0,
            'qy_self_recommendation': 0,
            'pgc_feed_covers': _cover,
            'from_diagnosis': 0,
            'origin_debut_check_pgc_normal': 0,
            'tree_plan_article': 0,
            'save': 1,
        }
        if writting_race_mode:
            params.update({
                'writing_race_compose': writting_race_mode
            })
        if extern_link:
            params.update({
                'extern_link': ['', extern_link][bool(extern_link)],
            })
        return {
            'params': params,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'code': 0,
            },
            'tips': {
                'ok': f'发布 头条号 图文作品《{title}》成功!',
                'fail': f'发布 头条号 图文作品《{title}》失败.',
            }
        }

    @action('post', api=API_POST_COMMENT)
    @login_required
    def post_comment(self, txt, group_id):
        csrftoken = re.findall("csrftoken=(.*)", self.login_headers['cookie'])[0]
        self.login_headers.update({
            'x-csrftoken': csrftoken,
        })
        self.login_headers.update(HEADERS_F)
        self.login_headers.update({
            'referer': URL_ARTICLE_ITEM.format(item_id=group_id)
        })
        return {
            'params': {
                'status': txt,
                'content': txt,
                'group_id': group_id,
                'item_id': group_id,
                'id': '0',
                'format': 'json',
                'aid': '24',
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'评论头条文章ID:{group_id} 成功!',
                'fail': f'评论头条文章ID:{group_id} 失败.',
            }
        }

    @action('post', api=API_POST_REPLY)
    @login_required
    def post_reply(self, txt, group_id, comment_id, reply_to_user_id, reply_id='0'):
        csrftoken = re.findall("csrftoken=(.*)", self.login_headers['cookie'])[0]
        self.login_headers.update({
            'x-csrftoken': csrftoken,
        })
        self.login_headers.update(HEADERS_F)
        self.login_headers.update({
            'referer': URL_ARTICLE_ITEM.format(item_id=group_id)
        })
        return {
            'params': {
                'content': txt,
                'group_id': group_id,
                'item_id': group_id,
                'reply_id': reply_id,
                'comment_id': comment_id,
                'reply_to_user_id': reply_to_user_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'评论头条文章(ID:{group_id}) 评论ID:{comment_id} 成功!',
                'fail': f'评论头条文章(ID:{group_id}) 评论ID:{comment_id} 失败.',
            }
        }

    @action('post', api=API_ASK_QUESTION)
    @login_required
    def post_question(self, title, content='', image=None):
        if len(title) < 4:
            logger.warning(f'问答标题必须在4-40字范围.')
            return
        image_uris = []
        if isinstance(image, list):
            for i in image:
                json_res = self.upload_image(i)
                uri = json_res.get('data')['web_uri']
                image_uris.append(uri)
        elif image:
            res = self.upload_image(image)
            web_uri = res.get('data')['web_uri']
            image_uris.append(web_uri)
        self.login_headers.update(HEADERS_F)
        _ = {
            'params': {
                'title': title,
                'content': content,
                't': f'{int(time.time()*1000)}',
                'enter_from': 'direct_toutiao',
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'err_no': 0,
            },
            'tips': {
                'ok': f'发布悟空问答 “{title}” 成功!',
                'fail': f'发布悟空问答 “{title}” 失败.',
            }
        }
        if image_uris:
            _['params'].update({
                'pic_list[]': image_uris
            })
        return _

    @action('post', api=API_REPOST)
    @login_required
    def repost(self, txt, item_id, uid):
        return {
            'params': {
                'content': txt,
                'cover_url': '',
                'fw_id': item_id,
                'fw_id_type': 4,
                'fw_user_id': uid,
                'opt_id': item_id,
                'opt_id_type': 4,
                'repost_to_comment': 1,
                'repost_type': 211,
                'title': '',
                'group_id': item_id,
                'item_id': item_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'转发 头条文章ID:{item_id} 成功!',
                'fail': f'转发 头条文章ID:{item_id} 失败.',
            }
        }

    @action('post', api=API_DELETE)
    @login_required
    def delete_media(self, group_id, comment=False):
        csrftoken = re.findall("csrftoken=(.*)", self.login_headers['cookie'])[0]
        self.login_headers.update({
            'x-csrftoken': csrftoken,
        })
        self.login_headers.update(HEADERS_F)
        key = 'thread_id' if not comment else 'comment_id'
        return {
            'params': {
                key: group_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'删除 ID:{group_id} 头条media 成功!',
                'fail': f'删除 ID:{group_id} 头条media 失败.',
            }
        }

    @action('post', api=API_ARTICLE_DELETE)
    @login_required
    def delete_article(self, item_id, create_time='', article_type=0, group_source=2):
        return {
            'params': {
                'item_id': item_id,
                'pgc_id': item_id,
                'id': item_id,
                'article_type': article_type,
                'group_id': item_id,
                'source_type': 0,
                'book_id': '',
                'create_time': create_time,
                'group_source': group_source
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'删除图文作品(ID:{item_id}) 成功!',
                'fail': f'删除图文作品(ID:{item_id}) 失败.',
            },
        }

    def delete_articles(self, status='unpassed', keyword=None, start_date=None, end_date=None, save=False):
        """
        :param status: 需要删除的作品的 当前状态,可以是'checking','passed','unpassed','draft','hide'之一
        :param keyword: 作品关键词
        :param start_date: 搜索开始日期
        :param end_date: 搜索结束日期
        """
        _status = status

        def callback(self, item):
            item_id = item.get('item_id', 0)
            ct = item.get('create_time', 0)
            status_code = item.get('status')
            if status_code == ARTICLE_STATUS[status]:
                self.delete_article(item_id, create_time=ct)
                return True

        if status == 'checking':
            _status = 'all'

        self.get_posted_articles(MDB=save, status=_status, item_callback=callback, keyword=keyword,
                                 start_date=start_date, end_date=end_date)

    @action('get', api=API_DELETE_VIDEO)
    @login_required
    def delete_video(self, item_id):
        return {
            'params': {
                'item_id': item_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'删除小视频(ID:{item_id}) 成功!',
                'fail': f'删除小视频(ID:{item_id}) 失败.',
            },
        }

    @action('post', api=API_DELETE_WENDA_DRAFT)
    @login_required
    def delete_wenda_draft(self, question_id):
        return {
            'params': {
                'qid': question_id,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'err_no': 0,
            },
            'tips': {
                'ok': f'删除悟空问答 问题草稿 (ID:{question_id}) 成功!',
                'fail': f'删除悟空问答 问题草稿 (ID:{question_id}) 失败.',
            },
        }

    @action('post',api=API_DELETE_QUESTION)
    @login_required
    def delete_question(self,qid):
        return {
            'params':{
                'qid':qid,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'err_no': 0,
            },
            'tips': {
                'ok': f'删除悟空问答 问题(ID:{qid}) 成功!',
                'fail': f'删除悟空问答 问题(ID:{qid}) 失败.',
            },
        }

    def delete_resource_img(self,web_uri):
        return self.change_media_resource_ref(web_uri,opt='delete')

    def get_followings(self,count=COUNT_FOLLOWING,MDB=None,ALL=False):
        me = TTUser(self.user_id)
        return me.get_followings(count=count,MDB=MDB,ALL=ALL)

    def get_fans(self,count=COUNT_FANS,MDB=None,ALL=False):
        me = TTUser(self.user_id)
        return me.get_fans(count=count,MDB=MDB,ALL=ALL)

    @action('get',api=API_COMMENT_LIST)
    def get_comments_of_media(self,item_id,offset=0,count=10):
        return {
            'params':{
                'item_id':item_id,
                'group_id':item_id,
                'offset':offset,
                'count':count
            },
            'extra_kwargs': {
                'headers': HEADERS,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'获取头条媒体 (ID:{item_id}) 可见评论 成功!',
                'fail': f'获取头条媒体 (ID:{item_id}) 可见评论失败.',
            },
        }

    @action('get', api=API_MEDIA_INFO)
    @login_required
    def get_account_media_info(self):

        def callback(self, response):
            self._media_info = response.get('data')['media']
            return response

        return {
            'params': None,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'获取 当前账户 media 信息成功!',
                'fail': f'获取 当前账户 media 信息失败.',
            },
            'callback':callback,
        }

    @action('get', api=API_ACCOUNT_EDIT_INFO)
    @login_required
    def get_account_info(self):

        def callback(self, response):
            self._account_info = response.get('media')
            bind_mobile = response.get('bind_mobile')
            dot_name = response.get('dot_name')
            location_name = response.get('location_name')
            self._account_info.update({
                'location_name': location_name,
                'dot_name': dot_name,
                'bind_mobile': bind_mobile
            })
            return response

        return {
            'params': {'output': 'json'},
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'check_func': lambda x: x.get('media'),
            'tips': {
                'ok': '获取 当前账户信息成功!',
                'fail': '获取 当前账户信息失败.',
            },
            'callback': callback,
        }

    @action('get',api=API_NOTY_COUNT)
    @login_required
    def get_notification_count(self):

        def callback(self,response):
            data = response.get('data')
            return data

        return {
            'params':None,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message':'success'
            },
            'tips': {
                'ok': '获取 当前账户通知消息 成功!',
                'fail': '获取 当前账户通知消息 失败.',
            },
            'callback': callback,
        }

    @action('get',api=API_BLOCKING_USER_LIST)
    @login_required
    def get_blocking_users(self):

        def callback(self,response):
            data = response.get('data')
            return data

        return {
            'params':None,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message':'success'
            },
            'tips': {
                'ok': '获取 当前账户 黑名单 成功!',
                'fail': '获取 当前账户 黑名单 失败.',
            },
            'callback': callback,
        }

    @action('get',api=API_UNREAD_MSG_INFO)
    @login_required
    def get_unread_msg(self):
        return {
            'params':None,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'error_code': 0
            },
            'tips': {
                'ok': f'头条 推送未读消息(通知)获取 成功!',
                'fail': f'头条 推送未读消息(通知)获取 失败.',
            },
        }

    @action('get',api=API_UNREAD_FANS_COUNT)
    @login_required
    def get_unread_fans_count(self):
        return {
            'params': None,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'账户 新的粉丝数 获取 成功!',
                'fail': f'账户 新的粉丝数 获取 失败.',
            },
        }

    @action('get',api=API_INVITE_COUNT)
    @login_required
    def get_wenda_invited_count(self):
        check_func = lambda x: isinstance(x.get('invite_count'),int)
        return {
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'tips': {
                'ok': f'悟空问答邀请回答数获取 成功!',
                'fail': f'悟空问答邀请回答数获取 失败.',
            },
            'check_func':check_func
        }

    @action('get',api=API_FANS_TREND)
    @login_required
    def get_fans_trend(self,start_date,end_date):
        return {
            'params':{
                'start_date':start_date,
                'end_date':end_date,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'日期：{start_date} 至 {end_date} 粉丝趋势获取 成功!',
                'fail': f'日期：{start_date} 至 {end_date} 粉丝趋势获取 失败.',
            },
        }

    @action('get',api=API_CONTENT_OVERVIEW)
    @login_required
    def get_content_overview(self,start_date,end_date):
        return {
               'params': {
                   'start_date': start_date,
                   'end_date': end_date,
               },
               'extra_kwargs': {
                   'headers': self.login_headers,
                   'JSON': 1,
               },
               'msg': {
                   'message': 'success'
               },
               'tips': {
                   'ok': f'日期：{start_date} 至 {end_date} 发布数据分析信息获取 成功!',
                   'fail': f'日期：{start_date} 至 {end_date} 发布数据分析信息获取 失败.',
               },
        }

    @crawl_helper('get',api=API_SUBSCRIBERS)
    @login_required
    def get_subscribers(self,ALL=True,MDB=None,count=COUNT_FANS):
        return {
            'params_func':lambda x,y:{'cursor':x,'has_more':y,'pagesize':28},
            'var':{
                'cursor': 0,
                'hasmore':'true',
            },
            'var_outer':'data',
            'more':'hasmore',
            'more_out':'data',
            'item_out':'subscriber_info',
            'db_setup':{
                'tname': f'{self.name+"_"+self.user_id}',
                'db':MONGODB['subscribers'],
                'ticket':'user_id',
            },
            'request_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            }
        }

    @crawl_helper('get',api=API_USER_FAVOURITE)
    @login_required
    def get_favourites(self,ALL=True,MDB=None,count=COUNT_FAVOURITES):
        headers = deepcopy(self.login_headers)
        headers.update(HEADERS)
        return {
            'params_func': params_for_favourite ,
            'var': {
                'max_repin_time': 0,
            },
            'extra_args': {
                'uid': self.user_id,
            },
            'more': 'has_more',
            'db_setup': {
                'tname': f'{self.name+"_"+self.user_id}',
                'db': MONGODB['favourite'],
                'ticket': 'item_id',
            },
            'request_kwargs': {
                'headers': headers,
                'JSON': 1,
            },
            'cleaner':favourite_cleaner
        }

    @crawl_helper('get',api=API_USER_COMMENTS)
    @login_required
    def get_posts(self,ALL=True,MDB=None,count=COUNT_POSTS):
        headers = deepcopy(self.login_headers)
        headers.update(HEADERS)
        return {
            'params_func': lambda x,y:{'max_time':x,'has_more':y,'count':20},
            'var': {
                'max_time': int(time.time()),
                'has_more': True,
            },
            'more': 'has_more',
            'more_out':'data',
            'var_outer':'data',
            'item_out':'thread_list',
            'db_setup': {
                'tname': f'{self.name+"_"+self.user_id+"_"+time_to_date(time.time(),format="%Y-%m-%d")}',
                'db': MONGODB['comments'],
                'ticket': 'comment_id',
            },
            'request_kwargs': {
                'headers': headers,
                'JSON': 1,
            },
        }

    @crawl_helper('get',api=API_VEDIO_LIST)
    @login_required
    def get_videos(self,ALL=True,MDB=None,count=COUNT_VIDEOS):
        headers = deepcopy(self.login_headers)
        headers.update(HEADERS)
        return {
            'params_func': lambda x:{'offset':x,'category':'ugc_video_mine','count':20},
            'var': {
                'offset': 0,
            },
            'more': 'has_more',
            'db_setup': {
                'tname': f'{self.name+"_"+self.user_id}',
                'db': MONGODB['my_videos'],
                'ticket': 'id',
            },
            'request_kwargs': {
                'headers': headers,
                'JSON': 1,
            },
            'cleaner':videos_cleaner
        }

    @crawl_helper('get',api=API_ARTICLE_LIST)
    @login_required
    def get_posted_articles(self,ALL=True,MDB=None,count=COUNT_ARTICLES,
                            status='all',size=10,start_date=None,end_date=None,
                            keyword=None,item_callback=None):
        """
        :param ALL: 是否全部抓取
        :param MDB: 存储的数据实例
        :param count: 最多的抓取条数限制
        :param status: 可以是'all','passed','unpassed','draft','hide'之一，过滤条件
        :param size: 每一页显示的条数
        :param start_date: 开始抓取日期,如：'2019-07-01'
        :param end_date: 结束抓取日期,如：'2019-07-01'
        :param item_callback: 对单条数据的回调处理函数，返回：
            None表示处理完后继续执行后续代码；
            1表示处理完后忽略后续处理代码；
            元组(item,200)表示用item替换原先的单条数据再继续后续代码处理
        :param keyword: 过滤的关键词
        """
        headers = deepcopy(self.login_headers)
        headers.update(HEADERS)

        start_time = int(time.mktime(time.strptime(start_date,"%Y-%m-%d"))) if start_date else  0
        end_time = int(time.mktime(time.strptime(end_date, "%Y-%m-%d"))) if end_date else  0
        keyword = keyword if keyword else ''

        return {
            'params_func': lambda x:{
                'size':size,
                'status':status,
                'from_time':0,
                'start_time':start_time,
                'end_time':end_time,
                'feature': 0,
                'search_word':keyword,
                'source': 'all',
                'page':int(x)+1,
            },
            'var': {
                'page': 0,
            },
            'item_callback':item_callback,
            'var_outer':'data',
            'item_out':'content',
            'more': 'message',
            'db_setup': {
                'tname': f'{self.name+"_"+self.user_id+"_"+time_to_date(time.time(),format="%Y-%m-%d")}',
                'db': MONGODB['my_articles'],
                'ticket': 'id',
            },
            'request_kwargs': {
                'headers': headers,
                'JSON': 1,
            },
            'cleaner':articles_cleaner
        }

    @crawl_helper('get',api=API_WENDA_DRAFT)
    @login_required
    def get_wenda_drafts(self,ALL=True,MDB=None,count=COUNT_ARTICLES):

        def item_callback(self,item):
            qid = None
            draft = item.get('draft')
            if draft:
                qid = draft.get('qid')
            item['qid'] = qid
            return (item,200)

        return {
            'params_func':lambda x:{
                'cursor':x
            },
            'var':{
                'cursor':int(time.time()*1000)
            },
            'item_out': 'draft_question_list',
            'data_wrap':False,
            'db_setup': {
                'tname': f'{self.name+"_"+self.user_id+"_"+time_to_date(time.time(),format="%Y-%m-%d")}',
                'db': MONGODB['wenda_draft'],
                'ticket': 'qid',
            },
            'request_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'item_callback': item_callback,
        }

    @action('get',api=API_INTERACT_USERS)
    @login_required
    def get_interact_fans(self,page=1):
        return {
            'params':{
                'page':page,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'获取当前登陆用户 粉丝互动排行榜 第{page}页 成功!',
                'fail': f'获取当前登陆用户 粉丝互动排行榜 第{page}页 失败.',
            },
        }

    @action('get',api=API_STORE_RESOURCES)
    @login_required
    def get_resource_images(self,page=1,pagesize=20,saved=False):
        tip = f'已收藏' if saved else f'全部'
        return {
            'params':{
                'resource_type': 3,
                'page_index': page,
                'page_size': pagesize,
                'is_saved': [0, 1][bool(saved)]
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'素材库图片资源列表({tip}) 第{page}页 获取 成功!',
                'fail': f'素材库图片资源列表获取({tip}) 第{page}页 失败.',
            },
        }

    @action('get',api=API_LOGIN_OP_LOG)
    @login_required
    def get_login_op_log(self,page=1,pagesize=20):
        return {
            'params':{
                'aid': 24,
                'account_sdk_source': 'web',
                'pageSize': pagesize,
                'pageNow': page,
                'month': 12,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'获取当前登陆用户 登陆记录 第{page}页 成功!',
                'fail': f'获取当前登陆用户 登陆记录 第{page}页 失败.',
            },

        }

    @action('get', api=API_SENSITIVE_OP_LOG)
    @login_required
    def get_sensitive_op_log(self, page=1, pagesize=20):
        return {
            'params': {
                'aid': 24,
                'account_sdk_source': 'web',
                'pageSize': pagesize,
                'pageNow': page,
                'month': 12,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success'
            },
            'tips': {
                'ok': f'获取当前登陆用户 敏感操作记录 第{page}页 成功!',
                'fail': f'获取当前登陆用户 敏感操作记录 第{page}页 失败.',
            },

        }

    @action('post',api=API_RESOURCE_IMG_UPLOAD)
    @login_required
    def upload_resource_img_by_open(self,image_path,key='upfile'):

        def callback(self,response):
            web_uri = response.get('web_uri')
            self.change_media_resource_ref(web_uri)
            return response

        data = {}
        header = deepcopy(HEADERS)
        data[key] = (image_path.rsplit(os.sep)[-1], open(image_path, 'rb').read())
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header['content-type'] = encode_data[1]
        self.login_headers.update(header)
        return {
            'params': data,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'上传图片至素材库 {image_path} 成功!',
                'fail': f'上传图片至素材库 {image_path} 失败.',
            },
            'callback':callback,
        }

    @action('post',api=API_RESOURCE_IMG_UPLOAD)
    @login_required
    def upload_resource_img_by_url(self,pic_url):

        def callback(self,response):
            web_uri = response.get('web_uri')
            self.change_media_resource_ref(web_uri)
            return response

        path = f'pic_url={pic_url}'
        url = '&'.join([API_RESOURCE_IMG_UPLOAD,path])
        return {
            'params':None,
            'api':url,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'上传图片至素材库 {pic_url} 成功!',
                'fail': f'上传图片至素材库 {pic_url} 失败.',
            },
            'callback':callback
        }

    @action('post', api=API_IMAGE_UPLOAD)
    @login_required
    def upload_image(self, image_path, key='file'):
        data = {}
        header = deepcopy(HEADERS)
        data[key] = (image_path.rsplit(os.sep)[-1], open(image_path, 'rb').read())
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header['content-type'] = encode_data[1]
        self.login_headers.update(header)
        return {
            'params': data,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'上传图片 {image_path} 成功!',
                'fail': f'上传图片 {image_path} 失败.',
            }
        }

    @action('post', api=API_ARTICLE_IMAGE_UPLOAD)
    @login_required
    def _upload_article_img(self, img_url, img_width, img_height):
        image_info = [{
            'url': img_url,
            "remark": '',
            'title': '',
            'content': '',
            'width': img_width,
            'height': img_height,
        }]
        self.login_headers.update({
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://mp.toutiao.com',
            'referer': 'https://mp.toutiao.com/profile_v3/graphic/publish'
        })
        return {
            'params': {
                'platform': 'toutiaohao',
                'position': 'articleup_sub',
                'image_info': image_info,
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'msg': 'ok',
            },
            'tips': {
                'ok': f'上传作品图片 {img_url} 成功!',
                'fail': f'上传作品图片 {img_url} 失败.',
            }

        }

    @action('post', api=API_IMG_QRCODE_CHECK)
    @login_required
    def _article_img_qrcode_check(self, img_url):
        self.login_headers.update({
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://mp.toutiao.com',
            'referer': 'https://mp.toutiao.com/profile_v3/graphic/publish'
        })
        return {
            'params': {
                'image_urls': img_url
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'作品图片 {img_url} 二维码图片检测上传成功!',
                'fail': f'作品图片 {img_url} 二维码图片检测上传失败.',
            }
        }

    @action('get', api=API_ARTICLE_IMG_CHECK)
    @login_required
    def _article_img_check(self, img_url):
        return {
            'params': {
                'image_url': img_url,
                'platform': 'toutiaohao',
                'position': 'articleup_sub',
                'noCache': f'{int(time.time()*1000)}'
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'msg': 'ok',
            },
            'tips': {
                'ok': f'作品图片 {img_url} 图片检测上传成功!',
                'fail': f'作品图片 {img_url} 图片检测上传失败.',
            }
        }

    @action('post',api=API_CHANGE_RESOURCE_REF)
    @login_required
    def change_media_resource_ref(self,web_uri,opt='add',rtype='3',saved=False,api=None):
        self.login_headers.update({
            'content-type':'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://mp.toutiao.com',
            'referer': 'https://mp.toutiao.com/profile_v3/graphic/resource-manager'
        })
        params = {
            'resource_id':web_uri,
            'resource_type':rtype,
        }
        if saved :
            params.update({
                'is_saved':'1',
            })
        elif saved is 0:
            params.update({
                'is_saved': '0',
            })
        else:
            params.update({
                'operation': opt,
            })
        return {
            'params':params,
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'api':api,
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'素材库图片 操作 {opt} id:{web_uri} 成功!',
                'fail': f'素材库图片 操作 {opt} id:{web_uri} 失败.',
            },
        }

    @action('get',api=API_WENDA_ANALYSIS)
    @login_required
    def wenda_analysis(self):
        return {
            'params':{
                'stat_type':5,
                'stat_keys':'["answer_count","go_detail_count","digg_count"]',
            },
            'extra_kwargs': {
                'headers': self.login_headers,
                'JSON': 1,
            },
            'msg': {
                'message': 'success',
            },
            'tips': {
                'ok': f'获取 悟空问答 当前状态数据  成功!',
                'fail': f'获取 悟空问答 当前状态数据 失败.',
            },
        }

    @action('get',api=API_SMALL_VIDEO_ANALYSIS)
    @login_required
    def small_videos_analysis(self,start_date,end_date,pagenum=1):
        return {
               'params': {
                   'start_date': start_date,
                   'end_date': end_date,
                   'page_num':pagenum,
               },
               'extra_kwargs': {
                   'headers': self.login_headers,
                   'JSON': 1,
               },
               'msg': {
                   'message': 'success'
               },
               'tips': {
                   'ok': f'日期：{start_date} 至 {end_date} 登陆用户小视频数据分析信息获取 成功!',
                   'fail': f'日期：{start_date} 至 {end_date} 登陆用户小视频数据分析信息获取 失败.',
               },
        }

    def follow_users(self, uids,
                     skip_no_fans=False,
                     skip_no_followings=False,
                     no_articles=False,
                     no_videos=False,
                     no_weitt=False
                     ):
        for uid in uids:
            user = TTUser(uid)
            if skip_no_fans:
                if user.fans_count == 0:
                    continue
            if skip_no_followings:
                if user.follow_count == 0:
                    continue
            if no_articles:
                res = user.get_published(count=1,MODE=ARTICLE)
                if not res:
                    continue
            if no_videos:
                res = user.get_published(count=1, MODE=VIDEO)
                if not res:
                    continue
            if no_weitt:
                res = user.get_published(count=1, MODE=WEITT)
                if not res:
                    continue
            self.follow_user(uid)

    def unfollow_users(self, uids,
                       only_no_fans=False,
                       only_no_followings=False,
                       no_articles=False,
                       no_videos=False,
                       no_weitt=False
                       ):
        for uid in uids:
            user = TTUser(uid)
            if only_no_fans:
                if user.fans_count != 0:
                    continue
            if only_no_followings:
                if user.follow_count != 0:
                    continue
            if no_articles:
                res = user.get_published(count=1,MODE=ARTICLE)
                if res:
                    continue
            if no_videos:
                res = user.get_published(count=1, MODE=VIDEO)
                if res:
                    continue
            if no_weitt:
                res = user.get_published(count=1, MODE=WEITT)
                if res:
                    continue
            self.unfollow_user(uid)

    def follow_followings_of_user(self,uid,
                                  skip_no_fans=False,
                                  skip_no_followings=False,
                                  no_articles=False,
                                  no_videos=False,
                                  no_weitt=False,
                                  count=COUNT_FOLLOWING,
                                  ALL=True,
                                  ):
        user = TTUser(uid)
        followings = user.get_followings(count=count,ALL=ALL)
        uids = [i.get('user_id') for i in followings]
        self.follow_users(uids,
                          skip_no_fans=skip_no_fans,
                          skip_no_followings=skip_no_followings,
                          no_articles=no_articles,
                          no_videos=no_videos,
                          no_weitt=no_weitt)

    def unfollow_followings_of_user(self,uid,
                                    only_no_fans=False,
                                    only_no_followings=False,
                                    no_articles=False,
                                    no_videos=False,
                                    no_weitt=False,
                                    count=COUNT_FOLLOWING,
                                    ALL=True,
                                    ):
        user = TTUser(uid)
        followings = user.get_followings(count=count, ALL=ALL)
        uids = [i['user_id'] for i in followings if i.get('user_id')]
        self.unfollow_users(uids,
                            only_no_fans=only_no_fans,
                            only_no_followings=only_no_followings,
                          no_articles=no_articles,
                          no_videos=no_videos,
                          no_weitt=no_weitt)