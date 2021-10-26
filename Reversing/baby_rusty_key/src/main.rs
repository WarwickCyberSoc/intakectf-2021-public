#[macro_use]
extern crate litcrypt;
//trash rust code only obfuscates it further :p
extern crate cursive;
extern crate chrono;
use cursive::align::HAlign;
use cursive::event::{Event};
use cursive::traits::Identifiable;
use cursive::views::{Dialog, EditView, SelectView, TextView};
use cursive::Cursive;

use chrono::prelude::{Utc,Timelike};

// creates unsafe code but it's about the only way for a global var without prostituting a parameter
static mut ALREADY_LICENSED: bool = false;

/* -------- ctrl-c hook stuff ------------ */
extern crate anyhow;
extern crate crossbeam_channel;
use std::time::Duration;
extern crate ctrlc;
use anyhow::Result;
use crossbeam_channel::{bounded, select, tick, Receiver};
/* ------ end of ctrl-c hook stuff ------- */


#[no_mangle]
fn verify_license(license: &str) -> bool{

    if !license.contains("-"){
        return false;
    }
    let mut current_hour = Utc::now().hour().to_string();
    current_hour=format!("{:0>2}",current_hour);
    let key_string = "KEY";
    let key_and_hour = [key_string,&current_hour].join("");

    let key_chunks: Vec<&str> =license.split("-").collect();
  
    if key_chunks.len()!=5{
        return false;
    }else{
        for i in 1..4{
            if key_chunks[i].len()!=5{
                return false;
            }
        }
    }
    let uppercase_license = license.to_uppercase();
    if license!=uppercase_license{
        return false;
    }
    if license.contains("B") || 
       license.contains("G") || 
       &key_chunks[4][3..5]!="33" ||
       ((key_chunks[1].chars().nth(0).unwrap() as u8) < 65) || ((key_chunks[1].chars().nth(0).unwrap() as u8) > 72) ||
       !license.contains("AA") ||
       !license.contains("Z01") ||
       &key_chunks[0]!=&key_and_hour{
        return false;

    }
    //where 23 is the hour in utc
    //e.g: KEY23-AAZ01-CCCCC-CCCCC-CCC33
    return true;
}


fn exit_program() {
    //lib borks terminal so can get in the bin - here's the scuffed part-fix - cope
    std::process::Command::new("reset").status().unwrap();
    print!("\x1B[2J\x1B[1;1H");
    std::process::exit(0);
}

fn license_evaluate_popup(session: &mut Cursive, license: &str) {
    session.add_global_callback(Event::CtrlChar('c'), |s| {
        s.set_screen(0);
    });
    if license.is_empty() {
        // Show error for empty key
        session.add_layer(Dialog::info("Please enter something!"));
    }else if !verify_license(license){
        session.add_layer(Dialog::info("License invalid"))
    }
    
    else {
        //program now licensed
        unsafe {
            ALREADY_LICENSED = true;
        }
        session.add_layer(
            Dialog::around(TextView::new("Success! Program Licensed")).button("Back", |session| {
                //since it's a dialog, we don't have to switch back to menu, can just pop dialog off
                session.pop_layer();
                session.quit();
            }),
        );
    }
}
use_litcrypt!();
fn menu() {
    let mut gcli = cursive::default();
    let mut options_view = SelectView::new().h_align(HAlign::Center);
    //change menu item depending on whether program licensed or not
    if unsafe { !ALREADY_LICENSED } {
        options_view.add_item("1. License", 1);
    } else {
        options_view.add_item("Already Licensed", 1);
    }
    options_view.add_item("2. View Flag", 2);
    options_view.add_item("3. View Hint", 3);
    options_view.add_item("Exit", 99999);
    //when option submitted
    options_view.set_on_submit(move |session, op_code: &u32| {
        if *op_code == 99999 {
            // session.quit();
            exit_program();
        } else if *op_code == 1 {
            // enter_something();
            if unsafe { !ALREADY_LICENSED } {
                //show program licenser screen
                session.set_screen(1)
            } else {
                //show program already licensed confirmation
                session.set_screen(2);
            }
        } else if *op_code==2{
            if unsafe{!ALREADY_LICENSED}{
                session.set_screen(3);
            }else{
                session.set_screen(4);
            }
        } else if *op_code==3{
            session.set_screen(5);
        }


    });
    //add menu to gcli
    gcli.screen_mut().add_layer(
        Dialog::around(options_view)
            .title("Menu")
            .padding_lrtb(1, 1, 1, 0),
    );
    //add new screen, id=1 - licenser
    gcli.add_active_screen();
    let licenser = Dialog::new()
        .title("Enter license")
        .padding_lrtb(1, 1, 1, 0)
        .content(
            EditView::new()
                .on_submit(license_evaluate_popup)
                .with_name("license"),
        )        
        .button("Back", |s|{
            s.set_screen(0);
        })
        .button("Submit", |session| {
            let license = session
                .call_on_name("license", |view: &mut EditView| {
                    // We can return content from the closure
                    view.get_content()
                })
                .unwrap();

            // Run the next step
            license_evaluate_popup(session, &license);
        });

    gcli.screen_mut().add_layer(licenser);
    //add new screen, id = 2 (already licensed)
    gcli.add_active_screen();
    gcli.screen_mut()
        .add_layer(
            Dialog::around(TextView::new("Already Licensed")).button("Ok", |s| {
                //go back to menu
                s.set_screen(0)
            }),
        );

    //add new screen id=3 (not licensed)
    gcli.add_active_screen();
    gcli.screen_mut()
        .add_layer(
            Dialog::around(TextView::new("You must license the program to use this feature"))
                .button("Ok", |s|{
                    //go back to menu
                    s.set_screen(0)
                })
        );

    gcli.add_active_screen();

    gcli.screen_mut()
        .add_layer(
            Dialog::around(TextView::new(lc!("WMG{3z_w4Y_t0_l1cense_the_pr0gr4m}")).h_align(HAlign::Center)));

    
    //add new screen id=5 (show hint)
    gcli.add_active_screen();
    gcli.screen_mut()
        .add_layer(
            Dialog::around(
                TextView::new("Look at the verify_license function. What happens if you get a valid key?")
            )
            .button("Ok", |s|{
                //go back to menu
                s.set_screen(0);
            })
        );

    //set current screen to be menu
    gcli.set_screen(0);
    //run window
    gcli.run();
}

// ctrl-c hook magic https://rust-cli.github.io/book/in-depth/signals.html
fn ctrl_channel() -> Result<Receiver<()>, ctrlc::Error> {
    let (sender, receiver) = bounded(100);
    ctrlc::set_handler(move || {
        let _ = sender.send(());
    })?;

    Ok(receiver)
}

fn main() -> Result<()> {
    /************************
     *       Screens        *
     *       0 - menu       *
     *  1 - License window  *
     * 2 - already licensed *
     *   3 - not licensed   *
     *    4 - show flag     *
     *    5 - show hint     *
     ************************/

    //so the program appears to work properly if using strings or whatever
    let _something: &str="The flag is: ";
    // hook/prevent ctrl-c being used (told you there'd be disgusting code - but I bet you thought it'd be mine... well this is a lib example)
    // since lib end terminal session, reloads are required, the lib has fps anyway
    let ctrl_c_events = ctrl_channel()?;
    //tick reload check duration
    let ticks = tick(Duration::from_millis(50));
    loop {
        select! {
            //reload menu
            recv(ticks) -> _ => {
                    menu();
                    // menu();
            }
            recv(ctrl_c_events) -> _ => {
                //do nothing on ctrl c
                {}
            }
        }
    }

    // Ok(())
}