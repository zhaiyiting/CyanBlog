import time
import os
import os.path as osp
import cPickle
import shutil
import markdown
import codecs

history_path = osp.join("_history", "history")
post_dir = "_post"
site_dir = "_site"
static_dir = "_static"

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
    def __init__():
        self.history_post_list = []
        self.history_post_name_list = []
        self.current_post_list = []

    def get_history_post(self):
        if osp.exists(history_path):
            self.history_post_list = cPickle.load(history_path)
            self.history_post_name_list = [post.filename for post in self.history_post_list]

    def get_current_post(self):
        post_list = os.listdir(post_dir)
        for post_name in post_list:
            post_path = osp.join(post_path, post_name)
            self.__parse_post(post_path)

    def __parse_post(self, post_path):
        post_title = None
        post_category = None
        post_tags = None
        with open(post_path, 'r') as f:
            content = f.readlines()
            for i,line in enumerate(content):
                line = line.strip()
                tmp_list = line.split(":")
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
            post_content = content[i:]
            post_content = '\n'.join(post_content)
            post_content = post_content.decode("gbk")
                        
        post_name = osp.basename(post_path)
        new_post = Post(post_name)
        if post_name in self.history_post_name_list:
            index = self.history_post_name_list.index(post_name)
            new_post.update(self.history_post_list[index])
        new_post.new_post(post_title = post_title,
                          post_category = post_category,
                          post_tags = post_tags,
                          post_content = post_content)
        self.current_post_list.append(new_post)


    def dump(self):
        with open(history_path, 'w') as f:
        cPickle.dump(self.current_post_list, f)


class Writer(object):
    site_post_dir = osp.join(site_dir, "post")
    site_static_dir = osp.join(site_dir, "static")

    def __init__(self, post_list):
        self.post_list = post_list
        self.__pre_build()
        self.__convert_post()


    def __pre_build(self):
        # recreate the site folder
        shutil.rmtree(site_dir)
        # make new
        os.mkdir(site_dir)
        # make post dir
        os.mkdir(self.site_post_dir)
        # copy static dir
        shutil.copy(static_dir, self.site_static_dir)

    def __convert_post(self):
        for post in self.post_list:
            build_post_path = osp.join(self.site_post_dir, post.filename)
            #output_file = codecs.open(build_post_path, 'w', encoding="utf-8")
            post_html = markdown.markdown(post.content)
            #output_file.write(post_html)
            post.html = post_html

