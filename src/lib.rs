// use image::GenericImageView;
// use image::Pixel;
use std::time::Instant;
use pyo3::prelude::*;


#[pyfunction]
fn process_image(img: Vec<Vec<bool>>, area_cut: f64, min_pixels: usize, min_len: f64, bind_dist: f64) -> PyResult<Vec<Vec<(usize, usize)>>> {

    
    // let now = Instant::now();


    // // let mut img = edge_detection::canny(img, 2.0, 0.2, 0.05).as_image().to_luma8();

    // let elapsed = now.elapsed();
    // println!("Cannied in: {:.2?}", elapsed);
    let mut is_empty = true;
    for row in img.iter(){
        for val in row.iter(){
            if *val{
                // println!("found hot");
                is_empty = false;
            }
        }
    }
    if is_empty {
        return Ok(Vec::new());
    }

    let segments = process_edges(img, area_cut, min_pixels, min_len, bind_dist);

    // println!("{:?}", segments);


    Ok(segments)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(process_image, m)?)?;

    Ok(())
    
}



pub fn process_edges(mut img: Vec<Vec<bool>>, area_cut: f64, min_pixels: usize, min_len: f64, bind_dist: f64)->Vec<Vec<(usize, usize)>>{

    let now = Instant::now();

    let mut points = find_endpoints(&mut img);
    // println!("endpoints: {:?}", points);
    // let mut path: Vec<(u32,u32)> = Vec::with_capacity(points.len() as usize);
    let mut sorted_points = sort_pixels(&mut img, &mut points);
    // println!("sorted_points: {:?}", sorted_points);

    area_cull(&mut sorted_points, area_cut, min_pixels);

    line_len_cull(&mut sorted_points, min_len);

    bind_segments(&mut sorted_points, bind_dist);
    // println!("{:?}", sorted_points[0]);

    // test(&mut img);

    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);

    sorted_points

}

fn bind_segments(segments:&mut Vec<Vec<(usize,usize)>>, join_dist: f64){
    let mut index = 0;
    while index < segments.len()-1{
        index+=1;
        // println!("{}", segments[index].len());
        // let seg1 = &mut segments[index-1];
        // let seg2 = &mut segments[index];

        if dist(*segments[index-1].last().unwrap(), *segments[index].first().unwrap()) < join_dist{
            
            let mut seg2 = segments.remove(index);
            segments[index-1].append(&mut seg2);

            // println!("{}", "removed");
            // segments.remove(index-1);
            index -= 1;
        }
        
    }
}

fn seg_len(seg:&Vec<(usize,usize)>)->f64{

    let mut length = 0.0;

    for index in 0..seg.len()-1{
        let p1 = seg[index];
        let p2 = seg[index+1];
        length+= dist(p1, p2);
        // TODO: maybe use primitive here
        // println!("{:?}, {:?}", p1, p2);
    }
    // println!("{}", length);
    length
    
}
fn line_len_cull(segments:&mut Vec<Vec<(usize,usize)>>, min_len: f64){
    let mut index = 0;
    while index < segments.len(){
        index+=1;
        // println!("{}", segments[index].len());
        if seg_len(&segments[index-1]) < min_len{
            
            // println!("{}", "removed");
            segments.remove(index-1);
            index -= 1;
        }
        
    }
}

fn dist_primitive(a: (usize,usize), b: (usize,usize))->u32{
    (a.0 as i32 - b.0 as i32).abs() as u32 + (a.1 as i32 - b.1 as i32).abs() as u32
}
fn dist(a: (usize,usize), b: (usize,usize))->f64{
    ((a.0 as f64 - b.0 as f64).powi(2) + (a.1 as f64 - b.1 as f64).powi(2)).sqrt()
}
fn area(a: (usize,usize), b: (usize,usize), c: (usize,usize))->f64{
    let l1 = dist(a,b);
    let l2 = dist(b,c);
    let l3 = dist(a,c);

    let p = (l1 + l2 + l3)/2_f64;
    (p * (p-l1) * (p-l2) * (p-l3)).abs().sqrt()
}

fn area_cull(segments:&mut Vec<Vec<(usize,usize)>>, area_cut: f64, min_pixels: usize){
    let mut index = 0;
    while index < segments.len(){
        index+=1;
        // println!("{}", segments[index].len());
        if segments[index-1].len() < min_pixels{
            // println!("{}", "removed");
            segments.remove(index-1);
            index -= 1;
        }
    }

    for seg in segments.iter_mut(){
        let mut index = 0;
        while index < seg.len()- 2{
            index += 1;
            if area(seg[index-1], seg[0+index], seg[1+index]) < area_cut{
                seg.remove(index);
                index -= 1;
            }
        }

    }
}


