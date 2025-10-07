#!/usr/bin/env python3
from pathlib import Path
import struct
from io import BytesIO
import zipfile
import os
import shutil

PK_LOCAL = b"PK\x03\x04"
PK_EOCD  = b"PK\x05\x06"
PK_CENTRAL = b"PK\x01\x02"

def find_zip_boundaries(buf: bytes):
    """找到所有可能的ZIP邊界"""
    results = []
    
    # 找到所有EOCD記錄
    pos = 0
    while True:
        eocd_pos = buf.find(PK_EOCD, pos)
        if eocd_pos == -1:
            break
            
        # 檢查是否有足夠的空間讀取EOCD
        if eocd_pos + 22 > len(buf):
            pos = eocd_pos + 1
            continue
            
        try:
            # 讀取EOCD結構
            comment_len = struct.unpack_from("<H", buf, eocd_pos + 20)[0]
            eocd_end = eocd_pos + 22 + comment_len
            
            if eocd_end > len(buf):
                pos = eocd_pos + 1
                continue
                
            # 讀取Central Directory信息
            cd_offset = struct.unpack_from("<L", buf, eocd_pos + 16)[0]
            cd_size = struct.unpack_from("<L", buf, eocd_pos + 12)[0]
            total_entries = struct.unpack_from("<H", buf, eocd_pos + 10)[0]
            
            # 尋找對應的ZIP開始位置
            # 方法1: 從CD偏移量往前找第一個Local Header
            zip_start = None
            if cd_offset < len(buf):
                # 往前搜索Local Header
                search_start = max(0, cd_offset - 2000000)  # 擴大搜索範圍
                local_pos = buf.find(PK_LOCAL, search_start, cd_offset)
                if local_pos != -1:
                    zip_start = local_pos
                    
            # 方法2: 如果方法1失敗，直接使用cd_offset作為起始點
            if zip_start is None:
                zip_start = cd_offset
                
            results.append({
                'start': zip_start,
                'end': eocd_end,
                'eocd_pos': eocd_pos,
                'cd_offset': cd_offset,
                'cd_size': cd_size,
                'entries': total_entries
            })
            
        except struct.error:
            pass
            
        pos = eocd_pos + 1
    
    return results

def extract_zip_by_index(blob_path: str, outdir: str, index: int = -1):
    buf = Path(blob_path).read_bytes()
    zip_boundaries = find_zip_boundaries(buf)
    
    if not zip_boundaries:
        print("[!] No ZIP boundaries found.")
        return
    
    print(f"[+] Found {len(zip_boundaries)} potential ZIP archives:")
    for i, zb in enumerate(zip_boundaries):
        size = zb['end'] - zb['start']
        print(f"  [{i}] Range: {zb['start']}-{zb['end']} (size: {size} bytes, entries: {zb['entries']})")
    
    # 選擇要提取的ZIP（默認最後一個）
    if index < 0:
        index = len(zip_boundaries) + index
    
    if index < 0 or index >= len(zip_boundaries):
        print(f"[!] Invalid index {index}")
        return
    
    zb = zip_boundaries[index]
    print(f"[+] Extracting ZIP [{index}]: range {zb['start']}-{zb['end']}")
    
    zip_data = buf[zb['start']:zb['end']]
    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    
    # 嘗試多種提取方法
    success = False
    
    # 方法1: 直接提取
    try:
        with zipfile.ZipFile(BytesIO(zip_data), 'r') as z:
            print(f"[+] ZIP file list: {z.namelist()}")
            z.extractall(outdir_path)
        print(f"[+] Successfully extracted to {outdir}")
        success = True
    except Exception as e:
        print(f"[!] Method 1 failed: {e}")
    
    # 方法2: 如果CD offset看起來不對，嘗試重新計算
    if not success and zb['cd_offset'] > len(zip_data):
        print("[+] Trying to fix CD offset...")
        try:
            # 重新計算相對於ZIP開始的偏移量
            adjusted_data = bytearray(zip_data)
            eocd_offset_in_data = zb['eocd_pos'] - zb['start']
            new_cd_offset = zb['cd_offset'] - zb['start']
            
            # 更新EOCD中的CD偏移量
            struct.pack_into("<L", adjusted_data, eocd_offset_in_data + 16, new_cd_offset)
            
            with zipfile.ZipFile(BytesIO(adjusted_data), 'r') as z:
                print(f"[+] ZIP file list: {z.namelist()}")
                z.extractall(outdir_path)
            print(f"[+] Successfully extracted with adjusted CD offset to {outdir}")
            success = True
        except Exception as e:
            print(f"[!] Method 2 failed: {e}")
    
    # 總是保存原始ZIP文件供檢查
    zip_file_path = outdir_path / f"extracted_{index}.zip"
    zip_file_path.write_bytes(zip_data)
    print(f"[+] Saved ZIP as {zip_file_path}")
    
    if not success:
        print(f"[+] First 64 bytes: {zip_data[:64].hex()}")
        print(f"[+] Last 64 bytes: {zip_data[-64:].hex()}")

