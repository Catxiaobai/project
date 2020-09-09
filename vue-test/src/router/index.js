import Vue from 'vue'
import VueRouter from 'vue-router'
// import view from 'vue-router/src/components/view'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('@/views/Test'),
    children: [
      {
        path: '/',
        name: 'home',
        component: () => import('@/views/Home/Home')
      },
      {
        path: '/item',
        name: 'item',
        component: () => import('@/views/Item/Item')
      },
      {
        path: '/person',
        name: 'person',
        component: () => import('@/views/Person/Person')
      }
    ]
  },
  {
    path: '/trace',
    component: () => import('@/views/Test'),
    children: [
      {
        path: '/page1',
        name: 'page1',
        component: () => import('@/views/Other/PageOne')
      },
      {
        path: '/page2',
        name: 'page2',
        component: () => import('@/views/Other/PageTwo')
      },
      {
        path: '/completeness',
        name: 'completeness',
        component: () => import('@/views/Trace/VerifyModel/Completeness')
      },
      {
        path: '/judgeModel',
        name: 'judgeModel',
        component: () => import('@/views/Trace/VerifyModel/JudgeModel')
      },
      {
        path: '/invalid',
        name: 'invalid',
        component: () => import('@/views/Trace/InvalidTrace/Invalid')
      },
      {
        path: '/safeVerify',
        name: 'safeVerify',
        component: () => import('@/views/Trace/Safety/SafeVerify')
      },
      {
        path: '/safeAssess',
        name: 'safeAssess',
        component: () => import('@/views/Trace/Safety/SafeAssess')
      },
      {
        path: '/used',
        name: 'used',
        component: () => import('@/views/Trace/UsedTrace/Used')
      },
      {
        path: '/usedTrace',
        name: 'usedTrace',
        component: () => import('@/views/Trace/UsedTrace/UsedTrace')
      },
      {
        path: '/addTrace',
        name: 'addTrace',
        component: () => import('@/views/Trace/UsedTrace/AddTrace')
      },
      {
        path: '/importTrace',
        name: 'importTrace',
        component: () => import('@/views/Trace/UsedTrace/ImportTrace')
      },
      {
        path: '/addInvalidTrace',
        name: 'addInvalidTrace',
        component: () => import('@/views/Trace/InvalidTrace/AddInvalidTrace')
      },
      {
        path: '/importInvalidTrace',
        name: 'importInvalidTrace',
        component: () => import('@/views/Trace/InvalidTrace/ImportInvalidTrace')
      },
      {
        path: '/createModel',
        name: 'createModel',
        component: () => import('@/views/Trace/Model/CreateModel')
      },
      {
        path: '/editModel',
        name: 'editModel',
        component: () => import('@/views/Trace/Model/EditModel')
      },
      {
        path: '/showModel',
        name: 'showModel',
        component: () => import('@/views/Trace/Model/ShowModel')
      },
      {
        path: '/completionModel',
        name: 'completionModel',
        component: () => import('@/views/Trace/VerifyModel/CompletionModel')
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
