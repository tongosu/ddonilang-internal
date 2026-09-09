use ddonirang_tool::repl_workflow::ReplSession;
use std::io::{self, Write};

pub fn repl(source_profile_identity: &str) -> Result<(), String> {
    let mut session = ReplSession::new(source_profile_identity)?;
    let stdin = io::stdin();

    println!("또니랑 REPL ({source_profile_identity})");
    println!(":hash - 현재 state_hash 출력");
    println!(":reset - 상태 초기화");
    println!(":quit - 종료");
    println!();

    loop {
        print!("또니랑> ");
        io::stdout().flush().map_err(|e| e.to_string())?;

        let mut line = String::new();
        if stdin.read_line(&mut line).map_err(|e| e.to_string())? == 0 {
            break;
        }

        let line = line.trim();
        if line == ":quit" || line == ":q" {
            break;
        }
        if line == ":hash" || line == ":h" {
            println!("state_hash={}", session.state_hash());
            continue;
        }
        if line == ":reset" {
            session.reset()?;
            println!("reset=ok");
            continue;
        }
        if line.is_empty() {
            continue;
        }

        match session.execute_line(line) {
            Ok(stdout) => print!("{stdout}"),
            Err(err) => {
                eprintln!("{}", err);
            }
        }
    }

    Ok(())
}
