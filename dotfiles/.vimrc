set nocompatible

colorscheme default

" Default TAB/SPACE config
set expandtab
set tabstop=4
set softtabstop=4
set shiftwidth=4

set number
set nobackup
set showcmd
set autoindent
set noincsearch
set wildmenu
"set ignorecase

syntax on
filetype on

" current line highlight
set cursorline
highlight Cursorline cterm=bold

" custom statusline
set statusline=
set statusline+=%f
set statusline+=[%{strlen(&fenc)?&fenc:'none'}
set statusline+=,%{&ff}]
set statusline+=%m
set statusline+=%r
set statusline+=%y
set statusline+=%=
set statusline+=Символ:'0x%B'
set statusline+=\ Колонка:%02c
set statusline+=\ Линия:%l/%L
set statusline+=(%P)
set laststatus=2

execute pathogen#infect()
execute pathogen#helptags()

" vim-airlineconfig
let g:airline#extensions#tabline#enabled = 1

if !exists('g:airline_symbols')
  let g:airline_symbols = {}
endif

let g:airline#extensions#branch#enabled=1
let g:airline#extensions#hunks#enabled=1
let g:airline#extensions#wordcount#enabled = 0
let g:airline#extensions#whitespace#enabled = 1
let g:airline#extensions#whitespace#checks = [ 'indent', 'trailing', 'mixed-indent-file' ]

let g:airline_left_sep = '▶'
let g:airline_right_sep = '◀'
let g:airline_symbols.linenr = '␤'
let g:airline_symbols.branch = '⎇'
let g:airline_symbols.paste = 'ρ'
let g:airline_symbols.notexists = '∄'
let g:airline_symbols.whitespace = 'Ξ'

" Autocmd config
if has("autocmd")
    autocmd FileType make setlocal tabstop=8 softtabstop=8 shiftwidth=8 noexpandtab
    autocmd FileType yaml setlocal tabstop=2 softtabstop=2 shiftwidth=2 expandtab
endif

"Keyboard mapping
"map <F1>:help<CR>
map <F2> <ESC>:w<CR>
map <F3> :tabprev <CR>
map <F4> :tabnext <CR>
map <F5> :tabnew <CR>
map <F6> :!python3 %<CR>
map <F7> :NERDTreeToggle <CR>
