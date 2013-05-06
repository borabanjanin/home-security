#!/usr/bin/python
import cgi
print "Content-type: text/html"
print
form = cgi.FieldStorage()
laptops = form.getvalue('laptops','0')
desktops = form.getvalue('desktops','0')

print """
<html>
<body>
<form action='configuration.py'>
How many laptops do you own?&nbsp;
<input type='radio' checked name='laptops' value='0' />0&nbsp;
<input type='radio' name='laptops' value='1' />1&nbsp;
<input type='radio' name='laptops' value='2' />2
<p>
How many desktops do you own?&nbsp;
<input type='radio' checked name='desktops' value='0' />0&nbsp;
<input type='radio' name='desktops' value='1' />1&nbsp;
<input type='radio' name='desktops' value='2' />2
<p>
<input type='submit' />
<p>
You own %d computers.
</form>
</body>
</html>""" % (int(laptops)+int(desktops))



