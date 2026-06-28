/**
 * tarot-cards.js  v4.0  — ライダー・ウェイト版 精密SVG 大アルカナ22枚
 * viewBox="0 0 100 160"
 * 使い方: TAROT_FULL[n].svg でSVG文字列取得
 */

function _wrap(num, name, border, skyTop, skyBot, gndTop, gndBot, body){
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 160">
<defs>
  <linearGradient id="sk${num}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${skyTop}"/><stop offset="100%" stop-color="${skyBot}"/></linearGradient>
  <linearGradient id="gn${num}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${gndTop}"/><stop offset="100%" stop-color="${gndBot}"/></linearGradient>
</defs>
<rect width="100" height="160" rx="7" fill="#0a0a0f"/>
<rect x="3" y="3" width="94" height="154" rx="6" fill="url(#sk${num})"/>
<rect x="3" y="115" width="94" height="42" rx="0" fill="url(#gn${num})"/>
<rect x="3" y="147" width="94" height="10" rx="0 0 6 6" fill="${border}" opacity="0.15"/>
<rect x="3" y="3" width="94" height="154" rx="6" fill="none" stroke="${border}" stroke-width="1.8" opacity="0.9"/>
<rect x="6" y="6" width="88" height="148" rx="5" fill="none" stroke="${border}" stroke-width="0.5" opacity="0.5"/>
<text x="8" y="17" font-size="9" fill="${border}" font-family="serif" font-weight="bold" opacity="0.9">${num}</text>
${body}
<rect x="6" y="138" width="88" height="18" rx="3" fill="${border}" opacity="0.18"/>
<text x="50" y="151" text-anchor="middle" font-size="8.5" fill="${border}" font-family="serif" font-weight="bold" letter-spacing="0.5">${name}</text>
</svg>`;
}

const TAROT_SVG = {};

// ── 0 愚者 ─────────────────────────────────────────────────────
TAROT_SVG[0] = _wrap(0,'THE FOOL','#DAA520','#87CEEB','#b0d8f0','#8B7355','#6B5A3E',`
<circle cx="78" cy="26" r="13" fill="#FFD700" opacity="0.9"/>
<path d="M78 11 L78 7 M92 22 L96 22 M87 15 L90 12 M87 27 L90 30 M69 15 L66 12" stroke="#FFD700" stroke-width="1.2" opacity="0.8"/>
<path d="M3 115 L42 88 L42 115Z" fill="#7a6045" opacity="0.8"/>
<path d="M42 88 L75 115 L42 115Z" fill="#6B5A3E" opacity="0.5"/>
<path d="M60 115 L78 85 L96 100 L97 115Z" fill="#909090" opacity="0.5"/>
<path d="M72 88 L78 80 L84 88" fill="#FFFFF0" opacity="0.4"/>
<ellipse cx="50" cy="82" rx="12" ry="18" fill="#FFFACD" opacity="0.85"/>
<circle cx="50" cy="64" r="9" fill="#FFDAB9" opacity="0.95"/>
<path d="M41 61 Q50 52 59 61" fill="#FF6347" opacity="0.85"/>
<path d="M39 64 L62 64" stroke="#FF6347" stroke-width="2" opacity="0.7"/>
<circle cx="47" cy="63" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="63" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 67 Q50 69 53 67" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M38 73 Q50 68 62 73 L64 100 L36 100Z" fill="#FFFACD" opacity="0.85"/>
<path d="M58 70 L74 50" stroke="#8B4513" stroke-width="2" opacity="0.85"/>
<circle cx="74" cy="48" r="5" fill="#FF69B4" opacity="0.8"/>
<circle cx="79" cy="46" r="3.5" fill="#FF1493" opacity="0.7"/>
<circle cx="70" cy="45" r="3.5" fill="#FFB6C1" opacity="0.7"/>
<ellipse cx="33" cy="105" rx="8" ry="5" fill="#FFFFF0" opacity="0.9"/>
<circle cx="27" cy="102" r="5" fill="#FFFFF0" opacity="0.9"/>
<path d="M38 99 L42 95" stroke="#FFFFF0" stroke-width="1.2" opacity="0.8"/>
<circle cx="66" cy="80" r="5" fill="#DAA520" opacity="0.7"/>
`);

// ── 1 魔術師 ─────────────────────────────────────────────────────
TAROT_SVG[1] = _wrap(1,'THE MAGICIAN','#8B0000','#FFD700','#FFA500','#228B22','#1a6b18',`
<path d="M35 24 Q42 16 50 22 Q58 16 65 24 Q58 32 50 26 Q42 32 35 24" fill="none" stroke="#DAA520" stroke-width="2" opacity="0.95"/>
<circle cx="22" cy="28" r="5" fill="#FF0000" opacity="0.7"/>
<circle cx="29" cy="24" r="4" fill="#FF0000" opacity="0.6"/>
<circle cx="15" cy="33" r="3.5" fill="#228B22" opacity="0.6"/>
<circle cx="78" cy="28" r="5" fill="#FF0000" opacity="0.7"/>
<circle cx="71" cy="24" r="4" fill="#FF0000" opacity="0.6"/>
<circle cx="85" cy="33" r="3.5" fill="#228B22" opacity="0.6"/>
<ellipse cx="50" cy="82" rx="16" ry="22" fill="#DC143C" opacity="0.8"/>
<path d="M34 70 Q50 65 66 70 L68 115 L32 115Z" fill="#FFFFF0" opacity="0.85"/>
<circle cx="50" cy="57" r="10" fill="#FFDAB9" opacity="0.95"/>
<circle cx="47" cy="55" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="55" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 60 Q50 62 53 60" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M62 67 L76 28" stroke="#8B4513" stroke-width="2.5" opacity="0.9"/>
<circle cx="76" cy="26" r="4" fill="#DAA520" opacity="0.85"/>
<path d="M38 67 L26 82" stroke="#FFDAB9" stroke-width="3.5" opacity="0.8"/>
<rect x="28" y="103" width="44" height="6" rx="2" fill="#8B4513" opacity="0.75"/>
<rect x="33" y="109" width="4" height="9" rx="1" fill="#8B4513" opacity="0.65"/>
<rect x="63" y="109" width="4" height="9" rx="1" fill="#8B4513" opacity="0.65"/>
<circle cx="38" cy="99" r="5" fill="#FFD700" opacity="0.8"/>
<rect x="44" y="95" width="8" height="8" rx="1" fill="#C0C0C0" opacity="0.75"/>
<path d="M56 94 Q60 90 64 94 Q60 98 56 94" fill="#FF6347" opacity="0.75"/>
<circle cx="72" cy="98" r="5" fill="#9370DB" opacity="0.75"/>
<path d="M36 84 Q50 88 64 84" stroke="#DAA520" stroke-width="1.5" opacity="0.7"/>
`);

// ── 2 女教皇 ─────────────────────────────────────────────────────
TAROT_SVG[2] = _wrap(2,'THE HIGH PRIESTESS','#9090ff','#000044','#000066','#000066','#191970',`
<rect x="8" y="22" width="15" height="93" rx="3" fill="#1C1C1C" opacity="0.95"/>
<rect x="9" y="19" width="13" height="8" rx="2" fill="#333" opacity="0.9"/>
<text x="15" y="27" text-anchor="middle" font-size="9" fill="#DAA520" font-family="serif" font-weight="bold">B</text>
<rect x="77" y="22" width="15" height="93" rx="3" fill="#F5F5DC" opacity="0.95"/>
<rect x="78" y="19" width="13" height="8" rx="2" fill="#E8E8D0" opacity="0.9"/>
<text x="84" y="27" text-anchor="middle" font-size="9" fill="#333" font-family="serif" font-weight="bold">J</text>
<rect x="23" y="22" width="54" height="93" fill="#1a0a5a" opacity="0.75"/>
<circle cx="35" cy="38" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="50" cy="32" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="65" cy="38" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="35" cy="58" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="50" cy="52" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="65" cy="58" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="35" cy="78" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="50" cy="72" r="4.5" fill="#8B0000" opacity="0.55"/>
<circle cx="65" cy="78" r="4.5" fill="#8B0000" opacity="0.55"/>
<ellipse cx="50" cy="82" rx="20" ry="30" fill="#0000CD" opacity="0.7"/>
<circle cx="50" cy="52" r="11" fill="#FFDAB9" opacity="0.95"/>
<circle cx="50" cy="43" r="6" fill="#C0C0C0" opacity="0.75"/>
<circle cx="40" cy="47" r="4.5" fill="#808080" opacity="0.65"/>
<circle cx="60" cy="47" r="4.5" fill="#808080" opacity="0.65"/>
<circle cx="47" cy="51" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="51" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 56 Q50 58 53 56" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M44 63 L56 63 M50 58 L50 68" stroke="#C0C0C0" stroke-width="1.5" opacity="0.8"/>
<rect x="34" y="70" width="32" height="20" rx="2" fill="#DEB887" opacity="0.85"/>
<text x="50" y="83" text-anchor="middle" font-size="9" fill="#8B4513" font-family="serif" font-weight="bold">TORA</text>
<path d="M30 85 Q50 92 70 85 Q68 115 50 118 Q32 115 30 85" fill="#0000CD" opacity="0.4"/>
`);

// ── 3 女帝 ─────────────────────────────────────────────────────
TAROT_SVG[3] = _wrap(3,'THE EMPRESS','#DAA520','#87CEEB','#a8d8ea','#228B22','#1a6b18',`
<path d="M80 20 Q84 50 82 80 Q80 100 80 115" fill="none" stroke="#4169E1" stroke-width="3.5" opacity="0.55"/>
<path d="M86 20 Q90 50 88 80 Q86 100 86 115" fill="none" stroke="#4169E1" stroke-width="2" opacity="0.4"/>
<rect x="8" y="55" width="5" height="60" rx="1" fill="#8B4513" opacity="0.7"/>
<ellipse cx="10" cy="50" rx="11" ry="14" fill="#228B22" opacity="0.65"/>
<rect x="87" y="60" width="5" height="55" rx="1" fill="#8B4513" opacity="0.7"/>
<ellipse cx="89" cy="55" rx="10" ry="13" fill="#228B22" opacity="0.65"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#DAA520" opacity="0.45"/>
<rect x="20" y="88" width="60" height="27" rx="5" fill="#DC143C" opacity="0.7"/>
<rect x="22" y="82" width="56" height="10" rx="3" fill="#8B4513" opacity="0.8"/>
<ellipse cx="50" cy="78" rx="22" ry="28" fill="#FFFFF0" opacity="0.85"/>
<circle cx="50" cy="53" r="12" fill="#FFDAB9" opacity="0.95"/>
<path d="M37 46 Q50 38 63 46" fill="none" stroke="#DAA520" stroke-width="2" opacity="0.8"/>
<circle cx="37" cy="46" r="3" fill="#DAA520" opacity="0.9"/>
<circle cx="44" cy="42" r="3" fill="#DAA520" opacity="0.9"/>
<circle cx="50" cy="40" r="3" fill="#DAA520" opacity="0.9"/>
<circle cx="56" cy="42" r="3" fill="#DAA520" opacity="0.9"/>
<circle cx="63" cy="46" r="3" fill="#DAA520" opacity="0.9"/>
<circle cx="47" cy="52" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="52" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 57 Q50 59 53 57" fill="none" stroke="#c07050" stroke-width="1"/>
<circle cx="28" cy="80" r="7" fill="none" stroke="#DAA520" stroke-width="2" opacity="0.8"/>
<path d="M28 87 L28 95 M24 91 L32 91" stroke="#DAA520" stroke-width="1.5" opacity="0.8"/>
<path d="M67 62 L74 33" stroke="#8B4513" stroke-width="2.5" opacity="0.85"/>
<circle cx="74" cy="31" r="5" fill="#FFD700" opacity="0.85"/>
<circle cx="18" cy="32" r="5" fill="#FF69B4" opacity="0.7"/>
<circle cx="26" cy="27" r="4" fill="#FF1493" opacity="0.6"/>
<circle cx="82" cy="35" r="5" fill="#FF69B4" opacity="0.7"/>
`);

// ── 4 皇帝 ─────────────────────────────────────────────────────
TAROT_SVG[4] = _wrap(4,'THE EMPEROR','#8B0000','#FF8C00','#FFA040','#8B4513','#6B3410',`
<path d="M3 115 L28 55 L42 80 L58 42 L72 70 L88 48 L97 68 L97 115Z" fill="#8B7355" opacity="0.75"/>
<path d="M58 42 L63 35 L68 42" fill="#FFFFF0" opacity="0.45"/>
<rect x="20" y="68" width="60" height="47" rx="3" fill="#808080" opacity="0.75"/>
<rect x="16" y="62" width="68" height="10" rx="2" fill="#696969" opacity="0.85"/>
<path d="M20 62 Q30 52 40 62" fill="none" stroke="#DAA520" stroke-width="1.8" opacity="0.75"/>
<circle cx="22" cy="60" r="3.5" fill="#DAA520" opacity="0.7"/>
<circle cx="38" cy="60" r="3.5" fill="#DAA520" opacity="0.7"/>
<path d="M60 62 Q70 52 80 62" fill="none" stroke="#DAA520" stroke-width="1.8" opacity="0.75"/>
<circle cx="62" cy="60" r="3.5" fill="#DAA520" opacity="0.7"/>
<circle cx="78" cy="60" r="3.5" fill="#DAA520" opacity="0.7"/>
<ellipse cx="50" cy="77" rx="20" ry="22" fill="#808080" opacity="0.82"/>
<circle cx="50" cy="52" r="11" fill="#FFDAB9" opacity="0.95"/>
<path d="M41 60 Q50 66 59 60 Q57 70 50 73 Q43 70 41 60" fill="#FFFFF0" opacity="0.85"/>
<rect x="38" y="40" width="24" height="9" rx="1" fill="#FFD700" opacity="0.92"/>
<path d="M38 40 L40 32 L43 40 M47 40 L50 32 L53 40 M57 40 L60 32 L62 40" stroke="#FFD700" stroke-width="1.8" opacity="0.85"/>
<circle cx="47" cy="50" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="50" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M63 64 L76 30" stroke="#FFD700" stroke-width="3" opacity="0.92"/>
<rect x="68" y="28" width="12" height="10" rx="1" fill="#FFD700" opacity="0.85"/>
<circle cx="34" cy="80" r="7" fill="#DAA520" opacity="0.75"/>
<path d="M31 75 L37 75 M34 72 L34 78" stroke="#FFFFF0" stroke-width="1.2" opacity="0.85"/>
<path d="M30 64 L20 115" stroke="#8B0000" stroke-width="8" opacity="0.55"/>
<path d="M70 64 L80 115" stroke="#8B0000" stroke-width="8" opacity="0.55"/>
`);

// ── 5 法王 ─────────────────────────────────────────────────────
TAROT_SVG[5] = _wrap(5,'THE HIEROPHANT','#9090ff','#C0A060','#A08040','#C0A060','#A08040',`
<rect x="8" y="18" width="15" height="97" rx="3" fill="#A0A0A0" opacity="0.75"/>
<rect x="77" y="18" width="15" height="97" rx="3" fill="#C8C8C8" opacity="0.75"/>
<ellipse cx="50" cy="72" rx="22" ry="30" fill="#FFFFF0" opacity="0.82"/>
<circle cx="50" cy="44" r="12" fill="#FFDAB9" opacity="0.95"/>
<rect x="38" y="32" width="24" height="8" rx="1" fill="#DAA520" opacity="0.92"/>
<rect x="40" y="25" width="20" height="8" rx="1" fill="#DAA520" opacity="0.92"/>
<rect x="43" y="19" width="14" height="7" rx="1" fill="#DAA520" opacity="0.92"/>
<path d="M43 19 L50 14 L57 19" fill="#DAA520" opacity="0.92"/>
<circle cx="47" cy="43" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="43" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 48 Q50 50 53 48" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M30 56 Q50 52 70 56 L72 102 L28 102Z" fill="#DC143C" opacity="0.72"/>
<path d="M65 56 L70 18" stroke="#DAA520" stroke-width="3" opacity="0.92"/>
<path d="M62 18 L73 18 M62 22 L73 22 M62 26 L73 26" stroke="#DAA520" stroke-width="1.8" opacity="0.85"/>
<path d="M36 114 L58 92 M44 114 L66 92" stroke="#DAA520" stroke-width="2.5" opacity="0.85"/>
<circle cx="36" cy="116" r="5" fill="#DAA520" opacity="0.75"/>
<circle cx="44" cy="116" r="5" fill="#C0C0C0" opacity="0.75"/>
<ellipse cx="28" cy="98" rx="10" ry="14" fill="#FFFACD" opacity="0.75"/>
<circle cx="28" cy="86" r="7" fill="#FFDAB9" opacity="0.85"/>
<ellipse cx="72" cy="98" rx="10" ry="14" fill="#FFFACD" opacity="0.75"/>
<circle cx="72" cy="86" r="7" fill="#FFDAB9" opacity="0.85"/>
<circle cx="38" cy="72" r="4" fill="#FF0000" opacity="0.55"/>
<circle cx="62" cy="72" r="4" fill="#FFFFF0" opacity="0.55"/>
<circle cx="50" cy="80" r="4" fill="#FF0000" opacity="0.55"/>
`);

// ── 6 恋人 ─────────────────────────────────────────────────────
TAROT_SVG[6] = _wrap(6,'THE LOVERS','#FF6347','#FFD700','#FFA500','#228B22','#1a6b18',`
<circle cx="50" cy="22" r="13" fill="#FF8C00" opacity="0.85"/>
<path d="M24 16 L28 8 L32 16 L36 8 L40 16" fill="none" stroke="#FF8C00" stroke-width="1.5" opacity="0.8"/>
<path d="M38 18 Q50 12 62 18" fill="none" stroke="#FFD700" stroke-width="2" opacity="0.7"/>
<path d="M60 16 L64 8 L68 16 L72 8 L76 16" fill="none" stroke="#FF8C00" stroke-width="1.5" opacity="0.8"/>
<ellipse cx="28" cy="30" rx="12" ry="15" fill="#FF6347" opacity="0.4"/>
<path d="M20 18 Q22 10 24 18" fill="#FFFACD" opacity="0.7"/>
<path d="M30 18 Q32 10 34 18" fill="#FFFACD" opacity="0.7"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<rect x="8" y="55" width="5" height="60" rx="1" fill="#8B4513" opacity="0.7"/>
<ellipse cx="10" cy="50" rx="10" ry="13" fill="#228B22" opacity="0.65"/>
<path d="M8 48 L16 44 M8 52 L14 48" stroke="#FF0000" stroke-width="0.8" opacity="0.6"/>
<rect x="87" y="60" width="5" height="55" rx="1" fill="#8B4513" opacity="0.7"/>
<ellipse cx="89" cy="55" rx="9" ry="12" fill="#228B22" opacity="0.65"/>
<ellipse cx="25" cy="82" rx="10" ry="22" fill="#FFDAB9" opacity="0.7"/>
<circle cx="25" cy="62" r="7" fill="#FFDAB9" opacity="0.9"/>
<path d="M20 56 Q25 50 30 56" fill="none" stroke="#DAA520" stroke-width="0.8" opacity="0.6"/>
<ellipse cx="75" cy="82" rx="10" ry="22" fill="#FFDAB9" opacity="0.7"/>
<circle cx="75" cy="62" r="7" fill="#FFDAB9" opacity="0.9"/>
<path d="M70 57 Q75 52 80 57" fill="none" stroke="#DAA520" stroke-width="0.8" opacity="0.6"/>
<path d="M48 64 L52 56 L56 64 L52 61Z" fill="#FF0000" opacity="0.6"/>
`);

// ── 7 戦車 ─────────────────────────────────────────────────────
TAROT_SVG[7] = _wrap(7,'THE CHARIOT','#00008B','#87CEEB','#aaccee','#228B22','#1a6b18',`
<path d="M3 115 Q30 108 60 112 Q80 108 97 112" fill="#6B8E23" opacity="0.5"/>
<rect x="15" y="72" width="70" height="28" rx="4" fill="#00008B" opacity="0.5"/>
<path d="M15 72 Q50 66 85 72" fill="#00008B" opacity="0.6"/>
<path d="M17 100 L17 115 M83 100 L83 115" stroke="#8B7355" stroke-width="2.5" opacity="0.65"/>
<ellipse cx="28" cy="113" rx="11" ry="6" fill="none" stroke="#8B7355" stroke-width="1.5" opacity="0.6"/>
<ellipse cx="72" cy="113" rx="11" ry="6" fill="none" stroke="#8B7355" stroke-width="1.5" opacity="0.6"/>
<rect x="16" y="72" width="68" height="28" rx="3" fill="none" stroke="#DAA520" stroke-width="1" opacity="0.5"/>
<path d="M38 72 Q50 68 62 72" fill="none" stroke="#DAA520" stroke-width="1.5" opacity="0.6"/>
<ellipse cx="50" cy="76" rx="12" ry="8" fill="#DAA520" opacity="0.4"/>
<path d="M44 70 L56 70 M50 66 L50 74" stroke="#DAA520" stroke-width="1.2" opacity="0.6"/>
<ellipse cx="50" cy="56" rx="14" ry="18" fill="#4169E1" opacity="0.4"/>
<circle cx="50" cy="42" r="10" fill="#FFDAB9" opacity="0.95"/>
<path d="M38 36 Q50 28 62 36 L62 42 L38 42Z" fill="#C0C0C0" opacity="0.8"/>
<text x="50" y="40" text-anchor="middle" font-size="10" fill="#DAA520" opacity="0.85">✦</text>
<circle cx="47" cy="41" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="41" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M38 50 Q50 46 62 50" fill="#C0C0C0" opacity="0.6"/>
<path d="M34 52 Q50 56 66 52" fill="none" stroke="#DAA520" stroke-width="0.8" opacity="0.5"/>
<circle cx="28" cy="104" r="4.5" fill="#FFFFF0" opacity="0.85"/>
<circle cx="72" cy="104" r="4.5" fill="#1C1C1C" opacity="0.85"/>
<path d="M28 70 L22 58 M72 70 L78 58" stroke="#1C1C1C" stroke-width="1.5" opacity="0.6"/>
`);

// ── 8 力 ─────────────────────────────────────────────────────
TAROT_SVG[8] = _wrap(8,'STRENGTH','#FF8C00','#87CEEB','#b0d8f0','#228B22','#1a6b18',`
<path d="M32 24 Q42 16 50 22 Q58 16 68 24 Q58 32 50 26 Q42 32 32 24" fill="none" stroke="#DAA520" stroke-width="2" opacity="0.95"/>
<circle cx="18" cy="28" r="5" fill="#FF69B4" opacity="0.7"/>
<circle cx="25" cy="24" r="4" fill="#FF1493" opacity="0.6"/>
<circle cx="82" cy="28" r="5" fill="#FF69B4" opacity="0.7"/>
<circle cx="75" cy="24" r="4" fill="#FF1493" opacity="0.6"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<ellipse cx="50" cy="82" rx="16" ry="25" fill="#FFFACD" opacity="0.8"/>
<circle cx="50" cy="58" r="10" fill="#FFDAB9" opacity="0.95"/>
<path d="M42 52 Q50 45 58 52" fill="none" stroke="#FFD700" stroke-width="1" opacity="0.7"/>
<circle cx="47" cy="57" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="57" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 62 Q50 64 53 62" fill="none" stroke="#c07050" stroke-width="1"/>
<ellipse cx="30" cy="86" rx="14" ry="10" fill="#DAA520" opacity="0.45"/>
<path d="M20 82 Q25 74 32 80 Q25 88 20 82" fill="#DAA520" opacity="0.55"/>
<path d="M22 84 Q28 88 34 84" fill="none" stroke="#8B4513" stroke-width="1.5" opacity="0.6"/>
<circle cx="32" cy="82" r="2" fill="#5D4037" opacity="0.7"/>
<circle cx="28" cy="78" r="2" fill="#5D4037" opacity="0.7"/>
<path d="M36 76 Q44 70 50 74 Q56 70 64 76" stroke="#DAA520" stroke-width="1.5" opacity="0.6"/>
<path d="M38 88 Q50 94 62 88" fill="#DAA520" opacity="0.2"/>
`);

// ── 9 隠者 ─────────────────────────────────────────────────────
TAROT_SVG[9] = _wrap(9,'THE HERMIT','#e0d080','#1a1a0a','#2a2a18','#8B7355','#6B5A3E',`
<path d="M3 115 L22 55 L36 80 L50 40 L64 65 L80 35 L97 55 L97 115Z" fill="#708090" opacity="0.75"/>
<path d="M50 40 L55 30 L60 40" fill="#FFFFF0" opacity="0.45"/>
<path d="M3 95 Q25 88 50 92 Q75 88 97 95 L97 115 L3 115Z" fill="#A9A9A9" opacity="0.4"/>
<ellipse cx="50" cy="74" rx="14" ry="26" fill="#808080" opacity="0.55"/>
<circle cx="50" cy="50" r="10" fill="#FFDAB9" opacity="0.85"/>
<path d="M42 45 Q50 38 58 45" fill="none" stroke="#C0C0C0" stroke-width="0.8" opacity="0.7"/>
<path d="M40 62 Q50 68 60 62 L62 100 L38 100Z" fill="#808080" opacity="0.6"/>
<path d="M40 45 L36 40 L44 42Z" fill="#C0C0C0" opacity="0.6"/>
<rect x="56" y="58" width="5" height="28" rx="2" fill="#8B4513" opacity="0.75"/>
<circle cx="58" cy="56" r="7" fill="#FFD700" opacity="0.45"/>
<circle cx="58" cy="56" r="3.5" fill="#FFD700" opacity="0.85"/>
<rect x="54" y="50" width="8" height="10" rx="1" fill="#DAA520" opacity="0.3"/>
<path d="M52 48 Q58 44 64 48" fill="none" stroke="#FFD700" stroke-width="0.8" opacity="0.5"/>
<polygon points="28,48 32,36 36,48" fill="none" stroke="#e0d080" stroke-width="0.8" opacity="0.5"/>
`);

// ── 10 運命の輪 ─────────────────────────────────────────────────────
TAROT_SVG[10] = _wrap(10,'WHEEL OF FORTUNE','#c080ff','#000033','#000055','#1a0a3a','#0a0520',`
<circle cx="50" cy="62" r="38" fill="none" stroke="#c080ff" stroke-width="1.5" opacity="0.6"/>
<circle cx="50" cy="62" r="28" fill="none" stroke="#9060d0" stroke-width="1" opacity="0.5"/>
<circle cx="50" cy="62" r="14" fill="#4B0082" opacity="0.6"/>
<path d="M50 24 L50 34 M50 90 L50 100 M12 62 L22 62 M78 62 L88 62" stroke="#c080ff" stroke-width="1.2" opacity="0.6"/>
<path d="M23 35 L31 43 M69 81 L77 89 M23 89 L31 81 M69 43 L77 35" stroke="#c080ff" stroke-width="1" opacity="0.5"/>
<text x="50" y="67" text-anchor="middle" font-size="14" fill="#c080ff" opacity="0.9" font-family="serif">☸</text>
<text x="50" y="28" text-anchor="middle" font-size="9" fill="#FFD700" opacity="0.8" font-family="serif">T</text>
<text x="84" y="65" text-anchor="middle" font-size="9" fill="#FFD700" opacity="0.8" font-family="serif">A</text>
<text x="50" y="98" text-anchor="middle" font-size="9" fill="#FFD700" opacity="0.8" font-family="serif">R</text>
<text x="16" y="65" text-anchor="middle" font-size="9" fill="#FFD700" opacity="0.8" font-family="serif">O</text>
<text x="50" y="34" text-anchor="middle" font-size="7" fill="#c080ff" opacity="0.65" font-family="serif">☿</text>
<text x="68" y="48" text-anchor="middle" font-size="7" fill="#c080ff" opacity="0.65" font-family="serif">♃</text>
<text x="68" y="80" text-anchor="middle" font-size="7" fill="#c080ff" opacity="0.65" font-family="serif">♂</text>
<text x="32" y="80" text-anchor="middle" font-size="7" fill="#c080ff" opacity="0.65" font-family="serif">♀</text>
<text x="32" y="48" text-anchor="middle" font-size="7" fill="#c080ff" opacity="0.65" font-family="serif">♄</text>
<text x="14" y="30" font-size="10" fill="#90EE90" opacity="0.75" font-family="serif">♌</text>
<text x="76" y="30" font-size="10" fill="#FFD700" opacity="0.75" font-family="serif">♉</text>
<text x="14" y="108" font-size="10" fill="#4169E1" opacity="0.75" font-family="serif">♏</text>
<text x="76" y="108" font-size="10" fill="#C0C0C0" opacity="0.75" font-family="serif">♒</text>
<path d="M18 28 Q14 35 18 42 Q24 32 18 28" fill="#DAA520" opacity="0.5"/>
<path d="M84 80 Q88 87 84 94 Q78 84 84 80" fill="#808080" opacity="0.5"/>
`);

// ── 11 正義 ─────────────────────────────────────────────────────
TAROT_SVG[11] = _wrap(11,'JUSTICE','#4169E1','#FFD700','#FFA500','#C0A060','#A08040',`
<rect x="8" y="20" width="15" height="95" rx="3" fill="#A0A0A0" opacity="0.75"/>
<rect x="77" y="20" width="15" height="95" rx="3" fill="#C8C8C8" opacity="0.75"/>
<ellipse cx="50" cy="76" rx="22" ry="30" fill="#DC143C" opacity="0.55"/>
<circle cx="50" cy="46" r="11" fill="#FFDAB9" opacity="0.95"/>
<rect x="38" y="34" width="24" height="8" rx="1" fill="#FFD700" opacity="0.9"/>
<path d="M38 34 L40 27 L43 34 M47 34 L50 27 L53 34 M57 34 L60 27 L62 34" stroke="#FFD700" stroke-width="1.8" opacity="0.85"/>
<circle cx="47" cy="45" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="45" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 50 Q50 52 53 50" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M62 55 L74 26" stroke="#C0C0C0" stroke-width="2" opacity="0.8"/>
<path d="M60 26 L78 26" stroke="#C0C0C0" stroke-width="1.5" opacity="0.75"/>
<path d="M30 60 L22 50 L34 54Z M30 60 L22 72 L34 68Z" fill="none" stroke="#DAA520" stroke-width="1.5" opacity="0.75"/>
<path d="M28 60 L36 60" stroke="#DAA520" stroke-width="1.5" opacity="0.65"/>
<path d="M36 66 Q50 62 64 66 L64 100 L36 100Z" fill="#FFFFF0" opacity="0.7"/>
<path d="M34 74 Q50 78 66 74" stroke="#4169E1" stroke-width="0.8" opacity="0.5"/>
`);

// ── 12 吊られた男 ─────────────────────────────────────────────────────
TAROT_SVG[12] = _wrap(12,'THE HANGED MAN','#4080d0','#87CEEB','#b0d8f0','#228B22','#1a6b18',`
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<rect x="20" y="18" width="8" height="70" rx="3" fill="#8B4513" opacity="0.82"/>
<rect x="72" y="18" width="8" height="70" rx="3" fill="#8B4513" opacity="0.82"/>
<rect x="20" y="18" width="60" height="8" rx="3" fill="#8B4513" opacity="0.82"/>
<path d="M50 26 L50 38" stroke="#808080" stroke-width="1.5" opacity="0.8"/>
<circle cx="50" cy="44" r="11" fill="#FFDAB9" opacity="0.95"/>
<circle cx="50" cy="42" r="9" fill="none" stroke="#FFD700" stroke-width="1.2" opacity="0.8"/>
<circle cx="47" cy="43" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="43" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 48 Q50 50 53 48" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M38 56 L28 72 M62 56 L72 72" stroke="#4080d0" stroke-width="1.8" opacity="0.65"/>
<path d="M38 56 Q50 62 62 56" fill="none" stroke="#4080d0" stroke-width="1.5" opacity="0.6"/>
<path d="M28 72 L36 76 M72 72 L64 76" stroke="#4080d0" stroke-width="1" opacity="0.55"/>
<path d="M36 76 Q50 82 64 76" fill="none" stroke="#4080d0" stroke-width="1" opacity="0.55"/>
<path d="M62 62 L70 55" stroke="#FFDAB9" stroke-width="2.5" opacity="0.7"/>
<path d="M38 68 L30 62" stroke="#FFDAB9" stroke-width="2.5" opacity="0.7"/>
`);

// ── 13 死神 ─────────────────────────────────────────────────────
TAROT_SVG[13] = _wrap(13,'DEATH','#a0a0b0','#191919','#303040','#2F4F4F','#1a3a2a',`
<path d="M3 115 L28 50 L42 75 L58 38 L72 65 L88 45 L97 62 L97 115Z" fill="#2F4F4F" opacity="0.75"/>
<path d="M3 100 Q50 92 97 100 L97 115 L3 115Z" fill="#006400" opacity="0.45"/>
<path d="M58 38 L63 30 L68 38" fill="#FFFFF0" opacity="0.4"/>
<ellipse cx="50" cy="70" rx="16" ry="24" fill="#1C1C1C" opacity="0.75"/>
<circle cx="50" cy="48" r="10" fill="#C0C0C0" opacity="0.75"/>
<path d="M42 44 Q50 36 58 44" fill="none" stroke="#808080" stroke-width="1" opacity="0.7"/>
<circle cx="46" cy="46" r="2" fill="#000" opacity="0.9"/>
<circle cx="54" cy="46" r="2" fill="#000" opacity="0.9"/>
<path d="M45 52 L55 52" stroke="#808080" stroke-width="1" opacity="0.6"/>
<rect x="55" y="35" width="4" height="28" rx="1" fill="#A9A9A9" opacity="0.7"/>
<rect x="52" y="35" width="10" height="5" rx="1" fill="#FFFFF0" opacity="0.75"/>
<path d="M52 40 Q57 44 62 40" fill="#000" opacity="0.6"/>
<text x="57" y="45" text-anchor="middle" font-size="7" fill="#FFFFF0" opacity="0.7" font-family="serif">☩</text>
<circle cx="22" cy="98" r="6" fill="#FFDAB9" opacity="0.5"/>
<path d="M16 104 Q22 96 28 104" fill="none" stroke="#808080" stroke-width="0.8" opacity="0.5"/>
<circle cx="72" cy="94" r="5" fill="#FFD700" opacity="0.4"/>
<path d="M22 52 Q28 44 34 52" stroke="#2F4F4F" stroke-width="1" opacity="0.5"/>
<path d="M68 58 Q74 50 80 58" stroke="#2F4F4F" stroke-width="1" opacity="0.5"/>
`);

// ── 14 節制 ─────────────────────────────────────────────────────
TAROT_SVG[14] = _wrap(14,'TEMPERANCE','#20c080','#87CEEB','#a8d8ea','#228B22','#1a6b18',`
<circle cx="72" cy="24" r="13" fill="#FFD700" opacity="0.85"/>
<path d="M72 9 L72 5 M86 20 L90 20 M81 13 L84 10 M81 25 L84 28 M63 13 L60 10" stroke="#FFD700" stroke-width="1.2" opacity="0.8"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<path d="M3 105 Q25 98 50 102 Q75 98 97 102 L97 115 L3 115Z" fill="#4169E1" opacity="0.35"/>
<rect x="8" y="55" width="5" height="60" rx="1" fill="#8B4513" opacity="0.7"/>
<ellipse cx="10" cy="50" rx="10" ry="13" fill="#228B22" opacity="0.6"/>
<ellipse cx="50" cy="72" rx="18" ry="28" fill="#FFFACD" opacity="0.82"/>
<circle cx="50" cy="46" r="11" fill="#FFDAB9" opacity="0.95"/>
<path d="M40 40 Q50 33 60 40" fill="none" stroke="#FFFACD" stroke-width="1" opacity="0.7"/>
<circle cx="47" cy="45" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="45" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 50 Q50 52 53 50" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M38 35 Q36 25 38 36 Q40 28 38 35" fill="#FFFACD" opacity="0.7"/>
<path d="M62 35 Q64 25 62 36 Q60 28 62 35" fill="#FFFACD" opacity="0.7"/>
<path d="M32 58 Q30 50 32 62 L28 62Z" fill="#4169E1" opacity="0.45"/>
<path d="M68 58 Q70 50 68 62 L72 62Z" fill="#4169E1" opacity="0.45"/>
<path d="M32 58 Q50 52 68 58" fill="none" stroke="#4169E1" stroke-width="1.2" opacity="0.65"/>
<text x="50" y="65" text-anchor="middle" font-size="9" fill="#FFD700" opacity="0.65" font-family="serif">△</text>
<circle cx="38" cy="90" r="5" fill="#DAA520" opacity="0.55"/>
<path d="M35 87 L41 87 M38 84 L38 90" stroke="#FFFFF0" stroke-width="1" opacity="0.8"/>
`);

// ── 15 悪魔 ─────────────────────────────────────────────────────
TAROT_SVG[15] = _wrap(15,'THE DEVIL','#c04040','#0D0000','#1a0000','#1a0000','#0a0000',`
<ellipse cx="50" cy="36" rx="20" ry="18" fill="#2D0000" opacity="0.8"/>
<path d="M33 28 L26 15 M67 28 L74 15" stroke="#c04040" stroke-width="2" opacity="0.85"/>
<path d="M26 15 L32 20 M74 15 L68 20" stroke="#c04040" stroke-width="1.2" opacity="0.75"/>
<path d="M40 18 Q50 10 60 18" fill="#c04040" opacity="0.55"/>
<circle cx="44" cy="33" r="2.5" fill="#FF0000" opacity="0.9"/>
<circle cx="56" cy="33" r="2.5" fill="#FF0000" opacity="0.9"/>
<path d="M43 40 Q50 45 57 40" fill="none" stroke="#c04040" stroke-width="1.2" opacity="0.8"/>
<text x="50" y="27" text-anchor="middle" font-size="10" fill="#c04040" opacity="0.85" font-family="serif">⁂</text>
<path d="M34 46 Q26 46 24 36" fill="#8B0000" opacity="0.4"/>
<path d="M66 46 Q74 46 76 36" fill="#8B0000" opacity="0.4"/>
<ellipse cx="30" cy="82" rx="10" ry="18" fill="#8B0000" opacity="0.45"/>
<circle cx="30" cy="66" r="7" fill="#FFDAB9" opacity="0.7"/>
<ellipse cx="70" cy="82" rx="10" ry="18" fill="#8B0000" opacity="0.45"/>
<circle cx="70" cy="66" r="7" fill="#FFDAB9" opacity="0.7"/>
<path d="M30 52 Q50 58 70 52" stroke="#c04040" stroke-width="1.5" opacity="0.65"/>
<circle cx="50" cy="54" r="5" fill="#c04040" opacity="0.65"/>
<path d="M24 70 L36 70 M40 84 L60 84 M64 70 L76 70" stroke="#c04040" stroke-width="1" opacity="0.55"/>
<path d="M30 74 L30 80 M70 74 L70 80" stroke="#c04040" stroke-width="1" opacity="0.5"/>
<path d="M26 84 Q28 92 30 100" stroke="#8B0000" stroke-width="1" opacity="0.5"/>
<path d="M74 84 Q72 92 70 100" stroke="#8B0000" stroke-width="1" opacity="0.5"/>
`);

// ── 16 塔 ─────────────────────────────────────────────────────
TAROT_SVG[16] = _wrap(16,'THE TOWER','#ff8040','#0f0800','#1a1000','#2F4F4F','#1a3a2a',`
<path d="M3 115 L28 55 L42 80 L58 45 L72 70 L88 52 L97 68 L97 115Z" fill="#2F4F4F" opacity="0.65"/>
<path d="M3 100 Q50 94 97 100 L97 115 L3 115Z" fill="#8B0000" opacity="0.35"/>
<rect x="32" y="22" width="36" height="68" rx="3" fill="#808080" opacity="0.8"/>
<path d="M32 22 Q50 14 68 22" fill="#A9A9A9" opacity="0.85"/>
<circle cx="50" cy="18" r="6" fill="#FFD700" opacity="0.8"/>
<rect x="40" y="32" width="20" height="12" rx="2" fill="#1C1C1C" opacity="0.7"/>
<rect x="40" y="52" width="20" height="12" rx="2" fill="#1C1C1C" opacity="0.7"/>
<rect x="40" y="72" width="20" height="10" rx="2" fill="#1C1C1C" opacity="0.65"/>
<path d="M12 28 L26 50 L20 50 L32 68" stroke="#FFD700" stroke-width="2.5" opacity="0.9"/>
<path d="M10 25 L14 30" stroke="#FFD700" stroke-width="1.5" opacity="0.8"/>
<path d="M88 24 L74 46 L80 46 L68 64" stroke="#FFD700" stroke-width="2" opacity="0.85"/>
<path d="M90 21 L86 26" stroke="#FFD700" stroke-width="1.5" opacity="0.8"/>
<circle cx="26" cy="84" r="6" fill="#FFDAB9" opacity="0.7"/>
<path d="M24 80 L22 95" stroke="#808080" stroke-width="1.2" opacity="0.6"/>
<circle cx="74" cy="80" r="5" fill="#FFDAB9" opacity="0.7"/>
<path d="M74 76 L76 92" stroke="#808080" stroke-width="1.2" opacity="0.6"/>
<circle cx="18" cy="52" r="3" fill="#FFD700" opacity="0.6"/>
<circle cx="82" cy="46" r="3" fill="#FFD700" opacity="0.6"/>
<circle cx="22" cy="38" r="2.5" fill="#FFD700" opacity="0.5"/>
`);

// ── 17 星 ─────────────────────────────────────────────────────
TAROT_SVG[17] = _wrap(17,'THE STAR','#80c0ff','#020510','#040820','#228B22','#1a6b18',`
<circle cx="50" cy="30" r="11" fill="#FFD700" opacity="0.75"/>
<path d="M50 18 L50 13 M62 24 L67 21 M65 33 L70 33 M62 40 L67 43 M50 42 L50 47 M38 40 L33 43 M35 33 L30 33 M38 24 L33 21" stroke="#FFD700" stroke-width="1.2" opacity="0.75"/>
<circle cx="18" cy="22" r="4.5" fill="#80c0ff" opacity="0.75"/>
<circle cx="78" cy="18" r="3.5" fill="#80c0ff" opacity="0.65"/>
<circle cx="84" cy="34" r="3" fill="#80c0ff" opacity="0.6"/>
<circle cx="15" cy="44" r="3" fill="#80c0ff" opacity="0.55"/>
<circle cx="82" cy="50" r="2.5" fill="#80c0ff" opacity="0.5"/>
<circle cx="22" cy="58" r="2.5" fill="#80c0ff" opacity="0.5"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<path d="M3 100 Q25 95 50 98 Q75 95 97 100 L97 115 L3 115Z" fill="#4169E1" opacity="0.35"/>
<ellipse cx="40" cy="82" rx="12" ry="25" fill="#FFDAB9" opacity="0.6"/>
<circle cx="40" cy="58" r="9" fill="#FFDAB9" opacity="0.88"/>
<path d="M33 52 Q40 46 47 52" fill="none" stroke="#FFD700" stroke-width="0.8" opacity="0.7"/>
<circle cx="37" cy="57" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="43" cy="57" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M28 70 Q28 64 32 68" fill="none" stroke="#80c0ff" stroke-width="1.5" opacity="0.7"/>
<path d="M28 70 Q28 76 32 72" fill="#4169E1" opacity="0.45"/>
<path d="M52 70 Q52 64 48 68" fill="none" stroke="#80c0ff" stroke-width="1.5" opacity="0.7"/>
<path d="M52 70 Q52 76 48 72" fill="#4169E1" opacity="0.45"/>
<rect x="65" y="55" width="5" height="58" rx="1" fill="#8B4513" opacity="0.7"/>
<ellipse cx="67" cy="50" rx="12" ry="14" fill="#228B22" opacity="0.65"/>
<circle cx="70" cy="45" r="3" fill="#80c0ff" opacity="0.6"/>
`);

// ── 18 月 ─────────────────────────────────────────────────────
TAROT_SVG[18] = _wrap(18,'THE MOON','#8080c0','#020208','#040418','#4169E1','#2a4a9a',`
<circle cx="50" cy="26" r="14" fill="#C0C0C0" opacity="0.55"/>
<path d="M44 17 Q36 26 44 35 Q50 28 50 26 Q50 24 44 17" fill="#808080" opacity="0.65"/>
<circle cx="47" cy="22" r="3" fill="#FFDAB9" opacity="0.6"/>
<path d="M34 18 Q30 22 32 28" fill="none" stroke="#DAA520" stroke-width="0.8" opacity="0.5"/>
<rect x="8" y="18" width="14" height="75" rx="3" fill="#808080" opacity="0.65"/>
<path d="M9 18 Q15 12 21 18" fill="#808080" opacity="0.65"/>
<rect x="78" y="18" width="14" height="75" rx="3" fill="#909090" opacity="0.65"/>
<path d="M79 18 Q85 12 91 18" fill="#909090" opacity="0.65"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<path d="M3 96 Q50 88 97 96 L97 115 L3 115Z" fill="#4169E1" opacity="0.4"/>
<ellipse cx="26" cy="96" rx="9" ry="6" fill="#DAA520" opacity="0.45"/>
<path d="M20 94 Q26 88 32 94" fill="none" stroke="#8B4513" stroke-width="1.2" opacity="0.6"/>
<path d="M22 96 L26 90 L30 96" fill="none" stroke="#8B4513" stroke-width="0.8" opacity="0.5"/>
<ellipse cx="74" cy="96" rx="9" ry="6" fill="#C0C0C0" opacity="0.45"/>
<path d="M68 94 Q74 88 80 94" fill="none" stroke="#808080" stroke-width="1.2" opacity="0.6"/>
<circle cx="50" cy="102" r="7" fill="#4169E1" opacity="0.65"/>
<path d="M46 100 Q50 96 54 100 M44 103 L56 103" stroke="#00CED1" stroke-width="0.8" opacity="0.7"/>
<path d="M3 82 Q25 76 50 80 Q75 76 97 82" fill="none" stroke="#8080c0" stroke-width="1" opacity="0.5" stroke-dasharray="3,3"/>
`);

// ── 19 太陽 ─────────────────────────────────────────────────────
TAROT_SVG[19] = _wrap(19,'THE SUN','#FFD700','#FFFACD','#FFE566','#C8A040','#B09030',`
<circle cx="50" cy="28" r="16" fill="#FFD700" opacity="0.85"/>
<circle cx="50" cy="28" r="9" fill="#FF8C00" opacity="0.65"/>
<path d="M50 8 L50 4 M50 48 L50 52 M30 28 L26 28 M70 28 L74 28 M36 14 L33 11 M64 42 L67 45 M36 42 L33 45 M64 14 L67 11" stroke="#FFD700" stroke-width="1.8" opacity="0.9"/>
<path d="M38 10 L35 7 M62 10 L65 7 M38 46 L35 49 M62 46 L65 49" stroke="#FFD700" stroke-width="1.2" opacity="0.8"/>
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#6B8E23" opacity="0.5"/>
<rect x="10" y="80" width="80" height="35" rx="2" fill="#A0522D" opacity="0.3"/>
<path d="M10 80 Q50 72 90 80" fill="#8B7355" opacity="0.35"/>
<path d="M3 100 Q50 95 97 100 L97 115 L3 115Z" fill="#6B8E23" opacity="0.4"/>
<ellipse cx="50" cy="74" rx="14" ry="26" fill="#FFDAB9" opacity="0.65"/>
<circle cx="50" cy="52" r="11" fill="#FFDAB9" opacity="0.95"/>
<path d="M40 46 Q50 40 60 46" fill="none" stroke="#FFD700" stroke-width="1" opacity="0.75"/>
<circle cx="47" cy="51" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="51" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 56 Q50 58 53 56" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M20 90 Q22 78 28 88 Q34 76 20 72" fill="#C0A060" opacity="0.5"/>
<path d="M22 80 Q28 84 34 80 Q28 76 22 80" fill="#8B7355" opacity="0.4"/>
`);

// ── 20 審判 ─────────────────────────────────────────────────────
TAROT_SVG[20] = _wrap(20,'JUDGEMENT','#e0e0ff','#050505','#101020','#00008B','#000055',`
<path d="M3 115 Q25 108 50 112 Q75 108 97 112" fill="#4169E1" opacity="0.45"/>
<ellipse cx="50" cy="38" rx="18" ry="22" fill="#e0e0ff" opacity="0.2"/>
<circle cx="50" cy="28" r="9" fill="#FFDAB9" opacity="0.8"/>
<path d="M36 22 Q50 13 64 22 L64 28 L36 28Z" fill="#FF4500" opacity="0.65"/>
<text x="50" y="27" text-anchor="middle" font-size="9" fill="#DAA520" opacity="0.9" font-family="serif">✦</text>
<path d="M24 18 Q26 8 28 18" fill="#FFFACD" opacity="0.75"/>
<path d="M32 16 Q34 6 36 16" fill="#FFFACD" opacity="0.75"/>
<path d="M64 16 Q66 6 68 16" fill="#FFFACD" opacity="0.75"/>
<path d="M72 18 Q74 8 76 18" fill="#FFFACD" opacity="0.75"/>
<path d="M34 36 L46 50" stroke="#e0e0ff" stroke-width="1.2" opacity="0.65"/>
<path d="M30 50 L70 50" stroke="#FFD700" stroke-width="1.2" opacity="0.65"/>
<text x="50" y="48" text-anchor="middle" font-size="11" fill="#FFD700" opacity="0.8" font-family="serif">♪</text>
<rect x="14" y="75" width="18" height="24" rx="2" fill="#808080" opacity="0.55"/>
<rect x="42" y="68" width="16" height="30" rx="2" fill="#A9A9A9" opacity="0.55"/>
<rect x="68" y="75" width="18" height="24" rx="2" fill="#808080" opacity="0.55"/>
<circle cx="23" cy="72" r="6" fill="#FFDAB9" opacity="0.75"/>
<circle cx="50" cy="65" r="7" fill="#FFDAB9" opacity="0.75"/>
<circle cx="77" cy="72" r="6" fill="#FFDAB9" opacity="0.75"/>
<path d="M20 68 Q25 62 30 68" fill="none" stroke="#e0e0ff" stroke-width="0.8" opacity="0.6"/>
<path d="M46 61 Q50 55 54 61" fill="none" stroke="#e0e0ff" stroke-width="0.8" opacity="0.6"/>
<path d="M72 68 Q77 62 82 68" fill="none" stroke="#e0e0ff" stroke-width="0.8" opacity="0.6"/>
`);

// ── 21 世界 ─────────────────────────────────────────────────────
TAROT_SVG[21] = _wrap(21,'THE WORLD','#40c080','#020508','#040a10','#000a15','#000510',`
<ellipse cx="50" cy="62" rx="36" ry="48" fill="none" stroke="#40c080" stroke-width="2" opacity="0.65"/>
<ellipse cx="50" cy="62" rx="26" ry="38" fill="none" stroke="#228B22" stroke-width="0.8" opacity="0.4"/>
<path d="M14 62 Q15 44 24 30 Q28 46 20 62 Q28 78 24 94 Q15 80 14 62" fill="#228B22" opacity="0.4"/>
<path d="M86 62 Q85 44 76 30 Q72 46 80 62 Q72 78 76 94 Q85 80 86 62" fill="#228B22" opacity="0.4"/>
<ellipse cx="50" cy="62" rx="14" ry="24" fill="#FFDAB9" opacity="0.35"/>
<circle cx="50" cy="46" r="10" fill="#FFDAB9" opacity="0.9"/>
<path d="M42 40 Q50 33 58 40" fill="none" stroke="#40c080" stroke-width="1" opacity="0.75"/>
<circle cx="47" cy="45" r="1.3" fill="#5D4037" opacity="0.8"/>
<circle cx="53" cy="45" r="1.3" fill="#5D4037" opacity="0.8"/>
<path d="M47 50 Q50 52 53 50" fill="none" stroke="#c07050" stroke-width="1"/>
<path d="M38 56 L30 66 M62 56 L70 66" stroke="#FFDAB9" stroke-width="1.5" opacity="0.65"/>
<path d="M38 68 L30 58" stroke="#FFDAB9" stroke-width="1.5" opacity="0.65"/>
<path d="M44 80 Q50 88 56 80 Q62 72 56 64 Q50 56 44 64 Q38 72 44 80" fill="none" stroke="#40c080" stroke-width="1" opacity="0.65"/>
<text x="14" y="26" font-size="11" fill="#90EE90" opacity="0.8" font-family="serif">♌</text>
<text x="74" y="26" font-size="11" fill="#FFD700" opacity="0.8" font-family="serif">♉</text>
<text x="14" y="106" font-size="11" fill="#4169E1" opacity="0.8" font-family="serif">♏</text>
<text x="74" y="106" font-size="11" fill="#C0C0C0" opacity="0.8" font-family="serif">♒</text>
`);

// ── マスターリスト ──────────────────────────────────────────────
const TAROT_FULL = [
  {n:0, name:'愚者',       wx:'water', sym:'🌟', keywords:'自由・出発・可能性',   svg:TAROT_SVG[0]},
  {n:1, name:'魔術師',     wx:'fire',  sym:'⚡', keywords:'意志・技術・実現力',   svg:TAROT_SVG[1]},
  {n:2, name:'女教皇',     wx:'water', sym:'🌙', keywords:'直感・神秘・潜在意識', svg:TAROT_SVG[2]},
  {n:3, name:'女帝',       wx:'earth', sym:'🌸', keywords:'豊穣・母性・創造',     svg:TAROT_SVG[3]},
  {n:4, name:'皇帝',       wx:'metal', sym:'👑', keywords:'権威・構造・安定',     svg:TAROT_SVG[4]},
  {n:5, name:'法王',       wx:'earth', sym:'🏛', keywords:'伝統・教義・精神指導', svg:TAROT_SVG[5]},
  {n:6, name:'恋人',       wx:'fire',  sym:'💞', keywords:'愛・選択・調和',       svg:TAROT_SVG[6]},
  {n:7, name:'戦車',       wx:'water', sym:'🏆', keywords:'勝利・意志力・突破',   svg:TAROT_SVG[7]},
  {n:8, name:'力',         wx:'fire',  sym:'🦁', keywords:'勇気・忍耐・内なる力', svg:TAROT_SVG[8]},
  {n:9, name:'隠者',       wx:'earth', sym:'🕯', keywords:'内省・孤独・知恵',     svg:TAROT_SVG[9]},
  {n:10,name:'運命の輪',   wx:'earth', sym:'☯', keywords:'変化・サイクル・運命', svg:TAROT_SVG[10]},
  {n:11,name:'正義',       wx:'metal', sym:'⚖', keywords:'公平・真実・法',       svg:TAROT_SVG[11]},
  {n:12,name:'吊られた男', wx:'water', sym:'🔄', keywords:'犠牲・新視点・待機',   svg:TAROT_SVG[12]},
  {n:13,name:'死神',       wx:'water', sym:'🥀', keywords:'終わり・変容・再生',   svg:TAROT_SVG[13]},
  {n:14,name:'節制',       wx:'fire',  sym:'🌈', keywords:'調和・均衡・癒し',     svg:TAROT_SVG[14]},
  {n:15,name:'悪魔',       wx:'earth', sym:'⛓', keywords:'束縛・物質・欲望',     svg:TAROT_SVG[15]},
  {n:16,name:'塔',         wx:'fire',  sym:'🌩', keywords:'崩壊・啓示・変革',     svg:TAROT_SVG[16]},
  {n:17,name:'星',         wx:'water', sym:'✨', keywords:'希望・回復・霊感',     svg:TAROT_SVG[17]},
  {n:18,name:'月',         wx:'water', sym:'🌕', keywords:'幻想・不安・無意識',   svg:TAROT_SVG[18]},
  {n:19,name:'太陽',       wx:'fire',  sym:'☀', keywords:'喜び・成功・活力',     svg:TAROT_SVG[19]},
  {n:20,name:'審判',       wx:'fire',  sym:'🎺', keywords:'覚醒・再生・使命',     svg:TAROT_SVG[20]},
  {n:21,name:'世界',       wx:'earth', sym:'🌍', keywords:'完成・統合・達成',     svg:TAROT_SVG[21]},
];
