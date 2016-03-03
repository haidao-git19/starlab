
    var map = new AMap.Map('container', {
        resizeEnable: true,
        center: [116.30946, 39.937629],
        zoom: 3
    });

    var amapAdcode = {};
    amapAdcode._district = new AMap.DistrictSearch({//高德行政区划查询插件实例
        subdistrict: 1   //返回下一级行政区
    });
    amapAdcode._overlay = [];//行政区划覆盖物
    amapAdcode.createSelectList = function(selectId, list) {//生成下拉列表
        var selectList = document.getElementById(selectId);
        selectList.innerHTML = '';
        selectList.add(new Option('--请选择--'));
        for (var i = 0, l = list.length, option; i < l; i++) {
            option = new Option(list[i].name);
            option.setAttribute("value", list[i].adcode);
            selectList.add(option);
        }
    };
    amapAdcode.search = function(adcodeLevel, keyword, selectId) {//查询行政区划列表并生成相应的下拉列表
        var me = this;
        if (adcodeLevel == 'district'||adcodeLevel == 'city') {//第三级时查询边界点
            this._district.setExtensions('all');
        } else {
            this._district.setExtensions('base');
        }
        this._district.setLevel(adcodeLevel); //行政区级别
        this._district.search(keyword, function(status, result) {//注意，api返回的格式不统一，在下面用三个条件分别处理
            var districtData = result.districtList[0];
            if (districtData.districtList) {
                me.createSelectList(selectId, districtData.districtList);
            } else if (districtData.districts) {
                me.createSelectList(selectId, districtData.districts);
            } else {
                document.getElementById(selectId).innerHTML = '';
            }
            map.setCenter(districtData.center);
            me.clearMap();
            me.addPolygon(districtData.boundaries);
        });
    };
    amapAdcode.clearMap = function(selectId) {//清空地图上的覆盖物
        map.remove(this._overlay);
        this._overlay = [];
    };
    amapAdcode.addPolygon = function(boundaries) {//往地图上添加覆盖物
        if (boundaries) {
            for (var i = 0, l = boundaries.length; i < l; i++) {
                //生成行政区划polygon
                var polygon = new AMap.Polygon({
                    map: map,
                    path: boundaries[i]
                });
                this._overlay.push(polygon);
            }
            map.setFitView();//地图自适应
        }
    };
    amapAdcode.clear = function(selectId) {//清空下拉列表
        var selectList = document.getElementById(selectId);
        selectList.innerHTML = '';
    };
    amapAdcode.createProvince = function() {//创建省列表
        this.search('country', '中国', 'province');
    };
    amapAdcode.createCity = function(provinceAdcode) {//创建市列表
        this.search('province', provinceAdcode, 'city');
        this.clear('district');
        this.clear('biz_area');
    };
    amapAdcode.createDistrict = function(cityAdcode) {//创建区县列表
        this.search('city', cityAdcode, 'district');
        this.clear('biz_area');
    };
    amapAdcode.createBiz = function(districtAdcode) {//创建商圈列表
        this.search('district', districtAdcode, 'biz_area');
    };
    amapAdcode.createProvince();