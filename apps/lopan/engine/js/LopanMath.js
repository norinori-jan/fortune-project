export default class LopanMath {

    static DEG2RAD = Math.PI / 180;
    static RAD2DEG = 180 / Math.PI;

    /**
     * 度→ラジアン
     */
    static toRadians(degree){
        return degree * this.DEG2RAD;
    }

    /**
     * ラジアン→度
     */
    static toDegrees(rad){
        return rad * this.RAD2DEG;
    }

    /**
     * 角度正規化
     */
    static normalize(angle){

        angle %= 360;

        if(angle < 0)
            angle += 360;

        return angle;
    }

}

/**
 * 区画中心角
 */
static middle(start,end){

    if(end < start)
        end += 360;

    return this.normalize((start+end)/2);

}

/**
 * 円周上座標
 */
static polar(radius,angle){

    const rad=this.toRadians(angle);

    return{

        x:radius*Math.cos(rad),

        y:radius*Math.sin(rad)

    };

}

/**
 * SVG Arc Path
 */
static arcPath(innerRadius,outerRadius,start,end){

    const s1=this.polar(outerRadius,start);
    const e1=this.polar(outerRadius,end);

    const s2=this.polar(innerRadius,end);
    const e2=this.polar(innerRadius,start);

    let sweep=end-start;

    if(sweep<0)
        sweep+=360;

    const large=sweep>180?1:0;

    return `
M ${s1.x} ${s1.y}
A ${outerRadius} ${outerRadius} 0 ${large} 1 ${e1.x} ${e1.y}
L ${s2.x} ${s2.y}
A ${innerRadius} ${innerRadius} 0 ${large} 0 ${e2.x} ${e2.y}
Z`;
}

/**
 * 文字配置
 */
static textPosition(innerRadius,outerRadius,start,end){

    const angle=this.middle(start,end);

    const radius=(innerRadius+outerRadius)/2;

    return this.polar(radius,angle);

}

/**
 * テキスト角度
 */
static textRotation(start,end){

    let angle=this.middle(start,end);

    if(angle>90 && angle<270)
        angle+=180;

    return angle;

}

/**
 * セル検索
 */
static findCell(master,angle){

    angle=this.normalize(angle);

    return master.find(cell=>{

        return angle>=cell.start_angle &&
               angle<cell.end_angle;

    });

}

/**
 * 山検索
 */
static findMountain(corrections,angle){

    angle=this.normalize(angle);

    let nearest=null;

    let min=999;

    corrections.forEach(m=>{

        let d=Math.abs(m.actual-angle);

        if(d>180)
            d=360-d;

        if(d<min){

            min=d;

            nearest=m;

        }

    });

    return nearest;

}

