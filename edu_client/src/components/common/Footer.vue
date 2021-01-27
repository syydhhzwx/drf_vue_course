<template>
    <div class="footer">
        <ul class="nav full-left">
            <li v-for="(v,i) in footer_list" :key="i">
                <a :href="v.link" style="color: white"  v-if="v.is_site">{{v.title}}</a>
                <router-link v-else-if="!v.is_site" to="/index" style="color: white">{{v.title}}</router-link>
            </li>

        </ul>
    </div>
</template>

<script>
export default {
    name: "Footer",
    data(){
        return{
            footer_list:[]
        }
    },
    methods: {
        get_all(){
            this.axios({
                url: this.$settings.HOST+'home/footer/',
                method: 'get',
            }).then(res =>{
                console.log(res);
                this.footer_list = res.data
            }).catch(error =>{
                console.log(error);
            })
        }
    },
    created() {
        this.get_all()
    }
}
</script>

<style scoped>
.footer {
    width: 100%;
    height: 128px;
    background: #25292e;
    color: #fff;
}

.footer ul {
    margin: 0 auto 16px;
    padding-top: 38px;
    width: 810px;
    padding-left: 410px;
}

.footer ul li {
    float: left;
    width: 112px;
    margin: 0 10px;
    text-align: center;
    font-size: 14px;
}

.footer ul::after {
    content: "";
    display: block;
    clear: both;
}

.footer p {
    text-align: center;
    font-size: 12px;
}
</style>
