"""Build the GPTI review document from repository Markdown with pinned Word v1.1 tokens."""
from pathlib import Path
import re
import json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'deliverables' / 'GPTI_使命品牌与业务体系_v1.0.docx'
SOURCE_FILES = [
    ROOT / 'strategy' / 'mission-system.md',
    ROOT / 'brand' / 'brand-system.md',
    ROOT / 'strategy' / 'programme-business-model.md',
]
BLACK = RGBColor(0, 0, 0)

def fonts(run, size=11.5, bold=False, italic=False):
    run.font.name = 'Aptos'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = BLACK
    rpr = run._element.get_or_add_rPr()
    rf = rpr.rFonts
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for key, val in [('ascii','Aptos'), ('hAnsi','Aptos'), ('eastAsia','仿宋'), ('cs','Aptos')]:
        rf.set(qn('w:'+key), val)
    szcs = rpr.find(qn('w:szCs'))
    if szcs is None:
        szcs = OxmlElement('w:szCs')
        rpr.append(szcs)
    szcs.set(qn('w:val'), str(round(size * 2)))
    return run

def inline(p, string, size=11.5, bold=False, italic=False):
    string = string.replace('`', '')
    parts = re.split(r'(\*\*.*?\*\*)', string)
    for part in parts:
        if not part: continue
        partbold = part.startswith('**') and part.endswith('**')
        if partbold: part = part[2:-2]
        fonts(p.add_run(part), size, bold or partbold, italic)

def para_format(p, before=4, after=None, indent=0, left=0, keep=False):
    if after is None: after = before
    fmt = p.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = 1.5
    fmt.first_line_indent = Cm(indent)
    fmt.left_indent = Cm(left)
    fmt.keep_with_next = keep
    fmt.widow_control = True
    # Explicit body-region line=360, lineRule=auto, symmetric spacing.
    ppr = p._p.get_or_add_pPr()
    spacing = ppr.find(qn('w:spacing'))
    spacing.set(qn('w:line'), '360')
    spacing.set(qn('w:lineRule'), 'auto')
    return p

def styled(doc, text, role='body'):
    p = doc.add_paragraph()
    if role == 'chapter':
        para_format(p, 9, indent=0, keep=True)
        inline(p, text, 21, True)
    elif role == 'secondary':
        para_format(p, 7.5, indent=0, keep=True)
        inline(p, text, 13, True)
    elif role == 'item':
        para_format(p, 2, indent=0, keep=True)
        inline(p, text, 12.5, True)
    elif role == 'intro':
        para_format(p, 7.5, indent=0.8)
        inline(p, text, 12)
    elif role == 'note':
        para_format(p, 4, indent=0)
        inline(p, text, 9, italic=True)
    else:
        para_format(p, 4, indent=0.8)
        inline(p, text, 11.5)
    return p

def border_on_header(p):
    ppr = p._p.get_or_add_pPr()
    pb = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    for k,v in [('val','single'),('sz','4'),('space','4'),('color','000000')]:
        b.set(qn('w:'+k),v)
    pb.append(b); ppr.append(pb)

def page_field(p):
    r = fonts(p.add_run(), 8)
    begin = OxmlElement('w:fldChar'); begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = ' PAGE '
    sep = OxmlElement('w:fldChar'); sep.set(qn('w:fldCharType'), 'separate')
    txt = OxmlElement('w:t'); txt.text='1'
    end = OxmlElement('w:fldChar'); end.set(qn('w:fldCharType'), 'end')
    for el in [begin,instr,sep,txt,end]: r._r.append(el)

def setup_numbers(doc):
    numroot = doc.part.numbering_part.element
    def addfmt(abstract_id, num_id, kind):
        ab=OxmlElement('w:abstractNum'); ab.set(qn('w:abstractNumId'), str(abstract_id))
        lvl=OxmlElement('w:lvl'); lvl.set(qn('w:ilvl'),'0')
        start=OxmlElement('w:start');start.set(qn('w:val'),'1');lvl.append(start)
        fmt=OxmlElement('w:numFmt');fmt.set(qn('w:val'),kind);lvl.append(fmt)
        txt=OxmlElement('w:lvlText');txt.set(qn('w:val'),'•' if kind=='bullet' else '%1.');lvl.append(txt)
        jc=OxmlElement('w:lvlJc');jc.set(qn('w:val'),'left');lvl.append(jc)
        ppr=OxmlElement('w:pPr');ind=OxmlElement('w:ind');ind.set(qn('w:left'),'360');ind.set(qn('w:hanging'),'360');ppr.append(ind);lvl.append(ppr)
        ab.append(lvl);numroot.append(ab)
        num=OxmlElement('w:num');num.set(qn('w:numId'),str(num_id));ref=OxmlElement('w:abstractNumId');ref.set(qn('w:val'),str(abstract_id));num.append(ref);numroot.append(num)
    # Avoid default IDs by obtaining maxima.
    aas=[int(x.get(qn('w:abstractNumId'))) for x in numroot.findall(qn('w:abstractNum'))]
    nns=[int(x.get(qn('w:numId'))) for x in numroot.findall(qn('w:num'))]
    a=max(aas+[0])+1;n=max(nns+[0])+1
    addfmt(a,n,'bullet');addfmt(a+1,n+1,'decimal')
    return n,n+1

