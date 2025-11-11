const assert = require('assert');
const rlib = require('..');

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
  } catch (err) {
    console.error(`✗ ${name}`);
    console.error(err);
    process.exit(1);
  }
}

test('add', () => {
  assert.strictEqual(rlib.add(2, 3), 5);
  assert.strictEqual(rlib.add(-1, 1), 0);
  assert.strictEqual(rlib.add(0, 0), 0);
});

test('multiply', () => {
  assert.strictEqual(rlib.multiply(2, 3), 6);
  assert.strictEqual(rlib.multiply(-2, 3), -6);
  assert.strictEqual(rlib.multiply(0, 5), 0);
});

test('exponent', () => {
  assert.strictEqual(rlib.exponent(2, 3), 8);
  assert.strictEqual(rlib.exponent(5, 2), 25);
  assert.strictEqual(rlib.exponent(10, 0), 1);
  assert.strictEqual(rlib.exponent(3, 4), 81);
});

test('divide', () => {
  assert.strictEqual(rlib.divide(6, 2), 3);
  assert.strictEqual(rlib.divide(10, 5), 2);
  assert.strictEqual(rlib.divide(-10, 2), -5);
});

test('divide by zero', () => {
  try {
    rlib.divide(10, 0);
    throw new Error('Expected error for division by zero');
  } catch (err) {
    assert.strictEqual(err.message, 'Division by zero');
  }
});

console.log('\nAll tests passed!');
