import sys
import time
import os
import os.path as osp
import cPickle
import shutil
import markdown
import config as common

class Post(object):

    def __init__(self, filename):
        # use time mark as the default title
        self.title = time.strftime("%Y-%m-%d")
        self.create_time = time.strftime("%Y-%m-%d")
        self.category = 'Uncategorized'
        self.tags = ['No-tag']
        self.time = time.time()

        # use post's file mame to identify one post
        # never use the same name for different post
        self.filename = filename
        self.link = "/post/" + self.filename + ".html"
        self.content = ""
        self.html = ""

    def new_post(self, post_title=None, post_category=None, post_tags=None,
            post_content = ""):
        if post_title:
            self.title = post_title
        if post_category:
            self.category = post_category
        if post_tags:
            self.tags = post_tags
        self.content = post_content

    def update(self, other):
        # update the history post with new post
        # history post will store the time info
        self.title = other.title
        self.category = other.category
        self.tags = other.tags
        


class Reader(object):
    def __init__(self):
        self.history_post_list = []
        self.history_post_name_list = []
        self.current_post_list = []

    def get_history_post(self):
        if osp.exists(common.history_path):
            history = open(common.history_path, 'r')
            self.history_post_list = cPickle.load(history)
            self.history_post_name_list = [post.filename for post in self.history_post_list]

    def get_current_post(self):
        post_list = os.listdir(common.post_dir)
        for post_name in post_list:
            post_path = osp.join(common.post_dir, post_name)
            self.__parse_post(post_path)
        # sort post
        def s(post):
            return post.time
        self.current_post_list.sort(key = s)

    def __parse_post(self, post_path):
        post_title = None
        post_category = None
        post_tags = None
        with open(post_path, 'r') as f:
            content = f.readlines()
            for i,line in enumerate(content):
                line = line.strip()
                tmp_list = line.split(":")
                for j in range(len(tmp_list)) :
                    tmp_list[j] = tmp_list[j].strip()
                if not line:
                    continue
                if line.startswith("~~~"):
                    # the post's meta data and content is separated by "~~~~~"
                    break
                elif tmp_list[0].startswith("title"):
                    if len(tmp_list) > 1:
                        post_title = tmp_list[1]
                elif tmp_list[0].startswith("cat"):
                    if len(tmp_list) > 1:
                        post_category = tmp_list[1]
                elif tmp_list[0].startswith("tag"):
                    if len(tmp_list) > 1:
                        tag_list = tmp_list[1].split(":")
                        post_tags = tag_list
            if i == len(content):
                # no separat line found
                print "Error: no separate line found in post{0}".format(post_path)
                return
            post_content = content[i+1:]
            post_content = '\n'.join(post_content)
            post_content = post_content.decode("gbk")
                        
        post_name = osp.basename(post_path)
        post_name = post_name.split(".")[0]
        new_post = Post(post_name)
        if post_name in self.history_post_name_list:
            index = self.history_post_name_list.index(post_name)
            new_post.update(self.history_post_list[index])
        new_post.new_post(post_title=post_title,
                          post_category=post_category,
                          post_tags=post_tags,
                          post_content=post_content)
        self.current_post_list.append(new_post)


    def dump(self):
        with open(common.history_path, 'w') as f:
            for post in self.current_post_list:
                del post.content
                del post.html
            cPickle.dump(self.current_post_list, f)


class Writer(object):

    def __init__(self, post_list):
        self.post_list = post_list
        self.__pre_build()
        self.__convert_post()


    def __pre_build(self):
        # recreate the site folder
        if osp.exists(common.site_dir):
            shutil.rmtree(common.site_dir)
        time.sleep(0.5)
        # make new
        os.mkdir(common.site_dir)
        # make post dir
        os.mkdir(common.site_post_dir)
        # copy static dir
        shutil.copytree(common.static_dir, common.site_static_dir)

    def __convert_post(self):
        for post in self.post_list:
            build_post_path = osp.join(common.site_post_dir, post.filename)
            #output_file = codecs.open(build_post_path, 'w', encoding="utf-8")
            post_html = markdown.markdown(post.content)
            post.html = post_html
            #output_file.write(post_html)
