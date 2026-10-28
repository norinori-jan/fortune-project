export default class LopanLoader {

    constructor(basePath = "./data") {

        this.basePath = basePath;

        this.master = null;

        this.layers = {};

        this.corrections = {};

    }

    async loadJSON(path){

        const response = await fetch(path);

        if(!response.ok){

            throw new Error(`Load Error : ${path}`);

        }

        return await response.json();

    }

}

async loadMaster(){

    this.master = await this.loadJSON(

        `${this.basePath}/master/lopan_master.json`

    );

    return this.master;

}

async loadLayer(layer){

    const data = await this.loadJSON(

        `${this.basePath}/layers/layer${String(layer).padStart(2,"0")}.json`

    );

    this.layers[layer]=data;

    return data;

}

async loadAllLayers(){

    const promises=[];

    for(let i=1;i<=26;i++){

        promises.push(this.loadLayer(i));

    }

    await Promise.all(promises);

}

async loadCorrections(){

    this.corrections=

        await this.loadJSON(

            `${this.basePath}/corrections/corrections.json`

        );

}

async initialize(){

    await this.loadMaster();

    await this.loadAllLayers();

    await this.loadCorrections();

    return this;

}


getLayer(number){

    return this.layers[number];

}

getMaster(){

    return this.master;

}

getCorrections(){

    return this.corrections;

}