def extract_zip_recursive(zip_path: str, outdir: str, max_depth: int = 100):
    """遞歸提取巢狀ZIP文件直到找到最終內容"""
    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    
    current_file = Path(zip_path)
    depth = 0
    
    print(f"[+] Starting recursive extraction from {zip_path}")
    
    while depth < max_depth:
        print(f"[+] Depth {depth}: Processing {current_file.name}")
        
        try:
            with zipfile.ZipFile(current_file, 'r') as z:
                files = z.namelist()
                print(f"    Files in archive: {files}")
                
                # 提取所有文件到當前深度目錄
                depth_dir = outdir_path / f"depth_{depth}"
                depth_dir.mkdir(exist_ok=True)
                z.extractall(depth_dir)
                
                # 檢查是否有ZIP文件需要進一步解壓
                zip_files = [f for f in files if f.lower().endswith('.zip')]
                
                if not zip_files:
                    # 沒有更多ZIP文件，檢查是否有其他有趣的文件
                    print(f"[+] Final extraction at depth {depth}")
                    print(f"[+] Final files: {files}")
                    return depth_dir
                
                # 選擇第一個ZIP文件繼續解壓
                next_zip = zip_files[0]
                current_file = depth_dir / next_zip
                depth += 1
                
        except zipfile.BadZipFile as e:
            print(f"[!] Bad ZIP file at depth {depth}: {e}")
            break
        except Exception as e:
            print(f"[!] Error at depth {depth}: {e}")
            break
    
    print(f"[!] Reached maximum depth {max_depth} or stopped due to error")
    return outdir_path

def extract_all_nested_levels(blob_path: str, outdir: str):
    """提取所有巢狀層級的ZIP文件"""
    buf = Path(blob_path).read_bytes()
    zip_boundaries = find_zip_boundaries(buf)
    
    if not zip_boundaries:
        print("[!] No ZIP boundaries found.")
        return
    
    print(f"[+] Found {len(zip_boundaries)} potential ZIP archives")
    
    # 為了處理大量的ZIP文件，我們先嘗試最外層的幾個
    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    
    # 嘗試最後一個（最外層的）ZIP
    print(f"[+] Trying to extract from the outermost ZIP (last boundary)")
    zb = zip_boundaries[-1]
    
    zip_data = buf[zb['start']:zb['end']]
    temp_zip = outdir_path / "outermost.zip"
    temp_zip.write_bytes(zip_data)
    
    try:
        # 遞歸解壓
        final_dir = extract_zip_recursive(str(temp_zip), str(outdir_path / "extracted"))
        print(f"[+] Recursive extraction completed. Final content in: {final_dir}")
        return final_dir
    except Exception as e:
        print(f"[!] Recursive extraction failed: {e}")
    
    # 如果遞歸失敗，嘗試其他邊界
    print(f"[+] Trying other boundaries...")
    for i, zb in enumerate(zip_boundaries[-10:], start=len(zip_boundaries)-10):  # 嘗試最後10個
        try:
            print(f"[+] Trying boundary {i}")
            zip_data = buf[zb['start']:zb['end']]
            temp_zip = outdir_path / f"boundary_{i}.zip"
            temp_zip.write_bytes(zip_data)
            
            with zipfile.ZipFile(temp_zip, 'r') as z:
                extract_dir = outdir_path / f"boundary_{i}_extracted"
                extract_dir.mkdir(exist_ok=True)
                z.extractall(extract_dir)
                print(f"[+] Successfully extracted boundary {i} to {extract_dir}")
                print(f"    Contents: {z.namelist()}")
                
                # 如果包含非ZIP文件，這可能是我們要的
                files = z.namelist()
                non_zip_files = [f for f in files if not f.lower().endswith('.zip')]
                if non_zip_files:
                    print(f"[+] Found non-ZIP files at boundary {i}: {non_zip_files}")
                    return extract_dir
                    
        except Exception as e:
            print(f"[!] Boundary {i} failed: {e}")
            continue
    
    return None

