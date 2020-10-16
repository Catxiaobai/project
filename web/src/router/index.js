import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/main'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login/Login')
  },
  {
    path: '/main',
    name: 'main',
    component: () => import('@/views/Main'),
    children: [
      {
        path: '/featureListGeneration',
        name: 'featureListGeneration',
        component: () => import('@/views/Item/Sub_scene_modeling/FeatureListGeneration')
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