def restarted_decimal_num(doc, base_num_id):
    root=doc.part.numbering_part.element
    old=next(el for el in root.findall(qn('w:num')) if int(el.get(qn('w:numId')))==base_num_id)
    abstract_id=old.find(qn('w:abstractNumId')).get(qn('w:val'))
    new_id=max(int(x.get(qn('w:numId'))) for x in root.findall(qn('w:num')))+1
    num=OxmlElement('w:num');num.set(qn('w:numId'),str(new_id))
    aid=OxmlElement('w:abstractNumId');aid.set(qn('w:val'),abstract_id);num.append(aid)
    override=OxmlElement('w:lvlOverride');override.set(qn('w:ilvl'),'0')
    start=OxmlElement('w:startOverride');start.set(qn('w:val'),'1');override.append(start);num.append(override)
    root.append(num)
    return new_id

def listpara(doc, text, numid, bullet=False):
    p=doc.add_paragraph(); para_format(p, 3.25 if bullet else 4, indent=0, left=.635)
    ppr=p._p.get_or_add_pPr(); numpr=OxmlElement('w:numPr')
    ilvl=OxmlElement('w:ilvl');ilvl.set(qn('w:val'),'0')
    nid=OxmlElement('w:numId');nid.set(qn('w:val'),str(numid))
    numpr.extend([ilvl,nid]);ppr.append(numpr)
    inline(p,text,11 if bullet else 11.5)
    return p

def add_table_as_records(doc, rows):
    if len(rows)<2:return
    heads=rows[0]
    for cells in rows[1:]:
        if len(cells)!=len(heads): continue
        head=cells[0]
        p=doc.add_paragraph();para_format(p,4,indent=0)
        inline(p,head+'。',11.5,True)
        for h,c in zip(heads[1:],cells[1:]):
            if c.strip(): inline(p,'  '+h+'：'+c,11.5)

def parse_table_row(line):
    return [x.strip() for x in line.strip().strip('|').split('|')]

def add_source(doc, path, chapter, bullet_num, decimal_num):
    lines=path.read_text(encoding='utf-8').splitlines()
    eyebrow=doc.add_paragraph(); eyebrow.paragraph_format.page_break_before=True
    para_format(eyebrow,2.5,indent=0,keep=True)
    inline(eyebrow,f'{chapter:02d}   GPTI STRATEGY',8.5,True)
    title={'mission-system.md':'使命体系','brand-system.md':'品牌体系','programme-business-model.md':'业务与项目体系'}[path.name]
    styled(doc,title,'chapter')
    active_decimal_num=decimal_num
    i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line or line.startswith('# '):i+=1;continue
        if line.startswith('版本 '):
            styled(doc,line,'note');i+=1;continue
        if line.startswith('## '):
            styled(doc,line[3:],'secondary');i+=1;continue
        if line.startswith('### '):
            styled(doc,line[4:],'item');i+=1;continue
        if line.startswith('|'):
            table=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=parse_table_row(lines[i]);i+=1
                if all(re.fullmatch(r':?-+:?',c or '') for c in row):continue
                table.append(row)
            add_table_as_records(doc,table)
            continue
        if line.startswith('- '):
            listpara(doc,line[2:],bullet_num,True);i+=1;continue
        m=re.match(r'^\d+\.\s+(.*)',line)
        if m:
            if line.startswith('1. '): active_decimal_num=restarted_decimal_num(doc,decimal_num)
            listpara(doc,m.group(1),active_decimal_num);i+=1;continue
        if line.startswith('`') and line.endswith('`'):
            styled(doc,line.strip('`'),'note');i+=1;continue
        parts=[line.replace('  ',' ')]
        i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||- |\d+\.\s)',lines[i].strip()):
            parts.append(lines[i].strip());i+=1
        styled(doc,' '.join(parts),'intro' if chapter==1 and len(parts)<2 and len(' '.join(parts))>90 else 'body')

def coverpara(doc,text,size,bold,before,after,style=None,line=1.0):
    p=doc.add_paragraph(style=style)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    fmt=p.paragraph_format;fmt.space_before=Pt(before);fmt.space_after=Pt(after);fmt.line_spacing=line
    inline(p,text,size,bold)
    return p

