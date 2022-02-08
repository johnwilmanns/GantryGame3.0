mod lib;

fn main(){
    // let mut img = image::open("C:/Users/Samir/OneDrive/Documents/Rust Projects/first_project/test.png").unwrap().to_luma8();

    let mut img:Vec<Vec<bool>> = vec![vec![false;50];24];
    img.append(&mut vec![vec![true;50];1]);
    img.append(&mut vec![vec![false;50];3]);
    img.append(&mut vec![vec![true;50];1]);
    img.append(&mut vec![vec![false;50];20]);
    // println!("{:?}", img);


    let results = lib::process_edges(img, 3.0, 3, 4.0, 5.0);
    println!("{:?}", results);
    println!("{} segments", results.len())
}