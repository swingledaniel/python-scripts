#![feature(generators, generator_trait)]

use std::ops::{Generator, GeneratorState};
use std::vec::Vec;
use std::pin::Pin;

fn main() {
    let mut prime_generator = || {
        let mut primes = Vec::new();
        primes.push(2);
        yield 2;
        let mut i: i64 = 3;
        'outer: loop {
            for p in &primes {
                if i % p == 0 {
                    i += 1;
                    continue 'outer;
                }
            }
            primes.push(i);
            yield i;
            i += 1;
        }
    };
    let m = 2000000;
    let mut sum = 0;
    let mut p = 0;
    while p < m {
        //print!("{}, ", p);
        sum += p;
        match Pin::new(&mut prime_generator).resume() {
            GeneratorState::Yielded(x) => p = x,
            _ => println!("There was a problem with the generator."),

        }
    }
    println!("{}", sum);
}
