// This is for something else
/* this is multiliune comment */
print "one";
print true;

print "complex arithmetic condition";
print 2 + 1;
print 1 + 2 > 3 * 4 == 5 <= 6 != !7;
print -(1 + 2) * 3 == 9 - (4 + 5);
print -1 + 2 * -3;
print 1 + 2 * 3;
print (1 + 2) * (3 - 4);

print "complex global local scope check";
var a = "global a";
var b = "global b";
var c = "global c";
{
  var a = "outer a";
  var b = "outer b";
  {
    var a = "inner a";
    print a;
    print b;
    print c;
  }
  print a;
  print b;
  print c;
}
print a;
print b;
print c;

print "global local addition";
var a2 = 1;
{
  var a2 = a2 + 2;
  print a2;
}

print "uninitialzed var";
var d;
print d;

print "if else condition with and/or operetor";
if (0 or 1)
print "hi" or 2;
else
print nil or "yes";

print "if else condition with and/or operetor";
if (1 and 0)
print "hi" or 2;
else
print nil or "yes";

print "while loop";
var i = 10;
while (i){
  print i;
  i = i - 1;
}

i = 0;
var temp;
print "for loop with break";
for (var b = 1; b < 10; b = b + 1) {
  print b;
  break;
}

print "for loop with continue";
for (var b = 1; b < 10; b = b + 1) {
  if (b == 9){
    print b;
  }
  else{
    continue;
  }
}

var bhakti = -(1 + 2) * 3 == 9 - (4 + 5); // False
print bhakti;

print "complex function and return value check";
fun makeCounter() {
  var i = 0;
  fun count() {
    i = i + 1;
    print i;
  }

  return count;
}

var counter = makeCounter();
counter(); 
counter(); 