#!/usr/bin/env node
const path = require('path');
const rlib = require('../../bindings/node');

console.log('rlib Node.js Example');
console.log('====================');
console.log();

// Test add
const sum = rlib.add(10, 5);
console.log(`10 + 5 = ${sum}`);

// Test multiply
const product = rlib.multiply(10, 5);
console.log(`10 * 5 = ${product}`);

// Test exponent
const power = rlib.exponent(2, 8);
console.log(`2 ^ 8 = ${power}`);

// Test divide (success)
const quotient = rlib.divide(10, 5);
console.log(`10 / 5 = ${quotient}`);

// Test divide by zero
try {
  rlib.divide(10, 0);
} catch (err) {
  console.log(`10 / 0 error: ${err.message}`);
}
