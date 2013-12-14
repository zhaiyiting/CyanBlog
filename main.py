import post
import build

def main():
    reader = post.Reader()
    reader.get_history_post()
    reader.get_current_post()

    post_list = reader.current_post_list
    writer = post.Writer(post_list)
    builder = build.Builder(post_list)
    builder.build_post()
    builder.build_home()
    builder.build_archive()
    builder.build_category()
    builder.build_tag()
    builder.build_aboutme()
    builder.build_rss()

    reader.dump()


if __name__ == "__main__":
    main()
