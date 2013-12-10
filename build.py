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
