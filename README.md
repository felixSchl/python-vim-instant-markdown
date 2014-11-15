#python-vim-instant-markdown

> Renders a markdown preview as you type

This is a fork of isnowfy's [python-vim-instant-markdown][isnowfy-repo].

This fork brings the following improvements:

* Switching buffers to another markdown or pandoc file will automatically update
  the browser to show that buffer.
* Ability to start / stop the server.
* Don't jump to bottom of page on each refresh.

Thanks for scturtle and his vim-instant-markdown-py project

##Requirements
* python and markdown and pygments package
* vim should have python support, you can check it `vim --version | grep +python`

##Installation
* `pip install markdown` and `pip install pygments`
* put `instandmd.vim` and the folder `instantmd` in `~/.vim/plugin` or use pathogen

##Run
* `:Instantmd` to start the server and launch a browser*
* `:InstantmdStartServer` to start the server
* `:InstantmdStopServer` to stop the server
* `:InstantmdStartBrowser` to start the browser

\* If the browser does not open automatically, please open the browser and load
<http://localhost:7000/>


[isnowfy-repo]:https://github.com/isnowfy/python-vim-instant-markdown
