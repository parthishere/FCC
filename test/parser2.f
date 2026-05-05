
var start = clock_ms();
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
var end = clock_ms();
print end - start;