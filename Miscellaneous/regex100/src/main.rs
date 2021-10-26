//https://regex101.com/r/tLT3gZ/1
extern crate fancy_regex;
use fancy_regex::Regex;
use std::io::Write;
use std::process::Command;
fn main(){
    println!("Match the pattern to get the flag");
    println!("Pattern: {}",r"^[A-Z]{3}{\w{3,}_\w{4,7}_\w{2}}$");
    //can't be bothered to strip new line so just have it at end of pattern
    //no one will know ;)
    let pattern = Regex::new(r"^[A-Z]{3}{\w{3,}_\w{4,7}_\w{2}}\n$").unwrap();
    let mut user_input = String::new();
    print!("Enter string: ");
    std::io::stdout().flush().ok();
    std::io::stdin().read_line(&mut user_input).unwrap();
    

    let result = pattern.is_match(&user_input);
    if result.unwrap(){
        let output = Command::new("sh")
                            .arg("-c")
                            .arg("cat flag.txt")
                            .output()
                            .expect("failed to execute process");
        let flag = String::from_utf8(output.stdout).unwrap();
        println!("Flag: {}",flag);
    }else{
        println!("Invalid String");
    }


}