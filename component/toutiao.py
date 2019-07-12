#coding:utf-8

from component.log import getLogger
from component.search import Searcher
from component.account import TTAcount
from component.timer import Timer
from component.news import TTNews
from component.user import TTUser
from component.grabber import UserGrabber
from config import COUNT_SEARCH,SVWEBID_FILE,SVWEBID
from settings import ARTICLE,VIDEO,WEITT
from util.tools import time_to_date
from util.user import weitt_cleaner

logger = getLogger(__name__)

c_count = 0
r_count = 0

class  TTBot:

    def __init__(self):
        self.timer = Timer()
        self.searcher = Searcher()
        self.news_spider = TTNews()
        self.account = TTAcount()
        self.user_grabber = UserGrabber()

    def search(self,keyword,
               USER=False,
               VIDEO=False,
               count=COUNT_SEARCH,
               ALL=True,
               MDB=None,
               strict=False,
               login=False
               ):
        """
        今日头条搜索，一般情况下是综合搜索，可以根据参数设置搜索对象，
        web页面搜索需要验证滑动，此处使用selenium模拟。
        :param keyword: 搜索关键词
        :param USER: 是否只搜索相关用户
        :param VIDEO: 是否只搜索相关视频
        :param count: 搜索结果获取的最多条数
        :param ALL: 是否获取全部搜索结果，若置True，count参数无效
        :param MDB: 是否进行数据库保存，可以是一个Database实例或者置1,置1后会自动创建一个新的Database实例进行数据保存
        :param strict: 是否启用严格匹配模式，只对搜索用户情况下有效
        :param login: 是否登录后再搜索
        :return: 搜索结果，[{},{},{},...]
        """
        if login:
            self.account.login()
        else:
            try:
                #先查看搜索需要的cookie字段 本地是否存在，不存在则查看config中是否设置
                with open(SVWEBID_FILE,'r') as f:
                    cookie = f.read()
                if not cookie:
                    cookie = SVWEBID
            except:
                cookie = None
            #以上两种皆无相关存储字段，则打开selenium获取
            if not cookie:
                self.searcher.validate()
            else:
                self.searcher.headers['cookie']=cookie
        return self.searcher.search(keyword,USER=USER,VIDEO=VIDEO,
                                    count=count,ALL=ALL,MDB=MDB,
                                    strict=strict)

    def grab_all_user_posts(self,mode):
        """
        链式获取用户的相关数据，默认使用数据库，具体：
        1.config中设置了链式爬取用户数据的入口用户uid, ENTER_USER_ID
        2.设置相关的爬取用户模式：爬取文章？视频？微头条？还是三者皆爬？参数详看mode
        3.循环爬取并存入数据库
        :param mode:
                '0':视频 ,'1':文章 ,'2':微头条 ,'all':全部
        """
        self.user_grabber.run_forever(mode)

    def interact_with_users(self,uids,
                            comment_start_time=None,
                            comment_end_time=None,
                            comment_on_article=False,
                            comment_on_video=False,
                            comment_on_weitt=False,
                            comment_article=None,
                            comment_video=None,
                            comment_weitt=None,
                            comment_txt=None,
                            comment_count=1,
                            repost_start_time=None,
                            repost_end_time=None,
                            repost_on_article=False,
                            repost_on_video=False,
                            repost_on_weitt=False,
                            repost_txt_article=None,
                            repost_txt_video=None,
                            repost_txt_weitt=None,
                            repost_txt=None,
                            repost_count=1,
                            ):
        """
        :param uids: 准备进行互动的用户uid列表
        :param comment_start_time: 对用户哪个时间段的头条进行评论互动的起始时间,如:'2019-07-05 09:10:12'
        :param comment_end_time: 对用户哪个时间段的头条进行评论互动的结束时间,如:'2019-07-05 09:10:12'
        :param comment_on_article: 是否对用户的发布头条作品进行评论
        :param comment_on_video: 是否对用户的发布视频进行评论
        :param comment_on_weitt: 是否对用户的微头条进行评论
        :param comment_article: 对用户发布的头条作品评论的内容
        :param comment_video: 对用户发布的视频评论的内容
        :param comment_weitt: 对用户发布的微头条评论的内容
        :param comment_txt: 对用户头条作品、视频、微头条评论的共同内容，此项若有，自动忽略前面三项评论内容
        :param comment_count: 对已确定头条作品、视频、微头条进行评论互动的条数
        :param repost_start_time: 对用户哪个时间段的头条进行转发互动的起始时间,如:'2019-07-05 09:10:12'
        :param reost_end_time: 对用户哪个时间段的头条进行转发互动的结束时间,如:'2019-07-05 09:10:12'
        :param repost_on_article: 是否对用户的发布头条作品进行转发
        :param repost_on_video: 是否对用户的发布视频进行转发
        :param repost_on_weitt: 是否对用户的微头条进行转发
        :param repost_txt_article: 对用户发布的头条作品转发并评论的内容
        :param repost_txt_video: 对用户发布的视频转发并评论的内容
        :param repost_txt_weitt: 对用户发布的微头条转发并评论的内容
        :param repost_txt:对用户头条作品、视频、微头条转发并评论的共同内容，此项若有，自动忽略前面三项评论内容
        :param repost_count:对已确定头条作品、视频、微头条进行转发并评论互动的条数
        """

        global c_count
        global r_count

        #每次调用 interact_with_users 函数 重置全局变量
        c_count = 0
        r_count = 0

        def data_cb(data,uid,cate,c_txt,rp_txt):
            """
            获取用户发布文章、视频、微头条API的回调函数
            :param data: 今日头条接口返回的原始json数据
            :param uid: 当前用户uid
            :param cate: 爬取模式，ARTICLE,VIDEO,WEITT之一
            :param c_txt: 评论互动的内容，无则置None
            :param rp_txt: 转发并评论 互动的内容，无则置None
            """

            global c_count
            global r_count

            shake = 0
            if cate == WEITT:
                id_key = 'wid'
                t_key = 'create_time'
            else:
                id_key = 'item_id'
                t_key  = 'behot_time'
            group_id = data.get(id_key)
            c_time   = data.get(t_key)
            if not c_time and cate == WEITT:
                data = weitt_cleaner(data)
                shake = 1
                c_time = data.get(t_key)
                if not c_time:
                    c_time = time_to_date(data.get('comment_base').get(t_key))
            else:
                c_time = time_to_date(int(c_time))
            if not group_id:
                if not shake:
                    data = weitt_cleaner(data)
                group_id = data.get('wid')
            if not group_id or not c_time:
                return 1
            if c_txt:
                if c_count < comment_count:
                    if all([comment_start_time,comment_end_time]):
                        if (comment_start_time <= c_time <= comment_end_time):
                            self.account.post_comment(c_txt,group_id)
                            c_count += 1
                        else:
                            return 1
                    else:
                        self.account.post_comment(c_txt, group_id)
                        c_count += 1
            if rp_txt:
                if r_count < repost_count:
                    if all([repost_start_time,repost_end_time]):
                        if repost_start_time <= c_time <= repost_end_time:
                            self.account.repost(rp_txt,group_id,uid)
                            r_count += 1
                        else:
                            return 1
                    else:
                        self.account.repost(rp_txt, group_id, uid)
                        r_count += 1

        def interact(mode):

            global c_count
            global r_count
            r_txt = None
            c_txt = None
            c_count = 0
            r_count = 0

            _mode = {
                ARTICLE: (comment_on_article, repost_on_article, comment_article, repost_txt_article),
                VIDEO: (comment_on_video, repost_on_video, comment_video, repost_txt_video),
                WEITT: (comment_on_weitt, repost_on_weitt, comment_weitt, repost_txt_weitt)
            }
            m = _mode[mode]
            if m[0]:
                c_txt = comment_txt if comment_txt else m[2]
            if m[1]:
                r_txt = repost_txt if repost_txt else m[3]
            if any([c_txt, r_txt]):
                count = max(comment_count, repost_count)
                _c = [None,c_txt][m[0]]
                _r = [None,r_txt][m[1]]
                user.get_published(count=count,
                                   MODE=mode, data_cb=data_cb,
                                   cb_args=(uid, mode,_c , _r), STRONG=True)

        for uid in uids:
            user = TTUser(uid)
            for i in [ARTICLE,VIDEO,WEITT]:
                interact(i)

    def run_timer_jobs(self):
        if self.timer.jobs:
            logger.info(f'开始执行定时器任务.当前任务数：{len(self.timer.jobs)}')
            self.timer.run()
        else:
            logger.info(f'当前定时器无任务.')