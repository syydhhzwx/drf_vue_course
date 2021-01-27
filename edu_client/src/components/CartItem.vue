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
            <el-select size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option label="1个月有效" value="30" key="30"></el-option>
                <el-option label="2个月有效" value="60" key="60"></el-option>
                <el-option label="3个月有效" value="90" key="90"></el-option>
                <el-option label="永久有效" value="10000" key="10000"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">{{ course.price }}</div>
        <div class="cart_column column_4" > <el-button @click="del_course(course.id)">删除</el-button> </div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    props: ['course'],
    watch: {
        "course.selected": function () {
            this.get_selected();
        }
    },
    methods: {
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

                    this.$message.success('删除成功')
                }
            }).catch(error=>{
                console.log(error);
            })
        }
    }
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

