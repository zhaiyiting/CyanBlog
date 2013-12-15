# -*- coding: utf-8 -*-
author_name = "luxiaolu"
blog_title = "戴城厂报"
blog_link = "http://luxiaolu.github.io"


## site map
class Page(object):
    def __init__(self, title, link):
        self.title = title.decode("utf-8")
        self.link = link

blog_title = blog_title.decode("utf-8")

rss_link = "/feed.xml"
archive_link = "/archives.html"
category_link = "/categories.html"
tag_link = "/tags.html"
home_page = Page("Home", "/index.html")
archive_page = Page("归档", archive_link)
category_page = Page("分类", category_link)
tag_page = Page("标签", tag_link)
aboutme_page = Page("关于我", "/about_me.html")
rss_page = Page("订阅", rss_link)


page_list = [home_page, archive_page, category_page, tag_page, aboutme_page, rss_page]

template_dir = "_template"
post_dir = "_post"
static_dir = "_static"
pic_dir = "/static/default/pic/"
import os.path as osp
history_path = osp.join("_history", "history")

site_dir = "site"
site_post_dir = "site/post"
site_post_dir_mk = "site/_post"
site_static_dir = "site/static"

