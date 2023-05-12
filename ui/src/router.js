import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import SignupView from './views/SignupView.vue'
import DashboardView from './views/DashboardView.vue';
import CreatePostView from './views/CreatePostView.vue';
import UpdatePostView from '@/views/UpdatePostView.vue'
import DeletePostView from '@/views/DeletePostView.vue'
import SearchPageView from "@/views/SearchPageView.vue";
import ProfileView from '@/views/ProfileView.vue'
import ProfileUpdate from '@/views/ProfileUpdate.vue'
import UserView from '@/views/UserView.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'loginView',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'SignupView',
    component: SignupView
  },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
  {
    path: '/createposts',
    name: 'CreatePost',
    component: CreatePostView,
  },
    {
    path: '/updatepost/:id',
    name: 'UpdatePost',
    component: UpdatePostView,
    props: true,
  },
  {
    path: '/deletepost/:id',
    name: 'DeletePost',
    component: DeletePostView,
    props: true,
  },
    {
      path: '/search',
      component: SearchPageView
    },
    {
    path: '/profile',
    name: 'Profile',
    component: ProfileView
  },
    {
      path: '/user/:id/update',
      name: 'UpdateProfile',
      component: ProfileUpdate
    },
    {
    path: '/user/:username',
    name: 'UserView',
    component: UserView,
  },
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router