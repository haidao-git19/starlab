var StationMap = {};
StationMap.init = function () {
    this.createMap();
    //this.getData();
    //this.autoUpdate();
};
StationMap.createMap= function () {
    var map = new AMap.Map('container', {
        center: [107.885629, 32.798837],
        /*layers: [new AMap.TileLayer.Satellite()],*/
        zoom: 5,
        resizeEnable:true,
        mapStyle:"blue_night"
    });
    var toolBar = new AMap.ToolBar({
        visible: true
    });
    map.addControl(toolBar);
    map.on("complete", completeEventHandler);

    this.map=map;

    var thisRef=this;
    function completeEventHandler() {
        //map.setMapStyle("blue_night");
        thisRef.getData();
    }
};

StationMap.getData = function () {
    var thisRef = this;
    $.ajax({
        //url: 'mockservice/apiResult' + Math.round(Math.random()) + '.json',
        url:stationMapConfig.apiUrl,
        data: {},
        success: function (data) {
            thisRef.addStations(data.data.stations);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(textStatus);
        }
    });
    $.ajax({
        //url: 'mockservice/apiResult' + Math.round(Math.random()) + '.json',
        url:stationMapConfig.apiGridUrl,
        data: {},
        success: function (data) {
            var lngLats=MapUtils.coord2DStrToLngLats(data.data.grid.join(","));
            thisRef.addGrids(lngLats);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(textStatus);
        }
    });
};
StationMap.renderData = function (data) {
    this.addStations(data.stations);
    var lngLats=MapUtils.coord2DStrToLngLats(data.grid.join(","));
    //this.drawGridLine(lngLats);
    this.addGrids(lngLats);
    //地图自适应
/*    var map =this.map;
    //map.setFitView();
    var bounds=new AMap.Bounds(new AMap.LngLat(76.245004,16.590842), new AMap.LngLat(139.526254,49.006833));
    map.setBounds(bounds);
    map.zoomIn();*/
};
StationMap.addStations=function(data){
    var arrData=data,vectorPoints=[];//矢量点数组
    var info={},vectorPoint=null;//每个矢量点的信息
    for (var i=0,iCount=arrData.length;i<iCount;i++){
        //获取每个矢量点的信息
        info=arrData[i];
         //添加每个矢量点
        vectorPoint=this.addStation(info);
        //用于返回矢量点数组
        vectorPoints.push(vectorPoint);
    }
    // 返回矢量点数组
    return vectorPoints;
};
StationMap.addStation=function(obj){
    var map =this.map;
    obj.imagePath="img/station"+(obj.type||"")+".png";
    var marker = new AMap.Marker({
        map: map,
        position: new AMap.LngLat(obj.lon,obj.lat),
        icon: new AMap.Icon({image:obj.imagePath,imageSize:new AMap.Size(16,16)}),
        title:obj.name
        //label:{content:obj.name},
        //offset: new AMap.Pixel(-19, -60)//x为图标一半宽度的负值，y为图标高度的负值
        //autoRotation: true
    });
    return marker;
};
StationMap.getStyleByType=function(type){
};
StationMap.addGrids=function(points){
    var point={};
    for(var i= 0,iCount=points.length;i<iCount;i++){
        point=points[i];
        this.drawRect(point);
    }
};
//绘制面
StationMap.drawArea=function(lngLats){
    var map =this.map;
    var  polygon = new AMap.Polygon({
        path: lngLats,//设置多边形边界路径
        strokeColor: "#2C64B0", //线颜色
        strokeOpacity: 0.7, //线透明度
        strokeWeight: 1,    //线宽
        fillColor: "#2C64B0", //填充色
        fillOpacity: 0.7//填充透明度
    });
    polygon.setMap(map);
};
StationMap.drawRect=function(point){
    var lngLats=[];
    var lng=point.lng;
    var lat=point.lat;
    lngLats.push(new AMap.LngLat(lng-0.1,lat+0.1));
    lngLats.push(new AMap.LngLat(lng+0.1,lat+0.1));
    lngLats.push(new AMap.LngLat(lng+0.1,lat-0.1));
    lngLats.push(new AMap.LngLat(lng-0.1,lat-0.1));
    this.drawArea(lngLats);
};

//绘制网格线
StationMap.drawGridLine=function(points){
    var map=this.map;
    //找出维度一样的数据
    //找出经度一样的数据
    var pointsObj={},point={},lng=0,lat=0;
    for(var i= 0,iCount=points.length;i<iCount;i++){
        point=points[i];
        lng=point.lng-0.1;
        lat=point.lat+0.1;
        pointsObj[lng]=pointsObj[lng]||[];
        pointsObj[lat]=pointsObj[lat]||[];

        pointsObj[lng].push(point);
        pointsObj[lat].push(point);
    }
    //绘制网格线
    var subPois=[],lngLats=[],lngLat={};
    for(var p in pointsObj){
        subPois=pointsObj[p];
        lngLats=[];
        for(var i= 0,iCount=subPois.length;i<iCount;i++){
            point=subPois[i];
            lngLat = new AMap.LngLat(point.lng,point.lat);
            lngLats.push(lngLat);
        }
        // 绘制线
        var polyline = new AMap.Polyline({
            map: map,
            path: lngLats,
            strokeColor: "#FFFC18",  //线颜色
            strokeOpacity: 0.2,     //线透明度
            strokeWeight: 2,      //线宽
            strokeStyle: "solid"  //线样式
        });
    }
};
