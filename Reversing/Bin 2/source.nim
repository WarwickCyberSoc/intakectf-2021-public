#nim c -d:release source.nim
#strings source | grep GMW
#python3 -c "print('}y5ae_yll43r_ll17s_5\'ti{GMW'[::-1])"
stdout.write("Enter password: ")
var userInput = readLine(stdin)
var result=""
for i in countdown(userInput.high,0):
    result.add(userInput[i])

var flag="}y5ae_yll43r_ll17s_5'ti{GMW"
if result == flag:
    echo "Success!"
else:
    echo "Incorrect password"