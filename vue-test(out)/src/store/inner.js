export default {
  state: {
    isCollapsed: false,
    currentMenu: null,
    menu: [],
    tabsList: [
      {
        path: '/trace',
        name: 'trace',
        label: '场景',
        icon: 's-home'
      }
    ]
  },
  mutations: {
    selectMenu(state, val) {
      // val.name === 'home' ? (state.currentMenu = null) : (state.currentMenu = val)
      if (val.name !== 'trace') {
        state.currentMenu = val
        let result = state.tabsList.findIndex(item => item.name === val.name)
        result === -1 ? state.tabsList.push(val) : ''
      } else {
        state.currentMenu = null
      }
    },
    closeTab(state, val) {
      let result = state.tabsList.findIndex(item => item.name === val.name)
      state.tabsList.splice(result, 1)
    },
    collapseMenu(state) {
      state.isCollapsed = !state.isCollapsed
    }
  },
  actions: {}
}
