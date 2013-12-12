import post

def main():
    reader = post.Reader()
    reader.get_history_post()
    reader.get_current_post()

    post_list = reader.current_post_list
    writer = post.writer(post_list)
    
