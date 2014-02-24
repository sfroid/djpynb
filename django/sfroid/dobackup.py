import pexpect
child = pexpect.spawn("python manage.py dbbackup")
child.expect("Password: ")
child.sendline("2fDj3bUser\n")
print 'output follows'
print child.before
print 'backup done'
