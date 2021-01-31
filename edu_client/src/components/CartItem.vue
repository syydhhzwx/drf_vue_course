<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link to="/course/detail/1">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option v-for="item in course.expire_list"  :label="item.expire_list" :value="item.id" :key="item.id"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4" >{{course.real_price.toFixed(2)}}</div>
<!--        <div class="cart_column column_4" v-el>{{ parseInt(course.price) }}</div>-->
        <div class="cart_column column_4" > <el-button @click="del_course(course.id)">删除</el-button> </div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    props: ['course'],
    data(){
        return{

        }

    },
    watch: {
        // 监测selected是否改变
        "course.selected": function () {
            this.get_selected();
        },
        // 监听课程对应的有效期id是否发生改变
        'course.expire_id':function () {
            this.change_expire()
        }
    },
    methods: {
        //修改redis中的有效期
        change_expire(){
            // 修改有效期  并得到有效期对应的价格价格
            // console.log(this.real_price);
            let token = sessionStorage.token || localStorage.token;
            this.axios.put(this.$settings.HOST+'cart/option/',{
                //要修改的有效期id，要修改课程id
                expric_id: this.course.expire_id,
                course_id: this.course.id,

            },{
                headers:{
                    'Authorization': 'jwt ' + token
                }
            }).then(res =>{
                console.log(res.data);
                this.$message.success('切换成功')
                console.log(res.data.price);
                if (res.data.price){
                    this.course.real_price = res.data.price
                    // this.$router.go(0)
                    // 当有限期切换时向父组件提交事件来修改总价
                    this.$emit('change_expice')
                }
            }).catch(error=>{
                console.log(error);
            })
        },
        // 切换选中状态
        get_selected() {
            let user_id = sessionStorage.getItem('user_id')
            console.log(this.course);
            if (this.course.selected) {
                this.axios.post(this.$settings.HOST + 'cart/del/', {
                    course_id: this.course.id,
                    user_id: user_id,
                }).then(res => {
                    console.log(res.data);
                    if (!res.data.message){
                        this.$message.success('当前状态已改变')

                    }
                }).catch(error=>{
                    console.log(error);
                })
            }else if (!this.course.selected){
                this.axios({
                    url:this.$settings.HOST + 'cart/del/',
                    method: 'delete',
                    data:{
                        course_id: this.course.id,
                        user_id: user_id,
                    }
                }).then(res => {
                    console.log(res.data);
                    if (!res.data.message){
                        this.$message.success('当前状态已改变')
                    }
                }).catch(error=>{
                    console.log(error);
                })
            }
            // this.$message.success('当前状态已改变')
        },
        // 删除购物车中的课程
        del_course(id) {
            // alert(111)
            console.log(id);
            let user_id = sessionStorage.getItem('user_id')
            this.axios({
                url:this.$settings.HOST+'cart/del_course/',
                method: 'delete',
                data:{
                    course_id: this.course.id,
                    user_id: user_id,
                }

            }).then(res => {
                console.log(res.data);
                if (!res.data.message){
                    this.$router.go(0)
                    this.$message({
                        message: '删除成功',
                        type: 'success',
                        duration: 1000,
                    });
                }
            }).catch(error=>{
                console.log(error);
            })
        }
    },

}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
}

.cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}

</style>

