import docx, re, sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx')
for p_idx in [40, 41, 42, 43, 52, 53]:
    p = doc.paragraphs[p_idx]
    xml = p._element.xml
    sz_matches = re.findall(r'w:val="(\d+)"', xml)
    print(f'P{p_idx}: val={sz_matches}')
    # print text inside m:t if any
    mt_texts = re.findall(r'<m:t[^>]*>(.*?)</m:t>', xml)
    wt_texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml)
    print(f'   m:t={mt_texts[:8]}')
    print(f'   w:t={wt_texts}')