def main():
    doc=Document()
    sec=doc.sections[0]
    sec.page_width=Cm(21); sec.page_height=Cm(29.7)
    sec.top_margin=Cm(2.55);sec.bottom_margin=Cm(2.35)
    sec.left_margin=Cm(2.7);sec.right_margin=Cm(2.7)
    sec.header_distance=Cm(1);sec.footer_distance=Cm(1)
    sec.different_first_page_header_footer=True
    normal=doc.styles['Normal'];normal.font.name='Aptos';normal.font.color.rgb=BLACK
    # Title style must be Word's Title and black without borders.
    title_style=doc.styles['Title'];title_style.font.name='Aptos';title_style.font.color.rgb=BLACK
    title_ppr=title_style._element.get_or_add_pPr()
    title_border=title_ppr.find(qn('w:pBdr'))
    if title_border is not None: title_ppr.remove(title_border)
    for st in [normal,title_style]:
        st._element.get_or_add_rPr()
    bullet_num,decimal_num=setup_numbers(doc)
    hdr=sec.header.paragraphs[0]
    hdr.alignment=WD_ALIGN_PARAGRAPH.LEFT
    fonts(hdr.add_run('GPTI'),7.5,True)
    fonts(hdr.add_run('  |  MISSION BRAND AND PROGRAMME SYSTEM'),7.5)
    border_on_header(hdr)
    footer=sec.footer.paragraphs[0]
    footer.alignment=WD_ALIGN_PARAGRAPH.LEFT
    fonts(footer.add_run('GPTI  |  使命品牌与业务体系'),7.5)
    # Right aligned tab stop keeps a live PAGE field at the right margin.
    footer.paragraph_format.tab_stops.add_tab_stop(Cm(15.6))
    fonts(footer.add_run('\t'),7.5)
    page_field(footer)

    coverpara(doc,'GPTI  ·  FOUNDING STRATEGY',8.5,True,0,70)
    coverpara(doc,'创始阶段工作文件',15,False,0,12, line=1.03)
    coverpara(doc,'全球繁荣与转型倡议',29,True,0,8,'Title',line=1.04)
    coverpara(doc,'使命品牌与业务体系',29,True,0,18,'Title',line=1.04)
    coverpara(doc,'GLOBAL PROSPERITY AND TRANSITION INITIATIVE',11,True,0,4)
    coverpara(doc,'MISSION BRAND AND PROGRAMME SYSTEM',10.5,True,0,35)
    coverpara(doc,'用于明确机构存在理由、项目选择与可核验成果',12.5,False,0,5,line=1.22)
    coverpara(doc,'含品牌语言、业务边界与首年运行框架',12.5,False,0,77,line=1.22)
    coverpara(doc,'BOARD DISCUSSION DRAFT',8.5,True,0,4)
    coverpara(doc,'VERSION 1.0   ·   26 SEPTEMBER 2026',9,False,0,0)

    for idx,path in enumerate(SOURCE_FILES,1):
        add_source(doc,path,idx,bullet_num,decimal_num)

    ep=doc.add_paragraph();ep.paragraph_format.page_break_before=True
    para_format(ep,2.5,indent=0,keep=True);inline(ep,'04   RESEARCH AND PUBLICATION',8.5,True)
    styled(doc,'资料依据与使用边界','chapter')
    styled(doc,'本文件是 GPTI 的创始阶段战略建议，尚未由董事会采纳。机构登记、税务豁免、项目权属和合作关系以相应正式文件为准。以下官方资料用于校准战略原则和合规边界，并不代表其机构支持、认证或认可 GPTI。','intro')
    refs=[
        ('联合国 2030 议程','https://sdgs.un.org/2030agenda'),
        ('国际劳工组织公正转型指南','https://www.ilo.org/publications/guidelines-just-transition-towards-environmentally-sustainable-economies'),
        ('OECD DAC 评价标准','https://www.oecd.org/en/topics/sub-issues/development-co-operation-evaluation-and-effectiveness/evaluation-criteria.html'),
        ('美国 IRS 501(c)(3) 目的','https://www.irs.gov/charities-non-profits/charitable-organizations/exempt-purposes-internal-revenue-code-section-501c3'),
        ('美国 IRS 私人利益限制','https://www.irs.gov/charities-non-profits/charitable-organizations/inurement-private-benefit-charitable-organizations'),
        ('联合国 ECOSOC 申请条件','https://ecosoc.un.org/en/ngo/apply-for-consultative-status'),
    ]
    for name,url in refs:
        p=doc.add_paragraph();para_format(p,4,indent=0)
        inline(p,name+'：'+url,10.5)
    styled(doc,'设计标准：sunshinerao/my-standards，固定提交 4057223710d62398a4a6c543de2e0bc199c33eb7。正文源文件位于本仓库 strategy/ 与 brand/ 目录。','note')
    doc.core_properties.title='GPTI 使命品牌与业务体系'
    doc.core_properties.subject='Global Prosperity and Transition Initiative founding strategy'
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc.save(OUT)
    print(json.dumps({'out':str(OUT),'bytes':OUT.stat().st_size},ensure_ascii=False))

if __name__=='__main__':main()
