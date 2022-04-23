mod lib;
use std::time::Instant;

fn main(){
    // let mut img = image::open("C:/Users/Samir/OneDrive/Documents/Rust Projects/first_project/test.png").unwrap().to_luma8();

    let mut img:Vec<Vec<bool>> = vec![vec![false;5000];240];
    img.append(&mut vec![vec![true;5000];1]);
    img.append(&mut vec![vec![false;5000];3]);
    img.append(&mut vec![vec![true;5000];1]);
    img.append(&mut vec![vec![false;5000];200]);
    // println!("{:?}", img);

    // let now = Instant::now();
    let results = lib::process_edges(img, 3.0, 3, 4.0, 5.0);
    // let elapsed = now.elapsed();
    // println!("All runs took: {:.2?}", elapsed);

    println!("{:?}", results);
    println!("{} segments", results.len())
}