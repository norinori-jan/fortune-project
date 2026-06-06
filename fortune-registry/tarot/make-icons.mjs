import { createRequire } from "module";
const require = createRequire(import.meta.url);
const fs = require("fs"), zlib = require("zlib");
function createPNG(size, color) {
  const sig = Buffer.from([137,80,78,71,13,10,26,10]);
  function crc32(buf){let c=0xFFFFFFFF,t=[];for(let i=0;i<256;i++){let n=i;for(let j=0;j<8;j++)n=n&1?0xEDB88320^(n>>>1):n>>>1;t[i]=n;}for(let i=0;i<buf.length;i++)c=t[(c^buf[i])&0xFF]^(c>>>8);return(c^0xFFFFFFFF)>>>0;}
  function chunk(type,data){const len=Buffer.alloc(4);len.writeUInt32BE(data.length);const t=Buffer.from(type);const cb=Buffer.concat([t,data]);const c=Buffer.alloc(4);c.writeUInt32BE(crc32(cb));return Buffer.concat([len,t,data,c]);}
  const ihdr=Buffer.alloc(13);ihdr.writeUInt32BE(size,0);ihdr.writeUInt32BE(size,4);ihdr[8]=8;ihdr[9]=2;
  const [r,g,b]=color, rows=[];
  for(let y=0;y<size;y++){const row=Buffer.alloc(1+size*3);row[0]=0;for(let x=0;x<size;x++){const cx=size/2,cy=size/2,dx=x-cx,dy=y-cy;let pr=r,pg=g,pb=b;const s=size/192;
    // 星形シンボル
    const dist=Math.sqrt(dx*dx+dy*dy);const angle=Math.atan2(dy,dx);const star=Math.cos(5*angle)*size*0.12+size*0.22;
    if(dist<star&&dist>size*0.08){pr=201;pg=168;pb=76;}
    row[1+x*3]=pr;row[2+x*3]=pg;row[3+x*3]=pb;}rows.push(row);}
  const raw=Buffer.concat(rows);const comp=zlib.deflateSync(raw,{level:6});
  return Buffer.concat([sig,chunk("IHDR",ihdr),chunk("IDAT",comp),chunk("IEND",Buffer.alloc(0))]);
}
const dir = "C:/Users/norin/fortune-project/fortune-registry/tarot";
for(const size of [192,512]){fs.writeFileSync(`${dir}/icon-${size}.png`,createPNG(size,[7,5,15]));console.log(`✓ icon-${size}.png`);}
