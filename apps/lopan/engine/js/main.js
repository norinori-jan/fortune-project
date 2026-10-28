import LopanLoader from "./LopanLoader.js";

const loader=new LopanLoader();

await loader.initialize();

console.log(loader.getMaster());

console.log(loader.getLayer(1));

console.log(loader.getLayer(24));

