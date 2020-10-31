import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
    path: '/',
    redirect: '/login'
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
        path: '/main',
        name: 'home',
        component: () => import('@/views/Home/Home')
      },
      {
        path: '/item',
        name: 'item',
        component: () => import('@/views/InfoManage/Item/Item')
      },
      {
        path: '/analysisBase',
        name: 'analysisBase',
        component: () => import('@/views/Database/AnalysisBase/AnalysisBase')
      },
      {
        path: '/designBase',
        name: 'designBase',
        component: () => import('@/views/Database/DesignBase/DesignBase')
      },
      {
        path: '/authority',
        name: 'authority',
        component: () => import('@/views/InfoManage/System/Authority')
      },
      {
        path: '/personnel',
        name: 'personnel',
        component: () => import('@/views/InfoManage/System/Personnel')
      },
      {
        path: '/tools',
        name: 'tools',
        component: () => import('@/views/InfoManage/System/Tools')
      }
    ]
  },
  {
    path: '/itemMain',
    name: 'itemMain',
    component: () => import('@/views/ItemMain'),
    children: [
      {
        path: '/itemMain',
        name: 'home',
        component: () => import('@/views/Home/Home')
      },
      // {
      //   path: '/item',
      //   name: 'item',
      //   component: () => import('@/views/InfoManage/Item/Item')
      // },
      {
        path: '/generalRules',
        name: 'generalRules',
        component: () => import('@/views/SafetyAnalysis/AnalysisRules/GeneralRules')
      },
      {
        path: '/specialRules',
        name: 'specialRules',
        component: () => import('@/views/SafetyAnalysis/AnalysisRules/SpecialRules')
      },
      {
        path: '/instantiate',
        name: 'instantiate',
        component: () => import('@/views/SafetyAnalysis/AnalysisRules/Instantiate')
      },
      {
        path: '/check',
        name: 'check',
        component: () => import('@/views/SafetyAnalysis/Implement/Check')
      },
      {
        path: '/demandExtraction',
        name: 'demandExtraction',
        component: () => import('@/views/SafetyAnalysis/Implement/DemandExtraction')
      },
      {
        path: '/failureAnalysis',
        name: 'failureAnalysis',
        component: () => import('@/views/SafetyAnalysis/Implement/FailureAnalysis')
      },
      // {
      //   path: '/subScene',
      //   name: 'subScene',
      //   component: () => import('@/views/SafetyAnalysis/Modeling/SubScene')
      // },
      // {
      //   path: '/complexScene',
      //   name: 'complexScene',
      //   component: () => import('@/views/SafetyAnalysis/Modeling/ComplexScene')
      // },
      {
        path: '/listGeneration',
        name: 'listGeneration',
        component: () => import('@/views/SafetyAnalysis/Modeling/ListGeneration')
      },
      {
        path: '/requirements',
        name: 'requirements',
        component: () => import('@/views/SafetyAnalysis/Requirements/Requirements')
      },
      {
        path: '/complete',
        name: 'complete',
        component: () => import('@/views/SafetyDesign/Complete/Complete')
      },
      {
        path: '/generalCriteria',
        name: 'generalCriteria',
        component: () => import('@/views/SafetyDesign/Criteria/GeneralCriteria')
      },
      {
        path: '/specialCriteria',
        name: 'specialCriteria',
        component: () => import('@/views/SafetyDesign/Criteria/SpecialCriteria')
      },
      {
        path: '/verification',
        name: 'verification',
        component: () => import('@/views/SafetyDesign/Verification/Verification')
      },
      {
        path: '/subSceneInfo',
        name: 'subSceneInfo',
        component: () => import('@/views/SafetyAnalysis/Modeling/SubScene/SubSceneInfo')
      },
      {
        path: '/subSceneModel',
        name: 'subSceneModel',
        component: () => import('@/views/SafetyAnalysis/Modeling/SubScene/SubSceneModel')
      },
      {
        path: '/complexSceneInfo',
        name: 'complexSceneInfo',
        component: () => import('@/views/SafetyAnalysis/Modeling/ComplexScene/ComplexSceneInfo')
      },
      {
        path: '/complexSceneModel',
        name: 'complexSceneModel',
        component: () => import('@/views/SafetyAnalysis/Modeling/ComplexScene/ComplexSceneModel')
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
