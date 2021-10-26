#nim c -d:release source.nim
#solution: strings source|grep WM
stdout.write "Enter password: "
var userInput = readLine(stdin)
var flag="WMG{r3v3r51ng_s33ms_e4sy}"
if userInput==flag:
    echo "Success!"
else:
    echo "Invalid Password"