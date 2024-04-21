---
layout: post
title: How to Build a Blog with Jekyll (and Hyde, the theme)
---

I did some searching around and couldn't find a good introduction that got you set up quickly with a blog and also had it look pretty. I finally found the helpful tutorial [here](https://jashmehta3300.github.io/making-your-own-blog/) on how to set up the Hyde theme and decided that I will add some helpful hints. 

### Downloading Ruby
Go [here](https://rubyinstaller.org/downloads/) and find your desired Ruby version. 
If you don't know what system type you have, search up 'System Information' in your start menu search bar and look under 'System Summary' and 'System Type'.

P.S. I did end up downlading the ruby with the dev kit. 

Running on MacOS.
At first I wanted to run this on MacOS, but ran into a lot of problems. One of them being that ruby is already installed into the MacOS system, but because of that, you can't edit any of the files. It is also heavily discouraged to use sudo to override the safe guards. 

I ended up trying this [suggestion](https://stackoverflow.com/questions/51126403/you-dont-have-write-permissions-for-the-library-ruby-gems-2-3-0-directory-ma) to no avail. I also ran into homebrew issues which a brew update-reset fixed. 

### Downloading Git
Download Git [here](https://git-scm.com/download/win)

My 'git' command is still not being recognized by my terminal!
You probably haven't set your PATH correctly. 
You will need to add both:
- C:\Program Files\Git\bin\
- C:\Program Files\Git\cmd\

On Windows 10 you [can](https://stackoverflow.com/questions/4492979/error-git-is-not-recognized-as-an-internal-or-external-command):
1. Search for 'environment variable' on the start menu
2. Select 'Edit the system environment variables'
3. Click 'Environment Variables' at the bottom
4. Click on the 'Path' entry
5. Using the 'New' button, add two entries, one for each Git path listed above

### Downloading VSCode
You are more than welcome to use your text editor of choice. 
I downloaded [VSCode](https://code.visualstudio.com/download). I did find a peculiar issue: when I download a new package, in order for my terminal to refresh, closing a window and reopening a window wasn't enough. I had to close VSCode as a whole and then reopen it. 

### Install Jekyll
Run gem install jekyll

### Install Dependencies
Needed for [Poole](https://github.com/poole/poole#usage), which is what Hyde is built on:
gem install jekyll jekyll-gist jekyll-sitemap jekyll-seo-tag

Needed for [Hyde](https://github.com/poole/hyde):
gem install jekyll-paginate jekyll-gist redcarpet

Needed for [Jekyll](https://jekyllrb.com/docs/):
gem install bundler

### Enter the edits from the blog

### Add plugins to Gem File

### Bundle Commands
Bundle is...

bundle init
bundle install
bundle exec jekyll serve