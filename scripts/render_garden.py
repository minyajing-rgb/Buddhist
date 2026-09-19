#!/usr/bin/env python3
"""Website scene component: original vector artwork rendered to PNG.
This is a contemporary artistic garden, not a reconstruction of a historic site.
No external images, fonts or third-party media are redistributed.
"""
from __future__ import annotations
import math,pathlib,random
import cairosvg
ROOT=pathlib.Path(__file__).resolve().parents[1]

def scene():
    r=random.Random(19);s=[]
    s.append('''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="880" viewBox="0 0 1800 880"><defs>
    <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#fff1d9"/><stop offset=".55" stop-color="#e4efe1"/><stop offset="1" stop-color="#b6d9cc"/></linearGradient>
    <radialGradient id="sun"><stop stop-color="#fffdf2"/><stop offset=".4" stop-color="#fff9e8" stop-opacity=".9"/><stop offset="1" stop-color="#fff7e6" stop-opacity="0"/></radialGradient>
    <linearGradient id="water" x2="0" y2="1"><stop stop-color="#99cbbb"/><stop offset=".4" stop-color="#74b9ad"/><stop offset="1" stop-color="#a5d0ba"/></linearGradient>
    <linearGradient id="dome"><stop stop-color="#d9a64d"/><stop offset=".28" stop-color="#fce4a1"/><stop offset=".53" stop-color="#e7ba61"/><stop offset=".78" stop-color="#f6db8f"/><stop offset="1" stop-color="#bc8d3c"/></linearGradient>
    <linearGradient id="wall"><stop stop-color="#f1deba"/><stop offset=".5" stop-color="#fff7df"/><stop offset="1" stop-color="#e8cda4"/></linearGradient>
    <linearGradient id="arch" x2="0" y2="1"><stop stop-color="#d5c5aa"/><stop offset=".6" stop-color="#ecd8b8"/><stop offset="1" stop-color="#fef0d1"/></linearGradient>
    <linearGradient id="stair" x2="0" y2="1"><stop stop-color="#fffae3"/><stop offset="1" stop-color="#d3b387"/></linearGradient>
    <linearGradient id="leaf"><stop stop-color="#739b6b"/><stop offset="1" stop-color="#2b7768"/></linearGradient>
    <g id="blossom"><circle r="14" fill="#f7ae98"/><circle cx="-8" cy="-4" r="8" fill="#f9bfa5"/><circle cx="6" cy="-7" r="9" fill="#f8c7ad"/><circle cx="8" cy="7" r="8" fill="#e58d7b"/><circle cx="-7" cy="8" r="8" fill="#ef9f8e"/><circle r="3.5" fill="#ffe4a2"/></g>
    <g id="lotus"><ellipse cy="13" rx="35" ry="6" fill="#d3e6c4" opacity=".7"/><path d="M0 11 Q-42 2 -40 -15 Q-9 -13 0 11" fill="#e99885" stroke="#ffe7cc"/><path d="M0 11 Q42 2 40 -15 Q9 -13 0 11" fill="#e99885" stroke="#ffe7cc"/><path d="M0 11 Q-31 -12 -19 -29 Q-1 -18 0 11" fill="#f7c6af" stroke="#ffe9c8"/><path d="M0 11 Q31 -12 19 -29 Q1 -18 0 11" fill="#f7c6af" stroke="#ffe9c8"/><path d="M0 12 Q-17 -14 0 -40 Q17 -14 0 12" fill="#fbe2c9" stroke="#ecc4a3"/><ellipse cy="9" rx="9" ry="3" fill="#d5ad60"/></g>
    <g id="floral"><path d="M0 0 C-14 -5 -13 -22 0 -15 C13 -22 14 -5 0 0 C14 5 13 22 0 15 C-13 22 -14 5 0 0" fill="none" stroke="#c29b52"/><circle r="3" fill="#c29b52"/></g>
    </defs><rect width="1800" height="880" fill="url(#sky)"/>
    <path d="M0 425 Q135 345 240 389 T450 392 T650 395 T870 372 T1060 390 T1350 361 T1590 372 T1800 310 V610 H0Z" fill="#b6c4c8" opacity=".30"/>
    <path d="M0 456 Q210 383 325 431 T570 440 T860 415 T1120 433 T1470 405 T1800 387 V600 H0Z" fill="#7ba996" opacity=".22"/>
    <ellipse cx="900" cy="220" rx="630" ry="430" fill="url(#sun)"/>
    <g fill="none" stroke="#fff6df" stroke-width="2" opacity=".65"><path d="M-20 153 Q160 63 311 135 T597 124"/><path d="M1240 100 Q1440 38 1620 86 T1850 70"/><path d="M540 301 Q760 260 1090 285"/></g>''')
    def pavilion(x,y,scale=1):
        s.append(f'<g transform="translate({x},{y}) scale({scale})">')
        s.append('<ellipse cx="0" cy="246" rx="144" ry="12" fill="#648f7250"/><path d="M-134 246 H134 L112 231 H-112Z" fill="#d4b380"/><rect x="-112" y="68" width="224" height="165" fill="url(#wall)" stroke="#cca867"/>')
        for ax in [-73,0,73]:
            s.append(f'<path d="M{ax-25} 230 V131 Q{ax-25} 106 {ax} 94 Q{ax+25} 106 {ax+25} 131 V230Z" fill="url(#arch)" stroke="#c6a165" stroke-width="2"/>')
            for xx in range(ax-18,ax+20,9):s.append(f'<path d="M{xx} 139 V221" stroke="#dfcba4" stroke-width="1"/>')
            for yy in range(145,220,13):s.append(f'<path d="M{ax-22} {yy} H{ax+22}" stroke="#dfcba4" stroke-width="1"/>')
        for ax in [-108,-38,38,108]:
            s.append(f'<rect x="{ax-5}" y="72" width="10" height="151" fill="#fff1cc" stroke="#c6a165"/><rect x="{ax-10}" y="76" width="20" height="8" rx="2" fill="#e9c888"/><rect x="{ax-9}" y="217" width="18" height="11" fill="#f7e0af"/>')
        s.append('<path d="M-135 66 Q-116 74 -104 53 L104 53 Q116 74 135 66 L125 81 H-125Z" fill="url(#dome)" stroke="#b28b48"/><rect x="-114" y="49" width="228" height="10" fill="#eed19a" stroke="#b28b48"/><path d="M-87 49 C-85 17 -37 9 -17 -28 Q0 -6 17 -28 C37 9 85 17 87 49Z" fill="url(#dome)" stroke="#c29446"/>')
        for t in [-60,-30,0,30,60]:s.append(f'<path d="M{t} 49 Q{t*.65} 9 0 -8" fill="none" stroke="#ac854345"/>')
        s.append('<path d="M-6 -26 L0 -49 L6 -26Z" fill="#c59a4e"/><circle cy="-47" r="4" fill="#e5bc67"/><path d="M0 -49 V-66" stroke="#c59a4e" stroke-width="2"/><circle cy="-68" r="3" fill="#e5bc67"/><rect x="-104" y="230" width="208" height="8" fill="#fff0cf" stroke="#c6a165"/>')
        for ax in range(-96,100,24):s.append(f'<use href="#floral" transform="translate({ax},58) scale(.26)"/>')
        s.append('</g>')
    for x in [560,1240]:pavilion(x,427,.53)
    # Terraced garden and a distant book pavilion beneath the central open sky.
    s.append('<path d="M0 555 Q450 523 900 557 Q1350 523 1800 555 V703 H0Z" fill="#b9cca3"/><path d="M0 588 Q470 555 900 578 Q1330 555 1800 588 V656 H0Z" fill="#e8dbaf"/>')
    pavilion(900,434,.44)
    # Water and pale stone paths lead toward the centre, not across the title.
    s.append('<path d="M0 703 Q320 630 630 657 L1170 657 Q1480 630 1800 703 V880 H0Z" fill="url(#water)"/><path d="M844 562 H956 L1055 694 H745Z" fill="url(#stair)" stroke="#cfb682"/>')
    for y in range(573,690,12):
        w=57+(y-562)*.75;s.append(f'<path d="M{900-w} {y} H{900+w}" stroke="#c5b080" stroke-width="1.2"/>')
    for side in [0,1]:
        s.append(f'<g transform="{("translate(1800,0) scale(-1,1)" if side else "")}"><path d="M0 600 L736 645 L745 664 L0 643Z" fill="#f5e7c4" stroke="#c4ad78"/><path d="M0 611 L739 654" stroke="#bda16b"/>')
        for x in range(5,735,30):
            y=583+x*.06;s.append(f'<path d="M{x} {y} L{x+12} {y+.7} V{y+44} L{x} {y+43.3}Z" fill="#f5e9c9" stroke="#c5ab76"/><ellipse cx="{x+6}" cy="{y-1}" rx="9" ry="3" fill="#fff5d5" stroke="#c5ab76"/>')
        s.append('</g>')
    pavilion(235,318,1.05);pavilion(1565,289,1.16)
    # Layered flowering trees with individually rendered leaves and flowers.
    def tree(x,y,size=1,pink=True):
        s.append(f'<g transform="translate({x},{y}) scale({size})"><path d="M-13 215 Q-20 109 -7 18 Q-72 -4 -110 -58 M-3 52 Q45 2 111 -61 M-3 61 Q-53 10 -56 -53 M-8 124 Q51 62 61 14" fill="none" stroke="#7f7958" stroke-width="9" stroke-linecap="round"/>')
        for _ in range(165):
            ang=r.random()*math.tau;rad=math.sqrt(r.random());xx=math.cos(ang)*150*rad;yy=math.sin(ang)*94*rad-42
            rr=r.uniform(12,30)
            fill=r.choice(['#b1bb79','#7b9f66','#91b176','#5f9877'])
            s.append(f'<ellipse cx="{xx:.1f}" cy="{yy:.1f}" rx="{rr:.1f}" ry="{rr*.6:.1f}" transform="rotate({r.uniform(-70,70):.1f} {xx:.1f} {yy:.1f})" fill="{fill}" opacity=".94"/>')
        if pink:
            for _ in range(145):
                ang=r.random()*math.tau;rad=math.sqrt(r.random());xx=math.cos(ang)*149*rad;yy=math.sin(ang)*90*rad-49;sc=r.uniform(.45,1.1)
                s.append(f'<use href="#blossom" transform="translate({xx:.2f},{yy:.2f}) scale({sc:.2f}) rotate({r.randrange(90)})"/>')
        s.append('</g>')
    for x,y,z,p in [(475,400,.6,False),(1310,385,.7,False),(52,215,1.33,True),(1767,171,1.48,True),(404,276,.86,True),(1401,238,.8,True)]:tree(x,y,z,p)
    # Low garden beds and ornamental stone lanterns.
    for center in [100,390,1385,1680]:
        for _ in range(40):
            x=center+r.uniform(-130,130);y=r.uniform(564,651);s.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r.uniform(10,27):.1f}" ry="{r.uniform(8,15):.1f}" fill="{r.choice(["#699570","#a3b57b","#86a778"])}"/>')
            if r.random()<.28:s.append(f'<use href="#blossom" transform="translate({x:.1f},{y-8:.1f}) scale(.32)"/>')
    for x,y in [(651,627),(1149,627),(127,676),(1673,676)]:
        s.append(f'<g transform="translate({x},{y})"><ellipse cy="14" rx="28" ry="6" fill="#5f987344"/><path d="M-17 9 H17 L12 -3 H-12Z" fill="#f6e1b6" stroke="#b89659"/><path d="M-5 -3 V-45 H5 V-3Z" fill="#f2d4a2" stroke="#b89659"/><path d="M-16 -45 V-67 Q0 -83 16 -67 V-45Z" fill="#fff0c6" stroke="#b89659"/><path d="M-21 -66 Q0 -83 21 -66Z" fill="#d5a958"/><circle cy="-81" r="4" fill="#e9c276"/></g>')
    for _ in range(100):
        y=r.uniform(689,880);x=r.uniform(0,1800);length=r.uniform(10,90)
        s.append(f'<path d="M{x:.1f} {y:.1f} q{length/2:.1f} -2 {length:.1f} 0" fill="none" stroke="{r.choice(["#e6ead0","#bad9bf","#69a998"])}" stroke-width="{r.uniform(.6,1.5):.1f}" opacity=".55"/>')
    # Lotus leaves and blooms in the foreground, with an open reflective centre.
    for _ in range(63):
        side=r.randrange(2);x=r.uniform(-40,550) if not side else r.uniform(1250,1840);y=r.uniform(718,896);rr=r.uniform(13,47)
        s.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rr:.1f}" ry="{rr*.31:.1f}" fill="{r.choice(["#5d9278","#80ab7d","#8caf78"])}" stroke="#c0ce9666"/>')
        if r.random()<.33:s.append(f'<use href="#lotus" transform="translate({x:.1f},{y-12:.1f}) scale({r.uniform(.4,1.2):.2f})"/>')
    for x,y,sc in [(262,814,1.5),(1539,800,1.35),(508,752,.65),(1246,741,.7)]:s.append(f'<use href="#lotus" transform="translate({x},{y}) scale({sc})"/>')
    # Sparse flower petals, tiny gilded stars, and a light botanical edge.
    for _ in range(38):
        x=r.choice([r.uniform(0,600),r.uniform(1200,1800)]);y=r.uniform(140,600)
        s.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4" ry="1.8" transform="rotate({r.randrange(150)} {x:.1f} {y:.1f})" fill="#eaab90" opacity=".7"/>')
    for x,y in [(416,100),(1357,120),(306,465),(1488,489),(1120,388),(676,391)]:s.append(f'<path d="M{x-4} {y}h8 M{x} {y-4}v8" stroke="#c79e55" stroke-width="1"/>')
    s.append('<path d="M0 876 Q380 835 740 879 M1070 879 Q1460 834 1800 876" fill="none" stroke="#d0b883" stroke-width="2"/></svg>')
    return ''.join(s)

def main():
    out=ROOT/'docs/garden/assets';out.mkdir(parents=True,exist_ok=True)
    cairosvg.svg2png(bytestring=scene().encode(),write_to=str(out/'garden.png'),output_width=2000)
    icon='<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect width="64" height="64" rx="16" fill="#fff8e9"/><g stroke="#b8914d" stroke-width="2" fill="#e4c688"><path d="M32 49C6 44 10 21 10 21C30 23 32 49 32 49Z"/><path d="M32 49C58 44 54 21 54 21C34 23 32 49 32 49Z"/><path d="M32 49C13 30 32 8 32 8C51 30 32 49 32 49Z" fill="#568578"/><path d="M15 53H49" fill="none"/></g></svg>'
    cairosvg.svg2png(bytestring=icon.encode(),write_to=str(out/'lotus.png'))
    print('Original garden illustration and lotus site icon rendered.')
if __name__=='__main__':main()
