/** Render precomputed SVG figures using an existing Sharp installation; no downloads. */
import {createRequire} from 'node:module';
import {readdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
const [directory,moduleRoot]=process.argv.slice(2);
if(!directory||!moduleRoot)throw Error('Usage: node render_quality_charts.mjs CHART_DIRECTORY EXISTING_NODE_RUNTIME_ROOT');
const require=createRequire(path.join(path.resolve(moduleRoot),'quality-chart-resolution.cjs'));
const sharp=require('sharp');
const records=[];
for(const file of (await readdir(directory)).filter(x=>x.endsWith('.svg')).sort()){
 const input=path.join(directory,file),output=input.replace(/\.svg$/,'.png');
 await sharp(input,{density:300}).png().withMetadata({density:300}).toFile(output);
 const meta=await sharp(output).metadata();if(meta.density!==300)throw Error('PNG density mismatch');
 records.push({svg:file,png:path.basename(output),width:meta.width,height:meta.height,dpi:meta.density});
}
await writeFile(path.join(directory,'render-manifest.json'),JSON.stringify({renderer:'Sharp',versions:sharp.versions,figures:records},null,2)+'\n');
console.log(JSON.stringify(records));
