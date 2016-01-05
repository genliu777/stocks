#!/bin/gawk
BEGIN {
	FS="\n";
	print FS;
}

{
n = match($0, /_t.push\(\{val:\"([^\"]*)\",val2:\"([^\"]*)\",val3:\"([^\"]*)\"\}\);/, a);
if(n>0) {
	print a[1], a[2], a[3];
}
}
