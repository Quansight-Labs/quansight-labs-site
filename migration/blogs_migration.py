from datetime import datetime
import re
import os
from pathlib import Path
from fnmatch import fnmatch
from pandas import read_csv

# Inputs:
#          CSV from notion DB for new labels and author slugs
#          download the zip file of the old website repo and unzip it in your Downloads folder
#               (or clone it and update the root variable to the correct location)
#          Have a ~/Documents/Quansight/New_Website/ directory where all the new files will be generated
#          this includes the new md files following the same structure, and at the root of this dir a blog_links.md
#          file which will have the list of all files created and detail if they had links to other blogs, labs or llc
#          for manual editing later on.
#          for questions contact @noatamir on gh or slack, or simply ask her for the output :wink:


# getting all the markdown files in the old repository posts directory
root = '~/Downloads/quansight-labs-site-main/posts/'  # replace local file paths if using this script.

pattern = "*.md"

file_paths = []

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            file_paths.append(os.path.join(path, name))

# remove duplicates from list if any
file_paths = list(dict.fromkeys(file_paths))


# defining the replace method
def replace(file_path, text, subs, flags=0):
    with open(file_path, "r+") as file:
        # read the file contents
        file_contents = file.read()
        text_pattern = re.compile(re.escape(text), flags)
        file_contents = text_pattern.sub(subs, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)


# defining the replace date method
def replace_date(file_path, author_slug):
    # open the file
    with open(file_path, "r+") as file:
        # read the file contents
        file_contents = file.read()
        file_contents = re.sub("author: .+", 'author: ' + str(author_slug), file_contents)
        date_pattern = re.search("\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(.+|$)\n", file_contents)
        if date_pattern:
            date_pattern = date_pattern[0].split()[0]
            datetime_conversion = datetime.strptime(date_pattern, '%Y-%m-%d')
            new_date_pattern = datetime.strftime(datetime_conversion, '%B %d, %Y')
            file_contents = re.sub("\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]).+\n", new_date_pattern + "\n",
                                   file_contents)

            file.seek(0)
            file.truncate()
            file.write(file_contents)


# defining the method to add quotes to the blog title
def title_quotes(file_path):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        title_pattern_label = re.search("title: ", file_contents)[0]
        file_contents = re.sub("title: ", title_pattern_label + "'", file_contents)
        title_pattern_titel = re.search("title: \'.+", file_contents)[0]
        file_contents = re.sub("title: \'.+", title_pattern_titel + "'", file_contents)

        file.seek(0)
        file.truncate()
        file.write(file_contents)


# defining the method to drop redundant meta fields
def drops(file_path):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        file_contents = re.sub("---(.+\n){4,9}---", "---", file_contents)
        file_contents = re.sub("slug:.+\n", '', file_contents)

        file.seek(0)
        file.truncate()
        file.write(file_contents)


# defining the method to add new neta data fields for blog categories, hero and fetured images
def adds(file_path):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        text_pattern = re.compile(re.escape('.. category: []'))
        file_contents = text_pattern.sub(
            "description: ''\n.. category: []\nfeaturedImage:\n  src: /posts/\n  alt: 'Lorem ipsum dolor'\nhero:\n  imageSrc: /posts/\n "
            " imageAlt: 'Lorem ipsum dolor'\n---",
            file_contents)

        file.seek(0)
        file.truncate()
        file.write(file_contents)


# defining the method to print references to other labs or Quansight blogs since we will need
# to manually change to whote links
def blog_links(file_path, blog_path, blog):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        labs_links = re.search("https://labs\.quansight\.org/blog/.+", file_contents)
        if labs_links:
            labs_links = labs_links[0]
        else:
            labs_links = "no labs links found"
        llc_links = re.search("https://www\.quansight\.com/post/.+", file_contents)  # https://www.quansight.com/post/
        # performance-for-image-processing-with-cucim
        if llc_links:
            llc_links = llc_links[0]
        else:
            llc_links = "no llc links found"
        file.close()
        with open(blog_path, "r+") as blog_file:
            blog_file.seek(0, 2)
            blog_file.write("\n"+blog+"\n"+labs_links+"\n"+llc_links)
            blog_file.truncate()

# use single file when testing
# file_path="/Users/augustiniv/Documents/Quansight/New_Website/posts/2022/05/the-evolution-of-the-scipy-developer-cli.md"

# read notion csv
notion_db = read_csv("~/Downloads/blog_conversion.csv")

# touch file to collect links mentioned in blogs
blog_links_path = '~/Documents/Quansight/New_Website/blog_links.md'
Path(blog_links_path).touch()


for org_file_path in file_paths:
    with open(org_file_path, 'r+') as org_file:
        content = org_file.read()
        content = content.replace("<!--", "---")
        content = content.replace("-->", "---")

    # touch file_path_new

    file_path_new = org_file_path.replace('~/Downloads/quansight-labs-site-main/',
                                          '~/Documents/Quansight/New_Website/')
    Path(file_path_new).touch()
    with open(file_path_new, 'w') as new_file:
        new_file.write(content)

    print(file_path_new)
    blog_name = re.sub(r'~/Documents/Quansight/New_Website/posts/20\d\d/\d\d/', '', file_path_new)
    blog_name = blog_name.replace(".md", "")
    print(blog_name)
    replace(file_path_new, ".. date: ", ".. published: ")
    notion = notion_db['Title'] == blog_name
    labels = notion_db[notion].Categories
    labels = list(labels.items())[0][1]
    replace(file_path_new, ".. tags: ", '.. category: []')
    adds(file_path_new)
    replace(file_path_new, ".. category: []", ".. category: ["+labels+"]" )
    author_slug = notion_db[notion].author_slugs
    author_slug = list(author_slug.items())[0][1]
    replace(file_path_new, ".. ", '')
    replace_date(file_path_new, author_slug)
    title_quotes(file_path_new)
    drops(file_path_new)
    replace(file_path_new, "\n--- TEASER_END ---\n", '')
    blog_links(file_path_new, blog_links_path, blog_name)

    # manually decide if you replace the links because these blogs were already migrated to the new website,
    # or open an issue to remember to migrate them later on
