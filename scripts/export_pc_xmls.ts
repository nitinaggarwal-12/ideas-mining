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
  const targetPath = path.join(outDir, `${tid}.drawio`);
  fs.writeFileSync(targetPath, healed.xml, 'utf8');
  console.log(`[export_pc_xmls] ${tid} (PromptCanvas #${pcId}) -> ${targetPath} (${healed.xml.length} bytes, valid=${healed.valid})`);
}
