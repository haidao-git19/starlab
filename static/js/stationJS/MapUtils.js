var MapUtils = {};

/**
 * 计算bounds
 * @param {Array} lngs 经度数组，格式为[x1,x2,...,xn]
 * @param {Array} lats 维度数组，格式为[y1,y2,...,yn]
 * @returns {Object}
 */
MapUtils.getBounds=function(lngs,lats){
    lngs.sort(sortFunc);
    lats.sort(sortFunc);
    //创建视野范围
    var boundsObj={};
    boundsObj.minLng=lngs.shift();
    boundsObj.minLat=lats.shift();
    boundsObj.maxLng=lngs.pop();
    boundsObj.maxLat=lats.pop();
    return boundsObj;

    function sortFunc(a,b){if(a>b)return 1;if(a<b)return -1;return 0;}
};
/**
 * 2D坐标由字符串格式转化成LngLats格式
 * @param {String} coord2DStr 坐标字符串，格式为(x1,y1,x2,y2,...,xn,yn)或者(x1,y1;x2,y2;...,xn,yn)
 * @returns {Array} LngLat对象组成的数组
 */
MapUtils.coord2DStrToLngLats=function(coord2DStr) {
    if (!coord2DStr) {
        return;
    }
    var coord2DArr = coord2DStr.replace(/;/g, ",").split(",");
    var lngLat = null, lngLats = [];
    var lng = 0, lat = 0;
    for (var i = 0, iCount = coord2DArr.length; i < iCount; i = i + 2) {
        lng = coord2DArr[i];
        if (lng == "" || isNaN(lng)) {
            //alert("经度值无效，请检查！");// 不能为空值，不能为0，必须是数字
            break;
        }
        lat = coord2DArr[i + 1];
        if (lat == "" || isNaN(lat)) {
            //alert("纬度值无效，请检查！");// 不能为空值，不能为0，必须是数字
            break;
        }
        lngLat = new AMap.LngLat(lng, lat);
        lngLats.push(lngLat);
    }
    return lngLats;
};
/**
 * 转换坐标为字符串
 * @ignore
 * @param {Array} lngLats LngLat对象组成的数组
 * @param {String} [splitStr] 分隔字符，默认为,
 * @returns {String} 2D坐标串，坐标串格式为：x1,y1,...xn,yn
 */
MapUtils.lngLatsToCoord2DStr=function(lngLats,splitStr){
    var coordStr="",coordArr=[],lngLat=null;
    for(var i=0,iCount=lngLats.length;i<iCount;i++){
        lngLat=lngLats[i];
        coordArr.push(lngLat.getLng()+","+lngLat.getLat());
    }
    splitStr=splitStr||",";
    coordStr=coordArr.join(splitStr);
    return coordStr;
};
/**
 * 普通对象转化成LngLats格式
 * @param {Array} objs 普通对象数组，对象含有lon，lat属性
 * @returns {Array} LngLat对象组成的数组
 */
MapUtils.objsToLngLats=function(objs) {
    if (!objs) {
        return;
    }
    var obj=null;
    var lngLat = null, lngLats = [];
    var lng = 0, lat = 0;
    for (var i = 0, iCount = objs.length; i < iCount; i ++) {
        obj = objs[i];
        lng=obj.lon;
        if (lng == "" || isNaN(lng)) {
            //alert("经度值无效，请检查！");// 不能为空值，不能为0，必须是数字
            break;
        }
        lat = obj.lat;
        if (lat == "" || isNaN(lat)) {
            //alert("纬度值无效，请检查！");// 不能为空值，不能为0，必须是数字
            break;
        }
        lngLat = new AMap.LngLat(lng, lat);
        lngLats.push(lngLat);
    }
    return lngLats;
};