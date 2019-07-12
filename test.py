#coding=utf-8
import time
from component.toutiao import TTBot
from component.user import TTUser

# def ass(res):
#     print(res)
#
# if __name__ == '__main__':
    # a = TTBot()
    # account = a.account
    # news_spider = a.news_spider
    # uids = ['50502346173', '4377795668', '3640241275','70105485318','97658287933']
    # print(account.wenda_analysis())
    # print(account.delete_article('6602141020383609358'))
    # print(account.unstore_media('6711635660941296132'))
    # print(account.unhide_article('6711941566493098504'))
    # print(account.get_unread_fans_count())
    # print(account.get_wenda_invited_count())
    # print(account.get_sensitive_op_log(pagesize=1))
    # print(account.unstar_resource_img('pgc-image/a8dc04c83f194adc9d0b56365e42fe50'))
    # print(account.delete_articles(status='checking',keyword='粉丝'))
    # print(account.delete_question('6711866197685567758'))
    # print(account.get_wenda_drafts(MDB=1))
    # print(account.get_wenda_questions(MDB=1))
    # for i in range(20,26):
    #     time.sleep(1)
    #     print(account.post_question(f'this is a test q {i}',content=f'tested'))
    # print(account.delete_wenda_draft('6711665324736905475'))
    # print(account.post_reply('thisisatest','6689315272605565452','6689386720494043147','86931246069'))
    # print(account.unfollow_followings_of_user('4377795668',count=20,ALL=False))
    # print(account.unfollow_users(uids))
    # news_spider.get_recommend_news(last_time='2019-07-07 10:50:00',MDB=1)
    # a.search('Gucci',MDB=1,USER=True)
    # a.interact_with_users(['68164853722'],comment_on_article=True,comment_txt='新的评论',comment_count=2,repost_on_article=True,repost_txt='新的转发',repost_count=1)
    # a.timer.setup(
    #     '2019-07-06 15:10:00',
    #     a.interact_with_users,
    #     args=(['75953693736','65445676041'],),
    #     kwargs={
    #             'comment_on_weitt':True,
    #             'comment_start_time':'2019-06-17 00:00:00',
    #             'comment_end_time':'2019-06-18 00:00:00',
    #             # 'comment_on_video':True,
    #             # 'comment_on_article': True,
    #             'comment_txt':'定时器评论',
    #             'comment_count':1,
    #             'repost_on_article':False,
    #             'repost_txt':'定时器转发',
    #             'repost_count':1
    #             },
    # )
    # a.timer.setup('2019-07-05 16:51:00',account.post_weitt,
    #               args=('This is a funny sslsss   sssittle test',),
    #               looping=True,
    #               frequency=360,
    #               args_func=lambda x:(f'{x[0]}-{time.time()}',),
    #               callback=ass)
    # a.timer.setup('2019-07-05 16:31:10',account.post_weitt,args=('This is a funnys little test',),callback=ass)
    # a.run_timer_jobs()
    # news_spider.get_body_shape_news(MDB=1,ALL=1)
    # news_spider.get_recommend_news(MDB=1,ALL=1)
    # a.grab_all_user_posts('all')
    # u = TTUser('3564799576')
    # u.get_fans(MDB=True)
    # print(u.info)
    # u.get_published(ALL=True,MDB=1,MODE='2')
    # u.get_followings(MDB=1)
    # u.get_published(ALL=True,MDB=1,MODE='0')
    # u.get_published(ALL=True, MDB=1, MODE='2')
    # account.unfollow_user('13522641920')
    # aa = u.get_published(count=1,MODE='1')
    # print(u.get_followings())
    # print(type(u.fans_count))
    # u.get_published(count=2,MODE='2',MDB=1)
    # u.get_published(ALL=True,data_cb=lambda x:1)
    # u.get_followings(ALL=True,MDB=1)
    # a.login()
    # a.login_helper.stop()
    # a.search('Java',MDB=1)
    # a.get_regimen_news(MDB=1, ALL=True)
    # account.unfollow_user('92961638858')
    # account.get_posted_articles(MDB=1)
    # account.get_posts(MDB=1)
    # account.delete_articles('checking')
    # print(account.upload_image(r'C:\Users\linkin\Pictures\公众号素材\图片\1timg.jpg'))
    # cc= [r'C:\Users\linkin\Pictures\公众号素材\图片\1timg.jpg',
    #      r'C:\Users\linkin\Pictures\公众号素材\图片\122.jpg']
    # print(account.post_weitt('THIS CONTENT IS POSTED BY TTBOT[笑]',image=cc))
    # print(account.delete('1637579341680651'))
    # print(account.repost('转发并评论','6689315272605565452','6636211626'))
    # print(account.delete_media('6711667304335802382',comment=True))
    # print(account.delete_media('1638551478768651'))
    # print(account.post_question('这是测试悟空问答问题','这是描述问题的内容',image=cc))
    # print(account.post_comment('为习主席点赞[赞][赞][赞][玫瑰][玫瑰][玫瑰]','6707502309561074180'))
    # print(account.post_reply('赞赞','6707502309561074180','6707523403937185803','95480041731','6707601855809487000'))
    # print(account.unstore_media('6707502309561074180'))
    # print(account.user_info)
    # print(account.media_id)
    # print(account.media_info)
    # news_spider.get_discovery_news(MDB=1)
    # print(account.unblock_user('5734066007'))
    # print(account.get_blocking_users())
    # print(account.get_notification_count())
    # account.get_subscribers(MDB=1)
    # print(account.user_id)
    # me = TTUser('5954781019')
    # me.get_fans(MDB=1)
    # account.get_favourites(MDB=1)
    # print(account.repost(f'THIS is a video repost test.{155}','6706405709120012813','1200318619324636'))
    # print(account.delete('6708177380906713096',comment=1))
    # print(account.post_comment('ffff','6702678918014435847'))
    # print(account.get_comments_of_media('6689315272605565452'))
    # print(account.delete('6708129817458098180',comment=1))
    # print(account.like_comment('6708188534878044173'))
    # print(account.delaa ete('6708129812113965060',comment=1))
    # print(account.account_status)
    # print(account.get_my_posts(MDB=1))
    # print(account.delete_video('6708196596980383751'))
    # account.get_my_posts(MDB=1)
    # print(account.delete_wenda_draft('6708204462206353675'))
    # print(account.get_interact_fans())
    # print(account.get_fans_trend('2019-07-10','2019-07-12'))
    # print(account.get_content_overview('2019-07-10','2019-07-12'))
    # print(account.wenda_analysis())
    # print(account.small_videos_analysis('2019-07-01','2019-07-13'))
    # print(account.upload_resource_img(r'C:\Users\linkin\Pictures\公众号素材\图片\22.jpg'))
    # print(account.delete_resource_img('pgc-image/266565ea60cb42c3a54b94ebdc58923a'))
    # print(account.unstar_resource_img('pgc-image/a53f6b919f6142589cd150d49af1d33f'))
    # print(account.get_resource_images())
    # print(account.upload_resource_img_by_url('https://tuchong.pstatp.com/1695426/f/68419895.jpg'))
    # print(account.get_unread_msg())
    # print(account.get_wenda_invited_count())
    # print(account.cancel_top_article('6709615853203096071','1562204177'))
    # print(account.hide_article('6709615853203096071','1562204177'))
    # print(account.unhide_article('6709615853203096071', '1562204177'))
    # print(account.get_sensitive_op_log())
    # print(account.get_login_log(page=2))
    # print(account.post_article('I robot sssss ',
    #                            u'''<div><p>不少人都曾抱怨过，为什么付出了那么多，还是没有看到自己身上增了多少肌肉量？
    #                            </p><p><strong>是不是自己没有健身天赋造成的？</strong></p>
    #                            <p>其实，大多数人都是没有健身天赋的，而且也没有轮到拼天赋的时候。天赋这东西属于不可控因素，我们要做的就是把可控的那部分完成也能取得不俗的效果。</p><p>之所以增肌效果差，还是不外乎没有做到以下4点！</p>
    #                            <div class="pgc-img"><p class="pgc-img-caption"></p></div><h1>1.健身没有规划，频率没有达到。</h1><p>举个例子：佳名每周只有两天去健身房训练，他每次训练两个部位，每次训练3个小时，但他坚持了半年仍然看不到明显效果。</p><p>其实健身并不是靠一次两次高强度训练的积累就能看到效果的，训练频率绝对是一个我们没法忽视的重要因素。</p><p>你一周只练一次胸肌和一周练两次胸肌，半年累积的效果绝对是天壤之别。</p><p>训练效果和训练容量有着密不可分的关系，训练容量又关乎到你的训练次数，组数，重量和频率。
    #                            </p><p>简单来说可以用以下公式体现：训练容量=训练次数x训练组数x训练重量，而训练频率就是在它们后面再乘以2。</p>
    #                            <p>合理的安排训练计划，增加训练频率绝对是你高效进阶的不二法门。</p>
    #                            </p></div>
    #                            <h1>2.不注意饮食，饮食是时间线更长的“训练”。</h1>
    #                            <p>在我刚开始接触健身的时候，有个大神告诉我他是靠吃面条增的肌。我当时坚信不疑，尝试了几个月发现并没有卵用。那时我才明白，这可能只是一句调侃的话，为曾经的榆木脑袋干杯。</p>
    #                            <p>随着对健身饮食的了解加深，我才意识到健身真的是吃什么长什么。你吃的不干净就是会多长脂肪，吃的太少就是体重难以增加，不重视吃，身材真的就不会给你好脸色看。</p>
    #                            <p>想让体内肌肉不断增长，就得重视蛋白质和碳水化合物的摄入量，即便我们无法做到精准计算，但往目标值靠拢总是最好的方案。</p>
    #                            </p></div><h1>3.轻视休息，无视睡眠。</h1>
    #                            <p>坚持健身久了，真的会上瘾。</p>
    #                            <p>相信很多人都能体会到健身给自己带来的愉悦，所以他们每天都往健身房跑，以为这样就能够比别人多长一些肌肉。出发点是好的，因为懒人很难增肌，但过频的训练反倒让肌肉无法安心生长。</p>
    #                            <!----><p><strong>每周留出1-2天作为休息时间，别觉得这是浪费，因为休息是为下次训练积蓄能量。</strong></p>
    #                            <p>而睡眠时间不足，绝对也是很多人都存在的问题。</p><p>舍不得睡，不想睡和不能睡之间，我们总是选择了前两种。因为想知道的东西太多了，总想把它们都装进脑袋。但我们要知道，睡眠时间直接影响生长激素，睡眠时间太短肌肉就无法在睡眠中增长，脂肪的分解也会受挫。</p>
    #                            <p><strong>简单来说，经常熬夜会影响增肌效率，让自己更容易变胖。</strong></p>
    #                            </p></div><h1>4.训练质量不达标，每次都点到为止。</h1>
    #                            <p>相信我们都知道“三分练，七分吃”的概念，但这句话的意思并不是让我们投入30分的努力去训练就足够了，而是在三分练这块区域投入90分乃至100分的努力才可以。</p><p>其实有些人之所以进步慢，就是因为在训练时投入的努力不够。</p><p>明明能够标准的完成5组，偏偏做完4组就放弃了。计划了6个动作，实际做完4个就觉得完成度很高，没必要再做了。这省略下的几组动作，会在日积月累中和别人悄悄拉开差距。</p>
    #                            </p></div><p>没有哪一个人增肌走了很多捷径，你所经历的，正是每个人都在经历的。</p><p><strong>耐住心，沉住气，完成它。</strong></p>
    #                            <p>好了，这一期的分享就是这样了，如果你有想要了解的方法，可以在文末给我留言或者直接私信我。</p><p>我是波普董，每日分享健身知识，让你我更有型。</p>
    #                            <p><a class="tteditor-mention" data-name="头条健身" data-uid="58637709857" data-id="false" data-concern-id="false">@头条健身</a>
    #                            <a class="tteditor-forum" data-name="夏天就要瘦" data-uid="false" data-id="1631780770277383" data-concern-id="1631780770277383">#夏天就要瘦#</a>
    #                            <a class="tteditor-forum" data-name="清风计划" data-uid="false" data-id="1623417676578820" data-concern-id="1623417676578820">#清风计划#</a><a class="tteditor-forum" data-name="夏季养生正当时" data-uid="false" data-id="1633412250240020" data-concern-id="1633412250240020">#夏季养生正当时#</a></p></div>'''
    #                            , cover_img=r'C:\Users\linkin\Pictures\公众号素材\图片\sanj.jpg'))