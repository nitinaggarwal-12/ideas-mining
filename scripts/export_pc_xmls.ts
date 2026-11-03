import * as fs from 'fs';
import * as path from 'path';
import { generateInfographicBlueprintXmlById } from '../../PromptCanvas/src/lib/canonical/infographicBlueprints52to66';
import { generateOpenKnowledgeInfographicXml } from '../../PromptCanvas/src/lib/canonical/openKnowledgeInfographic';
import { validateAndHealDrawioXml } from '../../PromptCanvas/src/lib/xmlHealer';

const outDir = path.resolve(__dirname, '../assets/canonical-ref/drawio');
fs.mkdirSync(outDir, { recursive: true });

const MAPPING: Array<{ tid: string; pcId: string }> = [
  { tid: 'T53', pcId: '52' },
  { tid: 'T54', pcId: '53' },
  { tid: 'T55', pcId: '54' },
  { tid: 'T56', pcId: '55' },
  { tid: 'T57', pcId: '56' },
  { tid: 'T58', pcId: '57' },
  { tid: 'T59', pcId: '58' },
  { tid: 'T60', pcId: '59' },
  { tid: 'T61', pcId: '60' },
  { tid: 'T62', pcId: '61' },
  { tid: 'T63', pcId: '62' },
  { tid: 'T64', pcId: '63' },
  { tid: 'T65', pcId: '64' },
  { tid: 'T66', pcId: '65' },
  { tid: 'T67', pcId: '66' },
  { tid: 'T68', pcId: 'open_knowledge' },
];

for (const { tid, pcId } of MAPPING) {
  const rawXml =
    pcId === 'open_knowledge'
      ? generateOpenKnowledgeInfographicXml('general', 'light')
      : generateInfographicBlueprintXmlById(pcId);
  const healed = validateAndHealDrawioXml(rawXml);
  let outXml = healed.xml;
  if (tid === 'T67') {
    outXml = outXml.replace(
      '&lt;!-- 3. BOTTOM-RIGHT BIFURCATING GREEN ARROWS: PASS --&gt;&lt;path d=&quot;M 577 553 Q 545 604 494 636&quot; fill=&quot;none&quot; stroke=&quot;#329E4B&quot; stroke-width=&quot;4&quot; stroke-linecap=&quot;round&quot;/&gt;&lt;polygon points=&quot;483,642 494,626 502,640&quot; fill=&quot;#329E4B&quot;/&gt;&lt;path d=&quot;M 577 553 Q 556 624 612 648&quot; fill=&quot;none&quot; stroke=&quot;#329E4B&quot; stroke-width=&quot;4&quot; stroke-linecap=&quot;round&quot;/&gt;&lt;polygon points=&quot;624,651 606,654 612,639&quot; fill=&quot;#329E4B&quot;/&gt;&lt;text x=&quot;515&quot; y=&quot;601&quot; font-family=&quot;Inter, -apple-system, sans-serif&quot; font-size=&quot;15&quot; font-weight=&quot;800&quot; fill=&quot;#0F2143&quot; text-anchor=&quot;middle&quot;&gt;PASS&lt;/text&gt;',
      '&lt;!-- 3. BOTTOM-RIGHT EXIT GREEN ARROW: PASS --&gt;&lt;path d=&quot;M 577 553 Q 556 624 612 648&quot; fill=&quot;none&quot; stroke=&quot;#329E4B&quot; stroke-width=&quot;4&quot; stroke-linecap=&quot;round&quot;/&gt;&lt;polygon points=&quot;624,651 606,654 612,639&quot; fill=&quot;#329E4B&quot;/&gt;&lt;text x=&quot;544&quot; y=&quot;610&quot; font-family=&quot;Inter, -apple-system, sans-serif&quot; font-size=&quot;15&quot; font-weight=&quot;800&quot; fill=&quot;#0F2143&quot; text-anchor=&quot;middle&quot;&gt;PASS&lt;/text&gt;'
    );
  }
  const targetPath = path.join(outDir, `${tid}.drawio`);
  fs.writeFileSync(targetPath, outXml, 'utf8');
  console.log(`[export_pc_xmls] ${tid} (PromptCanvas #${pcId}) -> ${targetPath} (${outXml.length} bytes, valid=${healed.valid})`);
}
