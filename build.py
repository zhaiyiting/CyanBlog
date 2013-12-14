import time
import os.path as osp
import mako.template as mtp
from mako.lookup import TemplateLookup
import config as common

class Builder(object):

    def __init__(self, post_list):
        self.post_list = post_list

    def build_post(self):
        template_name = "post.html"
        template_path = osp.join(common.template_dir, template_name)
        pre_post_list = self.post_list[:-1]
        pre_post_list.insert(0, None)
        post_post_list = self.post_list[1:]
        post_post_list.append(None)
        for i, post in enumerate(self.post_list):
            np = {"common":common,
                   "pre_post":pre_post_list[i],
                   "post":post,
                   "post_post":post_post_list[i],
                   "title":post.title}
            html = self.tmplate_render(template_path, np)
            output_path = osp.join(common.site_post_dir, post.filename+".html")
            with open(output_path, 'w') as f:
                f.write(html)

    def build_home(self):
        template_name = "home.html"
        template_path = osp.join(common.template_dir, template_name)
        home_pic = common.pic_dir + "home.jpg"
        np = {"common":common,
              "pic":home_pic,
              "title":common.blog_title}
        html = self.tmplate_render(template_path, np)
        output_path = osp.join(common.site_dir, "index.html")
        with open(output_path, 'w') as f:
            f.write(html)

    def build_archive(self):
        template_name = "list.html"
        template_path = osp.join(common.template_dir, template_name)
        post_group_name_list=[]
        post_group_list = []
        for post in self.post_list:
            post_year = post.create_time.split('-')[0]
            if not post_year in post_group_name_list:
                post_group_name_list.append(post_year)
                post_group_list.append([])
                current_group = post_group_list[-1]
            else:
                index = post_group_name_list.index(post_year)
                current_group = post_group_list[index]
            current_group.append(post)
        np = {"common":common,
              "post_group_name_list":post_group_name_list,
              "post_group_list":post_group_list,
              "title":common.blog_title}
        html = self.tmplate_render(template_path, np)
        output_path = osp.join(common.site_dir, "archives.html")
        with open(output_path, 'w') as f:
            f.write(html)

    def build_category(self):
        template_name = "list.html"
        template_path = osp.join(common.template_dir, template_name)
        post_group_name_list=[]
        post_group_list = []
        tag_num = []
        for post in self.post_list:
            post_category = post.category
            if not post_category in post_group_name_list:
                post_group_name_list.append(post_category)
                post_group_list.append([])
                current_group = post_group_list[-1]
                tag_num.append(1)
            else:
                index = post_group_name_list.index(post_category)
                current_group = post_group_list[index]
                tag_num[index] += tag_num[index]
            current_group.append(post)
        np = {"common":common,
              "post_group_name_list":post_group_name_list,
              "post_group_list":post_group_list,
              "tag_list":post_group_name_list,
              "tag_num":tag_num,
              "title":common.blog_title}
        html = self.tmplate_render(template_path, np)
        output_path = osp.join(common.site_dir, "categories.html")
        with open(output_path, 'w') as f:
            f.write(html)

    def build_tag(self):
        template_name = "list.html"
        template_path = osp.join(common.template_dir, template_name)
        post_group_name_list=[]
        post_group_list = []
        tag_num = []
        for post in self.post_list:
            post_tags = post.tags
            for tag in post_tags:
                if not tag in post_group_name_list:
                    post_group_name_list.append(tag)
                    post_group_list.append([])
                    tag_num.append(1)
                    current_group = post_group_list[-1]
                else:
                    index = post_group_name_list.index(tag)
                    current_group = post_group_list[index]
                    tag_num[index] += 1
                current_group.append(post)
        np = {"common":common,
              "post_group_name_list":post_group_name_list,
              "post_group_list":post_group_list,
              "tag_list":post_group_name_list,
              "tag_num":tag_num,
              "title":common.blog_title}
        html = self.tmplate_render(template_path, np)
        output_path = osp.join(common.site_dir, "tags.html")
        with open(output_path, 'w') as f:
            f.write(html)


    def build_aboutme(self):
        template_name = "about_me.html"
        template_path = osp.join(common.template_dir, template_name)
        about_pic = common.pic_dir + "about.jpg"
        np = {"common":common,
              "pic":about_pic,
              "title":common.blog_title}
        html = self.tmplate_render(template_path, np)
        output_path = osp.join(common.site_dir, "about_me.html")
        with open(output_path, 'w') as f:
            f.write(html)

    def build_rss(self):
        template_name = "feed.xml"
        template_path = osp.join(common.template_dir, template_name)
        pre_date = time.strftime("%Y-%m-%d")
        post_date = time.strftime("%H:%M:%S-08:00")
        date = pre_date + "T" + post_date
        for post in self.post_list:
            post.date = post.create_time + "00:00:00-08:00"
        np = {"common":common,
              "date":date,
              "post_list":self.post_list}
        html = self.tmplate_render(template_path, np)
        output_path = osp.join(common.site_dir, "feed.xml")
        with open(output_path, 'w') as f:
            f.write(html)

    def tmplate_render(self, template_path, np):
        lookup = TemplateLookup(directories=".")
        tmp_late = mtp.Template(filename=template_path, lookup=lookup)
        tmp_late.output_encoding = 'utf-8'
        html = tmp_late.render(**np)
        return html