fn sort_pixels(img:&mut Vec<Vec<bool>>, endpoints:&mut Vec<(usize, usize)>)->Vec<Vec<(usize,usize)>>{

    

    let dim = (img.len(), img[0].len());

    let offsets: [(i32, i32); 8] = [(-1,0), (0, -1), (0,1), (1, 0), (1,1), (1,-1), (-1,1), (-1,-1)];
    let mut x = endpoints[0].0;
    let mut y = endpoints[0].1;
    endpoints.remove(0);
    img[y][x] = false;
    // segment
    // let mut dir = (0_i32, 0);
    let mut segments: Vec<Vec<(usize,usize)>> = Vec::new();
    let mut segment: Vec<(usize,usize)>= Vec::new();
    segment.push((x,y));

    'outer: loop {
        
        
        for offset in offsets{

            let pos = (((x as i32) + offset.0) as usize, ((y as i32) + offset.1) as usize);
            if pos.0 >= dim.0 || pos.1 >= dim.1{
                continue;
            }

            if img[pos.1][pos.0]{
                // println!("{:?}", pos);
                img[pos.1][pos.0] = false;
                segment.push(pos);
                x = pos.0;
                y = pos.1;
                continue 'outer;
                // return pos;
            }
        }

        let mut mindist = std::u32::MAX;
        let mut min_index = std::usize::MAX;
        for (index, pos) in endpoints.iter().enumerate(){
            let dist = dist_primitive(*pos, (x,y));
            if dist < mindist{
                if img[pos.1][pos.0]{
                    mindist = dist;
                    min_index = index;
                }
                // TODO: remove from endpoints
            }
        }
        if min_index != std::usize::MAX {
            // println!("breaking at {:?}", (x,y));
            // if (x,y) != (0,0){
            //     panic!();
            // }
            segments.push(segment);
            segment = Vec::new();

            let pos = endpoints.swap_remove(min_index);
            img[pos.1][pos.0] = false;
            segment.push(pos);
            x = pos.0;
            y = pos.1;
        } else {
            break;
        }

        
        
    }

    // TODO: this is just for debugging, maybe fix this
    let mut i = 0;

    for row in img.iter(){
        for val in row.iter(){
            if *val{
                // println!("found hot");
                i+=1;
            }
        }
    }

    println!("there are {} leftover pixels that will not make it into the final image", i);

    // segments.remove(0);
    if !segment.is_empty(){
        segments.push(segment);
    }
    segments
}

fn find_endpoints(img: &mut Vec<Vec<bool>>)->Vec<(usize,usize)>{

    let mut endpoints: Vec<(usize,usize)> = Vec::new();

    // TODO: only iterate thru hot pixels
    // let reference = image::open("/Users/samirbeall/first_project/test.png").unwrap().to_luma8();
    for (y, row) in img.iter().enumerate(){
        for (x, val) in row.iter().enumerate(){
            if *val {
                if is_endpoint(&img, x as usize, y as usize){
                    endpoints.push((x as usize, y as usize));
                }
            }
        }
    }
    endpoints
}

// fn is_endpoint(img:& Vec<Vec<bool>>, x: usize, y: usize)->bool{

//     let dim = (img[0].len(), img.len());


//     let offsets: [(i32, i32); 4] = [(-1,0), (0, -1), (0,1), (1, 0)];

//     let mut dir = (0_i32, 0);

//     for offset in offsets{

//         let pos = (((x as i32) + offset.0) as usize, ((y as i32) + offset.1) as usize);
//         if pos.0 >= dim.0 || pos.1 >= dim.1{ // TODO: figure out why this shouldn't be >=
//             continue;
//         }

//         if img[pos.1][pos.0]{
//             if dir != (0,0){
//                 return false;
//             }
//             dir = offset;
//         }
//     }
//     if dir == (0,0){
//         return false;
//     } else if dir.0 == 0{
//         for shift in -1..=1{
//             let pos= (((x as i32) + shift) as usize, ((y as i32) - dir.1) as usize);
//             if pos.0 >= dim.0 || pos.1 >= dim.1{
//                 continue;
//             }
//             if img[pos.1][pos.0]{
//                 return false;
//             }
//         }
        
//         return true;
//     } else if dir.1 == 0{
//         for shift in -1..=1{
//             let pos= (((x as i32) - dir.0) as usize, ((y as i32) + shift) as usize);
//             if pos.0 >= dim.0 || pos.1 >= dim.1{
//                 continue;
//             }
//             if img[pos.1][pos.0]{
//                 return false;
//             }
//         }
        
//         return true;
//     } 

//     false

    
    
// }



// fn is_endpoint(img:& Vec<Vec<bool>>, x: usize, y: usize)->bool{

//     let dim = (img[0].len(), img.len());


//     let offsets: [(i32, i32); 8] = [(-1,0), (0, -1), (0,1), (1, 0), (1,1), (1,-1), (-1,1), (-1,-1)];

//     let mut has_neighbor = false;

//     for offset in offsets{

//         let pos = (((x as i32) + offset.0) as usize, ((y as i32) + offset.1) as usize);
//         if pos.0 >= dim.0 || pos.1 >= dim.1{ // TODO: figure out why this shouldn't be >=
//             continue;
//         }

//         if img[pos.1][pos.0]{
//             if has_neighbor{
//                 return false;
//             }
//             has_neighbor = true;
//         }
//     }
//     return has_neighbor
// }


fn is_endpoint(img:& Vec<Vec<bool>>, x: usize, y: usize)->bool{

    let dim = (img[0].len(), img.len());


    // let offsets: [(i32, i32); 8] = [(-1,0), (0, -1), (0,1), (1, 0), (1,1), (1,-1), (-1,1), (-1,-1)];
    let offsets: [(i32, i32); 8] = [(1,0), (1, 1), (0,1), (-1, 1), (-1,0), (-1,-1), (0,-1), (1,-1)];


    for (i,offset) in offsets.iter().enumerate(){

        let pos = (((x as i32) + offset.0) as usize, ((y as i32) + offset.1) as usize);
        if pos.0 >= dim.0 || pos.1 >= dim.1{ // TODO: figure out why this shouldn't be >=
            continue;
        }

        if img[pos.1][pos.0]{

            let first_part = &offsets[0..i-1];
            let second_part = &offsets[i+2..];
            for offset in first_part.iter().chain(second_part){
                let pos = (((x as i32) + offset.0) as usize, ((y as i32) + offset.1) as usize);
                if pos.0 >= dim.0 || pos.1 >= dim.1{ // TODO: figure out why this shouldn't be >=
                    continue;
                }

                if img[pos.1][pos.0]{
                    return false;
                }

            }
            return true;

        }
    }
    false
    // return has_neighbor
}