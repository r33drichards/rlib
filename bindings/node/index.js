const koffi = require('koffi');
const path = require('path');
const os = require('os');

// Determine library extension
let libExt;
if (os.platform() === 'darwin') {
  libExt = 'dylib';
} else if (os.platform() === 'win32') {
  libExt = 'dll';
} else {
  libExt = 'so';
}

// Try multiple library locations
const libLocations = [
  path.join(__dirname, `librlib.${libExt}`),
  path.join(__dirname, '..', '..', 'target', 'release', `librlib.${libExt}`),
];

let libPath = null;
for (const loc of libLocations) {
  try {
    require('fs').accessSync(loc);
    libPath = loc;
    break;
  } catch (e) {
    // Continue to next location
  }
}

if (!libPath) {
  throw new Error(`Could not find librlib.${libExt} in any expected location`);
}

// Load shared library
const lib = koffi.load(libPath);

// Define function signatures
const rlib_add = lib.func('rlib_add', 'int', ['int', 'int']);
const rlib_multiply = lib.func('rlib_multiply', 'int', ['int', 'int']);
const rlib_divide = lib.func('rlib_divide', 'int', ['int', 'int', koffi.out(koffi.pointer('int'))]);
const rlib_error_message = lib.func('rlib_error_message', 'string', ['int']);

const RlibError = {
  OK: 0,
  DIVISION_BY_ZERO: 1,
  INVALID_ARGUMENT: 2
};

function add(a, b) {
  return rlib_add(a, b);
}

function multiply(a, b) {
  return rlib_multiply(a, b);
}

function divide(a, b) {
  const result = [0];
  const error = rlib_divide(a, b, result);

  if (error !== RlibError.OK) {
    const msg = rlib_error_message(error);
    throw new Error(msg);
  }

  return result[0];
}

module.exports = { add, multiply, divide };
