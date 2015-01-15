
import twopence

config = twopence.Config()

target = config.target("client");
print "target name    ", target.name;
print "target ipv4addr", target.ipaddr;
print "target ipv4addr", target.property("ip6addr")

target.inject("/etc/hosts", "/tmp/injected", mode = 0660)
target.extract("/etc/hosts", "hosts.copy", user = "okir")

target.run("/bin/pwd");

status = target.run("/bin/blablabla")
print "Return code is", status.code
if not(status):
  print "Command failed as expected, message:", status.message

status = target.run("kill -9 $$")
print "Return code is", status.code
if not(status):
  print "Command failed as expected, message:", status.message

out = bytearray();
target.run("/bin/ls", stdout = out)
print "Output has", len(out), "bytes"

print "Verify commandline attribute"
cmd = twopence.Command("/bin/ls");
if cmd.commandline != "/bin/ls":
	print "Bad commandline:", cmd.commandline
else:
	print "Good, commandline attribute returns /bin/ls"

print "Verify user attribute"
cmd = twopence.Command("/bin/ls", user = "joedoe");
if cmd.user != "joedoe":
	print "Bad user attribute:", cmd.user, "(expected joedoe)"
else:
	print "Good, user attribute returns joedoe"

cmd = twopence.Command("/bin/ls", user = "okir");
cmd.suppressOutput()
cmd.stderr = None
target.run(cmd)
print "command stdout=", type(cmd.stdout), "; stderr=", type(cmd.stderr);
print "Output has", len(cmd.stdout), "bytes"

print "Connect stdin to a file"
cmd = twopence.Command("/usr/bin/wc", stdin = "/etc/hosts");
target.run(cmd)

print "Test capturing with shared buffer"
cmd = twopence.Command("echo error>&2");
status = target.run(cmd);
if len(status.stdout) == 0:
  print "bad, expected stderr to be captured in stdout buffer"
else:
  print "stdout buffer has", len(status.stdout), "bytes; good"

print "Test capturing with separate buffers"
cmd = twopence.Command("echo error>&2", stdout = bytearray(), stderr = bytearray());
status = target.run(cmd);
if len(status.stderr) == 0:
  print "bad, expected stderr to be captured in stderr buffer"
else:
  print "stderr buffer has", len(status.stderr), "bytes; good"
if len(status.stdout) != 0:
  print "bad, expected stdout to be empty"
else:
  print "stdout buffer has", len(status.stdout), "bytes; good"