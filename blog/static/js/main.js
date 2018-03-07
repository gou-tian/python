(function(w){
    var doc = w.document;
    // var body = doc.body;
    var utils = (function($){
        // 数据请求
        var ajax = {
            get: function(url, data, callback, dataTyep) {
                dataTyep = dataTyep || 'json';
                return $.get(url, data, callback, dataTyep)
            },
            post: function(url, data, callback, dataTyep) {
                dataTyep = dataTyep || 'json';
                return $.post(url, data, callback, dataTyep)
            }
        };
        // 创建页面导航
        function createNavList(data, insertEl, class_name) {
            // 设置添加元素位置
            insertEl = insertEl || doc.querySelector('.top-bar');
            // 设置样式列表
            class_name = class_name || 'top-nav pull-right clearfix';

            var ul = doc.createElement('ul'),
                i = 0,
                len = data.length;
            // 设置父元素样式
            ul.className = class_name;
            for(; i < len; i++) {
                var li = doc.createElement('li'),
                    a = doc.createElement('a');
                a.innerText = data[i].name;
                a.setAttribute('href',data[i].slug || 'javascript:;');
                a.setAttribute('data-mid', data[i].mid);
                // a.setAttribute('target', '_blank');
                a.addEventListener('click', function(ev){
                    console.log(this);
                    return false;
                }, false);
                li.appendChild(a);
                ul.appendChild(li);
            }
            // a.innerText = '关于我 | About ';
            // a.setAttribute('href','/about');
            // li.appendChild(a);
            // ul.appendChild(li);
            // 添加到页面
            // $('.top-nav').on('click','li>a', function(){
            //     console.log(this);
            //     return false;
            // });
            li.addEventListener('click', function(ev){
                /*var li = this.children,
                    i = 0,
                    len = li.length;
                for(; i < len; i++) {
                    li[i].index = i;
                    li[i].addEventListener('click', function(ev){

                        for(var j = 0; j < len; j++) {
                            if (j === this.index) {
                                console.log(this);
                            }
                        }

                        return false;
                    })
                }*/
                console.log(this);
            }, false);
            insertEl.appendChild(ul);

        }
        return {
            ajax: ajax,
            createNavList: createNavList
        }
    }(jQuery));

    w.onload = function(){
        // 创建页面导航
        utils.ajax.get('nav', function(res){
           console.log(res, typeof res);
           utils.createNavList(res);
        });
        console.log($('.top-nav'))
        // 以下为测试ajax get和post方法
        /*utils.ajax.get('ajax_return',{'name': 'jack', 'age': 32}, function(res){
           console.log(res, typeof res);
        });
        utils.ajax.post('ajax_return',{'name': 'jack','age': 32, 'sex': 'male'}, function(res){
           console.log(res, typeof res);
        })*/
    };
}(window));