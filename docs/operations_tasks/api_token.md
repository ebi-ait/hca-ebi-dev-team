---
layout: default
title: API Tokens
parent: Operations tasks
---

API Tokens are used to gain access to ingest api.

An easy way to get the token from a logged in session is to use the bookmarklet.



Instructions:
1. Create a bookmarklet in the browser's bookmark list with the following code as the URL

```javascript
javascript:(async function(navigator) { navigator.clipboard.writeText(Object.entries(window.localStorage).filter(([k,v])=>k.indexOf('elixir')>0).map(([k,v])=>v).map(JSON.parse)[0].access_token)})(navigator)
```

2. Log in to ingest ui
3. Click the copy token bookmark
4. The token will be copied to the clipboard.
