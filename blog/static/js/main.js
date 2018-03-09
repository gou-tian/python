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
        function createNavList(data, callback, insertEl, class_name) {
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
                a.setAttribute('target', '_blank');
                a.addEventListener('click', callback, false);
                li.appendChild(a);
                // li.addEventListener('click', callback, false);
                ul.appendChild(li);
            }
            // a.innerText = '关于我 | About ';
            // a.setAttribute('href','/about');
            // li.appendChild(a);
            // ul.appendChild(li);
            // 添加到页面
            // insertEl.appendChild(ul);

        }
        return {
            ajax: ajax,
            createNavList: createNavList
        }
    }(jQuery));

    w.onload = function(){
        // 创建页面导航
        var list = [];
        (function(){
            var nav = doc.querySelectorAll('.top-nav>li');
            var i = 0,
                len = nav.length;
            for(; i < len; i++) {
                nav[i].index = i;
                nav[i].addEventListener('click', function(ev){
                    ev.preventDefault();
                    var child = $(this).children('a');
                    console.log(child.data());
                    if (list.length > 0) {
                        console.log(list);
                    } else {
                        utils.ajax.get('list', function(res){
                           console.log('article_column_relation',res.data);
                           list = res.data;
                        }, 'json');
                    }
                    return false;
                }, false)
            }
        }());
        // 以下为测试ajax get和post方法
        /*utils.ajax.get('ajax_return',{'name': 'jack', 'age': 32}, function(res){
           console.log(res, typeof res);
        });
        utils.ajax.post('ajax_return',{'name': 'jack','age': 32, 'sex': 'male'}, function(res){
           console.log(res, typeof res);
        })*/
    };
}(window));