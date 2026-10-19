"""SDD rendering layer. All user-controlled text passes through e()."""
from html import escape

def e(value):
    return escape(str(value), quote=True)

def csrf(secret):
    return f'<input type="hidden" name="csrf" value="{e(secret)}">'

def layout(content, session, error=''):
    if session['user_id'] is None:
        account = '<div class="account"><a href="/login">Log in</a><a class="button" href="/register">Join the circle</a></div>'
    else:
        account = f'<div class="account"><span class="username">Hi, {e(session["name"])}</span><form method="post" action="/logout">{csrf(session["csrf"])}<button>Log out</button></form></div>'
    error_html = f'<div class="error" role="alert">{e(error)}</div>' if error else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Campus Circle · Your campus, connected</title><link rel="stylesheet" href="/style.css"></head>
    <body><header><a class="brand" href="/"><span class="logo">c.</span> campus circle<span class="beta">STUDENT COMMUNITY</span></a>{account}</header>
    <div class="layout"><aside><div class="eyebrow">YOUR SPACE</div><a class="nav active" href="/">◉ &nbsp; Community feed</a>
    <div class="sidebar-note"><span class="spark">✳</span><h3>Good things start<br>with a hello.</h3><p>A place for study breaks, new ideas, and the people around you.</p></div><small>Made for campus life.</small></aside>
    <main>{error_html}{content}</main><aside class="right"><div class="info-card"><div class="eyebrow">A SMALL REMINDER</div><h3>People first.<br>Always.</h3>
    <p>Be kind, stay curious, and keep personal information personal.</p><hr><span class="tag">#campuslife</span><span class="tag">#sayhello</span></div>
    <p class="footnote">Campus Circle · Course project<br>A space to connect and learn.</p></aside></div></body></html>'''

def auth(session, registering):
    heading, action = ('Join your campus circle', '/register') if registering else ('Welcome back', '/login')
    name = '<label>Display name<input name="name" maxlength="50" required autocomplete="name"></label>' if registering else ''
    password_type = 'new-password' if registering else 'current-password'
    button = 'Create account' if registering else 'Log in'
    link = '<a href="/login">Already a member? Log in</a>' if registering else '<a href="/register">New here? Create an account</a>'
    return f'''<section class="card auth"><div class="eyebrow">YOUR CAMPUS, CONNECTED</div><h2>{heading}</h2><p>A little closer to the people around you.</p>
    <form action="{action}" method="post">{csrf(session['csrf'])}{name}
    <label>Username<input name="username" minlength="3" maxlength="24" pattern="[A-Za-z0-9_]+" required autocomplete="username"></label>
    <span class="hint">3–24 letters, numbers, or underscores.</span>
    <label>Password<input name="password" type="password" minlength="12" maxlength="128" required autocomplete="{password_type}"></label>
    <span class="hint">12–128 characters.</span><button>{button}</button></form>{link}</section>'''

def home(session, posts):
    invitation = '<a class="button" href="/register">Join the circle ↗</a>' if session['user_id'] is None else '<span class="pill">You’re in the circle</span>'
    heading = f'''<div class="page-title"><div><div class="eyebrow">THE CAMPUS COMMON ROOM</div><h1>Stay in the circle<span>.</span></h1>
    <p>Small updates. Shared moments. Your community.</p></div><span class="pill">● &nbsp; Open to everyone</span></div>
    <section class="welcome"><div><span class="eyebrow">A SEAT AT THE TABLE</span><h2>Your next connection<br>starts here.</h2>
    <p>Share an idea, find your people, or just say hello.</p>{invitation}</div><div class="circle-art" aria-hidden="true"><span>hello!</span></div></section>
    '''
    composer = ''
    if session['user_id'] is not None:
        composer = f'''<section class="card composer"><h2>What’s happening on campus?</h2><form method="post" action="/posts">{csrf(session['csrf'])}
        <label for="post-body">Share a moment</label><textarea id="post-body" name="body" required maxlength="500" placeholder="An idea, a study tip, a little hello…"></textarea>
        <div class="composer-footer"><span class="hint">Text only · Up to 500 characters</span><button>Publish post ↗</button></div></form></section>'''
    rendered = []
    for post in posts:
        rendered.append(f'''<article class="card post"><div class="post-head"><span class="avatar" aria-hidden="true">{e(post['name'][0].upper())}</span>
        <div><strong>{e(post['name'])}</strong> <span class="hint">@{e(post['username'])}</span><time datetime="{e(post['created'])}">{e(post['created'])} UTC</time></div></div>
        <p class="post-body">{e(post['body'])}</p></article>''')
    empty = '<section class="empty"><div class="empty-icon">✳</div><h2>A fresh start for your campus</h2><p>No posts yet. Be the first to share a moment.</p></section>'
    return heading + composer + '<div class="feed-heading"><h2>Community feed</h2><span>Latest 100 · newest first</span></div>' + (''.join(rendered) if rendered else empty)
