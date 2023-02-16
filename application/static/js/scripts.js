window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


$(".start-register").click(function(){
    console.log("starting")
    $.post("/web/register/start",function( data ) {
        console.log(data);
        $(".register_status").html("产号中")
    });
})


$(".stop-register").click(function(){
    console.log("stoping")
     $.post("/web/register/stop",function( data ) {
        console.log(data);
         $(".register_status").html("已停产")
    });
})






$(function(){
    initTable();


    $('#status').change(function () {
        $("#bootstrapTable").bootstrapTable('refresh')
    })

    $("#is_sold").change(function () {
        $("#bootstrapTable").bootstrapTable('refresh')
    })

    $("#server").change(function () {
        $("#bootstrapTable").bootstrapTable('refresh')
    })

});
function initTable() {

    //先销毁表格
    $("#bootstrapTable").bootstrapTable({
        //服务器数据的请求方式 'get' 或 'post'。
        loadingFontSize: '12px',
        method: 'get',
        //设置为 true 会有隔行变色效果
        striped: true,
        //设置为 true 会在表格底部显示分页条。
        pagination: true,
        //请求后台的URL
        url: '/web/accounts',
        //服务器返回的数据类型。
        dataType: 'json',
        //工具按钮用哪个容器
        toolbar: '#toolbar',
        //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性
        cache: false,
        //设置为 true 启用分页条无限循环的功能
//         paginationLoop: true,
        //设置在哪里进行分页，可选值为 'client' 或者 'server'。设置 'server'时，必须设置服务器数据地址（url）或者重写ajax方法
        sidePagination: 'server',
        //初始化加载第一页，默认第一页
        pageNumber: 1,
        //每页的记录行数
        pageSize: 20,
        //可供选择的每页的行数
        pageList: [10,15,20, 50, 100],
        //设置为false 将禁止所有列的排序。
        sortable: true,
        //设置默认排序为 name
        sortName: 'created_at',
        //定义排序方式，'asc' 或者 'desc'。
        sortOrder: "desc",
        //是否显示右上角的搜索框
        search: true,
        //是否启用点击选中行
//         clickToSelect: true,
        //设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
        //设置为limit可以获取limit, offset, search, sort, order
        queryParamsType:'undefined',
        //请求服务器数据
        queryParams: function queryParams(params){
            var param = {
                 page: params.pageNumber,
                 size: params.pageSize,
                 keyword: params.searchText,

             };
             var status = $("#status").val()
             if (status){
                 param.status=status
             }
             var is_sold = $("#is_sold").val()
             if (is_sold){
                 param.is_sold=is_sold
             }
             var server = $("#server").val()
             if (server){
                param.server=server
             }
             return param;
        },
        //加载成功时执行
        onLoadSuccess: function(data){
            console.log("加载成功");
        },
        //加载失败时执行
        onLoadError: function(status){

            console.log("加载数据失败"+status);
        },

        columns: [
        {
            field: 'id',
            title: '编号',//标题  可不加
            align: 'center',
            valign: 'middle',
            sortable: false,
        },{
            field: 'wid',
            title: 'wid',
            align: 'center',
            valign: 'middle',
            sortable: false,
            width:  '80px'
        },{
            field: 'status',
            title: '状态',
            align: 'center',
            valign: 'middle',
            sortable: false
        },
        {
            field: 'price',
            title: '价格',
            align: 'center',
            valign: 'middle',
            sortable: false
        },
        {
            field: 'is_sold',
            title: '是否取出',
            align: 'center',
            valign: 'middle',
            sortable: false
        },
        {
            field: 'updated_at',
            title: '更新时间',
            align: 'center',
            valign: 'middle',
            sortable: false
        },{
            field: 'server',
            title: '所在设备',
            align: 'left',
            valign: 'middle',
            sortable: false
        },{
            field: 'country',
            title: '地区',
            align: 'left',
            valign: 'middle',
            sortable: false,

        },
        {
            field: 'public_key',
            title: 'public_key',
            align: 'left',
            valign: 'middle',
            sortable: false,

        },
        {
            field: 'private_key',
            title: 'private_key',
            align: 'left',
            valign: 'middle',
            sortable: false,

        }
        ]
    });
}
