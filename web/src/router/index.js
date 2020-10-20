import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

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
        path: '/infoManage/item',
        name: 'item',
        component: () => import('@/views/InfoManage/Item/Item')
      },
      {
        path: '/safetyAnalysis/analysisRules/generalRules',
        name: 'generalRules',
        component: () => import('@/views/SafetyAnalysis/AnalysisRules/GeneralRules')
      },
      {
        path: '/safetyAnalysis/analysisRules/specialRules',
        name: 'specialRules',
        component: () => import('@/views/SafetyAnalysis/AnalysisRules/SpecialRules')
      },
      {
        path: '/safetyAnalysis/implement/check',
        name: 'check',
        component: () => import('@/views/SafetyAnalysis/Implement/Check')
      },
      {
        path: '/safetyAnalysis/implement/demandExtraction',
        name: 'demandExtraction',
        component: () => import('@/views/SafetyAnalysis/Implement/DemandExtraction')
      },
      {
        path: '/safetyAnalysis/implement/failureAnalysis',
        name: 'failureAnalysis',
        component: () => import('@/views/SafetyAnalysis/Implement/FailureAnalysis')
      },
      {
        path: '/safetyAnalysis/modeling/subScene',
        name: 'subScene',
        component: () => import('@/views/SafetyAnalysis/Modeling/SubScene')
      },
      {
        path: '/safetyAnalysis/modeling/complexScene',
        name: 'complexScene',
        component: () => import('@/views/SafetyAnalysis/Modeling/ComplexScene')
      },
      {
        path: '/safetyAnalysis/modeling/listGeneration',
        name: 'listGeneration',
        component: () => import('@/views/SafetyAnalysis/Modeling/ListGeneration')
      },
      {
        path: '/safetyAnalysis/requirements/requirements',
        name: 'requirements',
        component: () => import('@/views/SafetyAnalysis/Requirements/Requirements')
      },
      {
        path: '/safetyDesign/complete/complete',
        name: 'complete',
        component: () => import('@/views/SafetyDesign/Complete/Complete')
      },
      {
        path: '/safetyDesign/criteria/generalCriteria',
        name: 'generalCriteria',
        component: () => import('@/views/SafetyDesign/Criteria/GeneralCriteria')
      },
      {
        path: '/safetyDesign/criteria/specialCriteria',
        name: 'specialCriteria',
        component: () => import('@/views/SafetyDesign/Criteria/SpecialCriteria')
      },
      {
        path: '/safetyDesign/verification/verification',
        name: 'verification',
        component: () => import('@/views/SafetyDesign/Verification/Verification')
      },
      {
        path: '/infoManage/system/authority',
        name: 'authority',
        component: () => import('@/views/InfoManage/System/Authority')
      },
      {
        path: '/infoManage/system/personnel',
        name: 'personnel',
        component: () => import('@/views/InfoManage/System/Personnel')
      },
      {
        path: '/infoManage/system/tools',
        name: 'tools',
        component: () => import('@/views/InfoManage/System/Tools')
      },
      {
        path: '/database/analysisBase/analysisBase',
        name: 'analysisBase',
        component: () => import('@/views/Database/AnalysisBase/AnalysisBase')
      },
      {
        path: '/database/designBase/designBase',
        name: 'designBase',
        component: () => import('@/views/Database/DesignBase/DesignBase')
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