def extract_innermost_only(zip_path: str, outdir: str, max_depth: int = 10000):
    """只提取最內層的檔案，跳過所有中間層"""
    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    
    current_file = Path(zip_path)
    depth = 0
    temp_dir = outdir_path / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    print(f"[+] Extracting only the innermost files from {zip_path}")
    
    while depth < max_depth:
        if depth % 1000 == 0:  # 每1000層顯示進度
            print(f"[+] Depth {depth}...")
        
        try:
            # 確保文件存在
            if not current_file.exists():
                print(f"[!] File not found: {current_file}")
                break
                
            with zipfile.ZipFile(current_file, 'r') as z:
                files = z.namelist()
                
                # 檢查是否有ZIP文件需要進一步解壓
                zip_files = [f for f in files if f.lower().endswith('.zip')]
                
                if not zip_files:
                    # 沒有更多ZIP文件，這就是最內層
                    print(f"[+] Found innermost layer at depth {depth}")
                    print(f"[+] Final files: {files}")
                    
                    # 直接提取到輸出目錄
                    z.extractall(outdir_path)
                    
                    # 清理臨時目錄
                    if temp_dir.exists():
                        shutil.rmtree(temp_dir)
                    
                    print(f"[+] Innermost files extracted to {outdir_path}")
                    return outdir_path
                
                # 使用內存方式處理，避免路徑問題
                next_zip = zip_files[0]
                zip_content = z.read(next_zip)
                
                # 寫入到臨時文件
                temp_zip_path = temp_dir / f"level_{depth}.zip"
                temp_zip_path.write_bytes(zip_content)
                current_file = temp_zip_path
                depth += 1
                
        except zipfile.BadZipFile as e:
            print(f"[!] Bad ZIP file at depth {depth}: {e}")
            print(f"[!] File size: {current_file.stat().st_size if current_file.exists() else 'N/A'}")
            break
        except Exception as e:
            print(f"[!] Error at depth {depth}: {e}")
            print(f"[!] Current file: {current_file}")
            print(f"[!] File exists: {current_file.exists()}")
            if current_file.exists():
                print(f"[!] File size: {current_file.stat().st_size}")
                # 顯示文件的前幾個字節來診斷
                with open(current_file, 'rb') as f:
                    header = f.read(16)
                    print(f"[!] File header: {header.hex()}")
            break
    
    print(f"[!] Reached maximum depth {max_depth}")
    # 清理臨時目錄
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    return None

def extract_final_content(blob_path: str, outdir: str):
    """提取最終內容，只保留最內層文件"""
    buf = Path(blob_path).read_bytes()
    zip_boundaries = find_zip_boundaries(buf)
    
    if not zip_boundaries:
        print("[!] No ZIP boundaries found.")
        return
    
    print(f"[+] Found {len(zip_boundaries)} nested ZIP levels")
    
    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)
    
    # 嘗試從第一個ZIP開始（最內層）
    print(f"[+] Trying from the innermost ZIP (first boundary)...")
    zb = zip_boundaries[0]
    
    zip_data = buf[zb['start']:zb['end']]
    temp_zip = outdir_path / "innermost.zip"
    temp_zip.write_bytes(zip_data)
    
    try:
        # 檢查這個ZIP是否可以直接提取
        with zipfile.ZipFile(temp_zip, 'r') as z:
            files = z.namelist()
            print(f"[+] Innermost ZIP contains: {files}")
            
            # 如果沒有嵌套ZIP，直接提取
            zip_files = [f for f in files if f.lower().endswith('.zip')]
            if not zip_files:
                print(f"[+] No nested ZIPs found, extracting directly...")
                z.extractall(outdir_path)
                temp_zip.unlink()
                
                print(f"[+] Final content extracted to: {outdir_path}")
                for file in outdir_path.iterdir():
                    if file.is_file():
                        print(f"    Final file: {file.name} ({file.stat().st_size} bytes)")
                return outdir_path
    except Exception as e:
        print(f"[!] Innermost ZIP extraction failed: {e}")
    
    # 如果內層失敗，嘗試從外層開始
    print(f"[+] Trying from the outermost ZIP (last boundary)...")
    zb = zip_boundaries[-1]
    
    zip_data = buf[zb['start']:zb['end']]
    temp_zip = outdir_path / "outermost.zip"
    temp_zip.write_bytes(zip_data)
    
    try:
        # 檢查外層ZIP
        with zipfile.ZipFile(temp_zip, 'r') as z:
            files = z.namelist()
            print(f"[+] Outermost ZIP contains: {files}")
        
        # 只提取最內層內容
        final_dir = extract_innermost_only(str(temp_zip), str(outdir_path))
        
        # 清理臨時ZIP文件
        temp_zip.unlink()
        
        if final_dir:
            print(f"[+] Final content extracted to: {final_dir}")
            # 顯示最終文件列表
            for file in final_dir.iterdir():
                if file.is_file():
                    print(f"    Final file: {file.name} ({file.stat().st_size} bytes)")
        return final_dir
        
    except Exception as e:
        print(f"[!] Extraction failed: {e}")
        return None

def extract_last_zip(blob_path: str, outdir: str):
    extract_zip_by_index(blob_path, outdir, -1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} blob.zip outdir [mode]")
        print("  mode options:")
        print("    index (default): Extract specific ZIP by index")
        print("    recursive: Extract all nested levels")  
        print("    final: Extract only the innermost files")
        sys.exit(1)
    
    blob_path = sys.argv[1]
    outdir = sys.argv[2]
    
    if len(sys.argv) > 3:
        mode = sys.argv[3]
        if mode == 'recursive':
            extract_all_nested_levels(blob_path, outdir)
        elif mode == 'final':
            extract_final_content(blob_path, outdir)
        else:
            index = int(mode)
            extract_zip_by_index(blob_path, outdir, index)
    else:
        extract_zip_by_index(blob_path, outdir, -1)