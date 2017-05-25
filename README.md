# sustc_framework

This is a framework for simple spiders to login CAS system of SUSTC services.

An example gives an idea of logging into network of dormitory using this framework.

[fuck_courses_one_key_select](https://github.com/BorisChenCZY/fuck_courses_one_key_select) is also develped on this framework.
However, this code is not rubosty at all. Maybe some improvement will be done on it soon.

sustc_framework is developed by an old project called [sakai_getter](https://github.com/BorisChenCZY/sakai-getter), 

Dependency:
- Python3.x
- BeautifulSoup4
- lxml
- requests

To get an instance, you need to pass your username, password and the site you want to login

After you create an instance, you should call login method.:

```python
sustc = SUSTech('username', 'password', 'http://jwxt.sustc.edu.cn/jsxsd')
assert sustc.login() == True
```

You can use get, post method to get HTTP response.
```
html = sustc.get('http://jwxt.sustc.edu.cn/jsxsd')
```
Variable html contains the html content, which is a sting. You can use beautifulsoup or pyquery to parse the string variable.

So sorry for doing only a little work. star if you like it~
