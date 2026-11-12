"""把scripts/check_pages.py的每條規則各拿掉一次，看tests/test_check_pages.py抓不抓得到。跑完還原。

用法：python3 tests/mutation_check_pages.py .（參數是repo的根目錄）
"""
import subprocess, sys, shutil
from pathlib import Path
ROOT = Path(sys.argv[1])
P = ROOT / "scripts" / "check_pages.py"
S = ROOT / "scripts" / "check_slide_map.py"
orig = P.read_text(encoding="utf-8"); orig_s = S.read_text(encoding="utf-8")
M = [
 ("P1 沒有逐頁稿", P, 'rep.err(rel, f"大綱的第{pg}頁沒有逐頁稿")', 'pass'),
 ("P1 標題", P, 'rep.err(rel, f"第一行要是', 'None and rep.err(rel, f"第一行要是'),
 ("P2 缺段落", P, 'rep.err(rel, f"缺少段落', 'None and rep.err(rel, f"缺少段落'),
 ("P2 重複段落", P, 'rep.err(rel, f"段落「## {n}」出現', 'None and rep.err(rel, f"段落「## {n}」出現'),
 ("P2 順序", P, 'rep.err(rel, "段落的順序不對', 'None and rep.err(rel, "段落的順序不對'),
 ("P3 卡不存在", P, 'rep.err(rel, f"證據卡 {cid} 不存在")\n                    continue', 'continue'),
 ("P3 類型不合", P, 'rep.err(rel, f"證據卡 {cid} 的類型是', 'None and rep.err(rel, f"證據卡 {cid} 的類型是'),
 ("P3 不認得的標示", P, 'rep.err(rel, f"證據卡段落用了不認得的標示【{tag}】")', 'pass'),
 ("P3 多了slide-map沒有的卡", P, 'for cid in sorted(page_cards - want):', 'for cid in []:'),
 ("P3 少了slide-map有的卡", P, 'for cid in sorted(want - page_cards):', 'for cid in []:'),
 ("P4 數字沒列", P, 'if num not in listed:', 'if False:'),
 ("P4 拿掉反引號檔名的排除", P, 't = PATH_TICK.sub(" ", text)', 't = text'),
 ("P4 拿掉第N頁的排除", P, 't = PAGE_REF.sub(" ", t)', 't = t'),
 ("P4 拿掉大寫名稱的排除", P, 't = NAME_NUM.sub("", t)', 't = t'),
 ("P5 找不到", P, 'if not found(num, pool):', 'if False:'),
 ("P5 表格的卡不在這頁", P, 'rep.err(rel, f"數字表的', 'None and rep.err(rel, f"數字表的'),
 ("P5 不算限制", P, ', secs.get("限制", "")])', '])'),
 ("P5 顯示設定的列", P, 'if num not in shown:', 'if False:'),
 ("P6 術語", P, 'if not m or not any(', 'if False and not any('),
 ("P7 標示", P, 'if f"【{tag}】" in reader and not (page_types & types):', 'if False:'),
 ("四捨五入改成只看整數", S, "if round(yv, d) == x", "if round(yv) == round(x)"),
]
for name, f, old, new in M:
    src = orig if f == P else orig_s
    assert src.count(old) == 1, name
    f.write_text(src.replace(old, new, 1), encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", str(ROOT / "tests" / "test_check_pages.py")], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1]
    print(f"{name}：{'測試抓到了' if r.returncode == 1 else '測試沒抓到'}（{last}）")
    P.write_text(orig, encoding="utf-8"); S.write_text(orig_s, encoding="utf-8")
print("還原後內容相同：", P.read_text(encoding="utf-8") == orig and S.read_text(encoding="utf-8") == orig_s)
