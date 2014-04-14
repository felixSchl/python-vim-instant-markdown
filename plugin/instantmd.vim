" vim: set fdm=marker :
let s:scriptfolder = expand('<sfile>:p:h').'/md_instant'

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif


let b:instantmd_fail=0
python <<EOF
try:
    import markdown, pygments
except ImportError:
    print("Error: Required `markdown` and `pygments` modules")
    vim.eval('let b:instantmd_fail=1')
EOF
if (b:instantmd_fail==1)
    finish
endif

python <<EOF
import vim, time
sys.path.append(vim.eval('s:scriptfolder'))
from instantmd import InstantMarkdown
INSTANT = InstantMarkdown()
EOF

com! -nargs=* Instantmd             call s:start()
com! -nargs=* InstantmdStartServer  call s:startDaemon()
com! -nargs=* InstantmdStartBrowser call s:startBrowser()
com! -nargs=* InstantmdStopServer   call s:killDaemon()

aug python-vim-instant-markdown-g
    au VimLeave * call s:killDaemon()
aug END

fu! s:update()
    if !exists('b:changedtickLast')
        let b:changedtickLast = b:changedtick
    elseif b:changedtickLast != b:changedtick
        let b:changedtickLast = b:changedtick
        call s:refresh()
    endif
endfu

fu! s:refresh()
python << EOF
INSTANT.send_markdown(vim.current.buffer)
EOF
endfu

fu! s:start()
    call s:startDaemon()
    call s:startBrowser()
    call s:initBuffer()
python << EOF
import time
time.sleep(3)
EOF
    call s:refresh()
endfu

fu! s:initBuffer()
    aug python-vim-instant-markdown
        au! * <buffer>
        au BufEnter <buffer> call s:refresh()
        au CursorHold,CursorHoldI,CursorMoved,CursorMovedI <buffer> call s:update()
    aug END
    call s:refresh()
endfu

" Daemon {{{
fu! s:startBrowser()
python <<EOF
if not INSTANT.running:
    INSTANT.start_threads()
INSTANT.start_browser()
EOF
endfu

fu! s:startDaemon()
python << EOF
if not INSTANT.running:
    INSTANT.start_threads()
    import sys, time
    sys.stdout = open(os.path.devnull, 'w')
    sys.stderr = open(os.path.devnull, 'w')
EOF

    aug python-vim-instant-markdown-g
        au FileType markdown call s:initBuffer()
        au FileType pandoc call s:initBuffer()
    aug END
endfu

fu! s:killDaemon()
    au! python-vim-instant-markdown * <buffer>
python << EOF
if INSTANT.running:
    INSTANT.stop_threads()
EOF
endfu
" }}}

