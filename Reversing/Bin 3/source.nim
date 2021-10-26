#nim c -d:release source.nim
#strings | grep JZT
#rot13 decode
import strutils


proc rot13(c: char): char =
  case toLowerAscii(c)
  of 'a'..'m': chr(ord(c) + 13)
  of 'n'..'z': chr(ord(c) - 13)
  else:        c
 
stdout.write "Enter Password: "
var userInput = readLine(stdin)
var flagCharacters = ['J','Z','T','{','0','x','_','g','u','1','5','_','1','5','_','z','0','e','3','_','q','1','s','s','1','p','h','y','g','}']

for index in 0..<userInput.len:
    var currentCHar = rot13((flagCharacters[index]))
    if currentCHar!=userInput[index]:
        echo "Incorrect Password"
        quit 1

echo "Success!"
echo "You got it correct!"
