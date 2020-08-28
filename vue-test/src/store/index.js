import Vue from 'vue'
import Vuex from 'vuex'
import tab from '@/store/tab'
import inner from '@/store/inner'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    tab,
    inner
  }
})
