import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//创建VueX对象
const store = new Vuex.Store({
  state: {
    //存放的键值对就是所要管理的状态
    name: 'helloVueX',
    item: ''
  },
  getters: {
    getItem(state) {
      return state.item
    }
  },
  mutations: {
    changeItem(state, newItem) {
      state.item = newItem
      console.log('changeItem', state.item)
    }
  }
})
export default store
// export default new Vuex.Store({
//   state: {},
//   mutations: {},
//   actions: {},
//   modules: {}
// })
