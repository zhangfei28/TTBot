#coding:utf-8

# ------ 用户账户设置 ------
#今日头条账户密码
USERNAME = ''
PASSWORD = ''
# 用户cookie,可置空，格式 ： 'tt_web_id=xxxxx;sso_user=xxxx'
COOKIE = ''
# 存放用户cookie的文件路径
COOKIE_FILE = 'accessory/cookie.txt'

# ------ MongoDB数据库设置 ------
MONGODB = {
    'host'              :'127.0.0.1',
    'port'              :27017,
    'database'          :'TTBot2019',
    '__all__'           :'今日头条web首页推荐新闻数据库',
    'my_videos'         :'今日头条登陆用户小视频数据库',
    'my_articles'       :'今日头条登陆用户发布图文作品数据库',
    'favourite'         :'今日头条登陆用户收藏数据库',
    'comments'          :'今日头条登陆用户微头条(转发评论)数据库',
    'search'            :'今日头条搜索数据库',
    'article'           :'今日头条用户文章数据库',
    'video'             :'今日头条用户视频数据库',
    'weitt'             :'今日头条用户微头条数据库',
    'followings'        :'今日头条用户关注数据库',
    'fans'              :'今日头条用户粉丝数据库',
    'subscribers'       :'今日头条用户订阅者数据库',
    'news_hot'          :'今日头条热点新闻数据库',
    'news_entertainment':'今日头条娱乐新闻数据库',
    'news_tech'         :'今日头条科技新闻数据库',
    'news_game'         :'今日头条游戏新闻数据库',
    'news_sports'       :'今日头条体育新闻数据库',
    'news_car'          :'今日头条汽车新闻数据库',
    'news_finance'      :'今日头条财经新闻数据库',
    'internet'          :'今日头条互联网新闻数据库',
    'software'          :'今日头条软件新闻数据库',
    '智能家居'           :'今日头条智能家居新闻数据库',
    '电视剧'             :'今日头条电视剧新闻数据库',
    '综艺'               :'今日头条综艺新闻数据库',
    'gossip'            :'今日头条八卦新闻数据库',
    'movie'             :'今日头条电影新闻数据库',
    'NBA'               :'今日头条NBA新闻数据库',
    'CBA'               : '今日头条CBA新闻数据库',
    '中超'               :'今日头条中超新闻数据库',
    'football_italy'    :'今日头条意甲新闻数据库',
    'car_new_arrival'   :'今日头条新车新闻数据库',
    'SUV'               :'今日头条SUV车型新闻数据库',
    'car_guide'         :'今日头条汽车导购新闻数据库',
    'car_usage'         :'今日头条用车新闻数据库',
    'investment'        :'今日头条投资新闻数据库',
    'stock'             :'今日头条股票新闻数据库',
    'finance_management':'今日头条理财新闻数据库',
    'macro_economic'    :'今日头条宏观经济新闻数据库',
    'news_military'     :'今日头条军事新闻数据库',
    'military_china'    :'今日头条中国军情新闻数据库',
    'military_world'    :'今日头条环球军事新闻数据库',
    'weaponry'          :'今日头条武器新闻数据库',
    'funny'             :'今日头条搞笑新闻数据库',
    'news_fashion'      :'今日头条时尚新闻数据库',
    '时装'               :'今日头条时装新闻数据库',
    '美体'               :'今日头条美体新闻数据库',
    '腕表'               :'今日头条腕表新闻数据库',
    '珠宝'               :'今日头条珠宝新闻数据库',
    'news_food'         :'今日头条美食新闻数据库',
    'news_essay'        :'今日头条美文新闻数据库',
    'news_baby'         :'今日头条育儿新闻数据库',
    'news_travel'       :'今日头条旅游新闻数据库',
    'news_world'        :'今日头条国际新闻数据库',
    'news_history'      :'今日头条历史新闻数据库',
    'news_regimen'      :'今日头条养生新闻数据库',
    'news_discovery'    :'今日头条探索新闻数据库',
    'wenda_draft'       :'悟空问答草稿箱',
    'wenda'             :'悟空问答我的问题列表',
    'user'              :'',
    'password'          :'',
}
# 链式爬取存储已爬取用户uid的表名
FINISHED_TABLE = 'finished_uids'

# ------ selenium相关设置 ------
CHROME_PATH = 'accessory/chromedriver.exe'
IMG_BIG_PATH = 'img/big.png'
IMG_BLOCK_PATH = 'img/block.png'
IMG_S_BIG_PATH = 'img/big_s.png'
IMG_S_BLOCK_PATH = 'img/block_s.png'

# ------ 用户爬取相关设置 ------
# 整站用户链式爬取模式下的最初入口用户ID
ENTER_USER_ID = '8'
# 最大的爬取线程数
MAX_THREADS = 100
# 爬取热点新闻最大的默认条数
COUNT_HOTNEWS = 1000
# 爬取非视频
# 爬取单个用户最多的发布的新闻文章篇数
COUNT_NEWS = 100
# 爬取用户关注账户的最多默认数
COUNT_FOLLOWING = 1000
# 爬取用户粉丝账户的最多默认数
COUNT_FANS = 10000
# 爬取登陆账户收藏的最多默认数
COUNT_FAVOURITES = 10000
# 爬取登陆账户评论的最多默认数
COUNT_POSTS = 10000
# 爬取登陆账户小视频的最多默认数
COUNT_VIDEOS = 10000
# 爬取登陆账户发布图文作品的最多默认数
COUNT_ARTICLES = 10000
# 搜索cookie中的s_v_web_id
SVWEBID = ''
# 存放最新的s_v_web_id 值文件，删除该文件程序会自动更新
SVWEBID_FILE = 'accessory/svwebid.txt'
# 搜索结果最多返回最大的默认数
COUNT_SEARCH = 1000

# ------ 代理相关设置 ------
#是否使用代理
PROXY_ENABLE = True
#使用单个的代理ip，优先级最高
#此项若有填写，则使用此代理，后面的代理池PROXY_POOL不会考虑
# 格式可以为下面几种:
# 1.  "127.0.0.1:8080"
# 2.  "username:password@1.1.1.1:1111"
# 3.  "www.dailiurl.com/path/xxxx"
# 4.  "username:password@www.dailiurl.com/path/xxxx"
PROXY = ''
#代理池，此处用的是一次一个，每次不同,示例代理链接，请自行替换自己的代理url
PROXY_POOL = 'https://xxx.com/proxy/get?token=xx&amount=1&proxy_type=http&format=txt&splitter=rn&expire=300'

# ------ HTTP请求相关设置 ------
#请求失败后的重试次数：
# -1表示无限次请求；
# 0表示不重试；
# >0的表示重试的次数
MAX_RETRY = 10
#访问请求的时间间隔设置，单位：秒
DELAYS = 1
#合法请求操作列表
HTTP_METHODS = ['get','head','post','put','options']
#访问返回结果属于正常的状态码列表
OK_CODE = [200,]

# ------ 日志设置 ------
#启用日志
LOG_ENABLE = True
#日志显示级别
LOG_LEVEL = 'INFO'
#日志文件编码
LOG_FILE_ENCODING = 'UTF-8'
#日志文件路径
LOG_FILE_SAVE_PATH = r'log/log.txt'
#日志时间格式
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
#日志级别对应格式
LOG_FORMAT = {
    'DEBUG'     : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'INFO'      : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'WARNING'   : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'ERROR'     : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'CRITICAL'  : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
}