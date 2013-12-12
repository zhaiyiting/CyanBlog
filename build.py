import os
import os.path as osp
author_name = "luxiaolu"
title = "Dai Daily"

link = "http://luxiaolu.github.io"
feed_link = "/feed.xml"

class Page(object):

    def __init__(self, title, link):
        self.title = title
        self.link = link

home_page = Page(title="Home", link="/")
about_me_page = Page(title="About me", link="/about_me")
rss_page = Page(title="RSS", link=feed_link)
page_list = [home_page, about_me_page, rss_page]

current_page = home_page

class G_nsp(object):
    def __init__(self, **dic):
        self.__dict__.update(dic)
g_nsp = G_nsp(**globals())
import mako.template as mtp
tmplate = mtp.Template(filename="base.html")
tmplate.output_encoding = 'utf-8'
with open("index.html", 'w') as f:
    f.write(tmplate.render(g_nsp=g_nsp, cpage=home_page)) 


class PostBuilder(object):
    template_dir = "_template"
    template_name = "post.html"

    def __init__(self, post_list):
        self.post_list = post_list
        self.template_path = osp.join(template_dir, template_name)
        self.html = ""

    def build_post(self):
        pre_post_list = self.post_list[:-1]
        pre_post_list.insert(0,None)
        post_post_list = self.post_list[1:]
        post_post_list.append(None)
        for i,post in enumerate(self.post_list):
            tmp_late = mtp.Template(filename=self.template_path)
            tmp_late.output_encoding = 'utf-8'
            self.html = tmp_late.render(pre_post = pre_post_list[i],
                                        post = post,
                                        post_post = post_post_list[i])
