import Vue from 'vue'
import Router from 'vue-router'
import Index from '../components/Index'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import Detail from "../components/Detail";
import Cart from "../components/Cart";
import CartItem from "../components/CartItem";
import Order from "../components/Order";
import OrderSuccess from "../components/OrderSuccess";

Vue.use(Router)

export default new Router({
    mode:'history',
  routes: [
      {path:'/index',component:Index},
      {path:'/',component:Home},
      {path:'/login',component:Login},
      {path:'/register',component:Register},
      {path:'/course',component:Course},
      {path:'/detail/:id',component:Detail},
      {path:'/cart',component:Cart},
      {path:'/cartitem',component:CartItem},
      {path:'/order',component:Order},
      {path:'/result',component:OrderSuccess},
  ]
})
